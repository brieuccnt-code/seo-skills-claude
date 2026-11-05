#!/usr/bin/env python3
"""Mesure la longueur du contenu principal des pages en tête de SERP et propose une fourchette.

Sources possibles (une seule) :
  --serp fichier.csv --keyword "mot-clé"   CSV keyword,position,url (même format que serp_cluster.py)
  --urls url1 url2 ...                     liste d'URL
  --html-dir dossier                       pages HTML déjà enregistrées (*.html)

--render : charge les pages dans un vrai navigateur (Playwright) pour lire aussi le contenu affiché
en JavaScript. Plus lent ; nécessite  py -m pip install playwright  et  py -m playwright install chromium.

Extraction : on retire script, style, nav, header, footer, aside, form ; on garde le plus grand
<article> ou <main> s'il existe, sinon le <body>. C'est une approximation : relire les cas
aberrants (page bloquée, contenu chargé en JavaScript, page de consentement).

Exemple :
  python serp_length.py --serp data/raw/serp.csv --keyword "voyage albanie" -o data/clean/longueur.csv
  python serp_length.py --serp data/raw/serp.csv --keyword "voyage albanie" --exclude-domains youtube.com,reddit.com -o ...

Sorties : CSV par page + résumé (médiane, P25, P75, fourchette recommandée) à l'écran et dans <sortie>_resume.txt
"""
import argparse
import csv
import glob
import os
import re
import statistics
import sys
import unicodedata
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

SKIP = {"script", "style", "noscript", "nav", "header", "footer", "aside", "form", "svg", "template",
        "iframe", "button", "select"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
WORD = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*|\d+(?:[.,]\d+)*", re.UNICODE)


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # tags ouverts
        self.skip = 0
        self.blocks = []         # [(tag, [textes])] pour article/main ouverts
        self.containers = []     # textes des article/main terminés
        self.body = []
        self.title, self.h1 = "", ""
        self.h2 = self.h3 = 0
        self._in_title = self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append(tag)
        if tag in SKIP:
            self.skip += 1
        if tag in ("article", "main"):
            self.blocks.append([])
        if tag == "title":
            self._in_title = True
        if tag == "h1" and not self.h1:
            self._in_h1 = True
        if not self.skip:
            if tag == "h2":
                self.h2 += 1
            elif tag == "h3":
                self.h3 += 1

    def handle_endtag(self, tag):
        if tag in VOID or tag not in self.stack:
            return
        while self.stack:
            t = self.stack.pop()
            if t in SKIP:
                self.skip = max(0, self.skip - 1)
            if t in ("article", "main") and self.blocks:
                self.containers.append(" ".join(self.blocks.pop()))
            if t == "title":
                self._in_title = False
            if t == "h1":
                self._in_h1 = False
            if t == tag:
                break

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1:
            self.h1 += data
        if self.skip:
            return
        self.body.append(data)
        for b in self.blocks:
            b.append(data)

    def result(self):
        while self.blocks:
            self.containers.append(" ".join(self.blocks.pop()))
        body_text = " ".join(self.body)
        best = max(self.containers, key=lambda t: len(WORD.findall(t)), default="")
        # un <main>/<article> minuscule (ex. bloc cookies) ne doit pas remplacer le body
        text = best if len(WORD.findall(best)) >= 0.3 * len(WORD.findall(body_text)) else body_text
        return {"words": len(WORD.findall(text)), "title": " ".join(self.title.split()),
                "h1": " ".join(self.h1.split()), "h2": self.h2, "h3": self.h3}


def analyse(html):
    p = Extract()
    try:
        p.feed(html)
        p.close()
    except Exception:
        pass
    return p.result()


class Renderer:
    """Charge les pages avec Playwright (option --render)."""
    def __init__(self, timeout):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            sys.exit("--render nécessite Playwright : py -m pip install playwright  puis  py -m playwright install chromium")
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch()
        self.ctx = self.browser.new_context(locale="fr-FR")
        self.timeout = timeout * 1000

    def fetch(self, url):
        page = self.ctx.new_page()
        try:
            resp = page.goto(url, wait_until="load", timeout=self.timeout)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            return (resp.status if resp else ""), page.content()
        finally:
            page.close()

    def close(self):
        self.browser.close()
        self.pw.stop()


def fetch(url, timeout):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; serp-length-check/1.0)",
                                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.5"})
    with urlopen(req, timeout=timeout) as r:
        raw = r.read(5_000_000)
        charset = r.headers.get_content_charset() or "utf-8"
        return r.status, raw.decode(charset, errors="replace")


def nh(h):
    return "".join(c for c in unicodedata.normalize("NFD", (h or "").replace("﻿", "").strip().lower())
                   if unicodedata.category(c) != "Mn")


def load_serp(path, keyword, top):
    raw = open(path, "rb").read()
    text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig", "replace")
    first = text.splitlines()[0] if text else ""
    delim = "\t" if "\t" in first else (";" if first.count(";") > first.count(",") else ",")
    out = []
    for r in csv.DictReader(text.splitlines(), delimiter=delim):
        row = {nh(k): (v or "").strip() for k, v in r.items() if k}
        kw = row.get("keyword") or row.get("mot-cle") or row.get("mot cle") or row.get("requete") or ""
        url = row.get("url") or row.get("page") or ""
        try:
            pos = int(float((row.get("position") or "0").replace(",", ".")))
        except ValueError:
            pos = 0
        if url and kw.lower() == keyword.lower() and (not pos or pos <= top):
            out.append((pos, url))
    return sorted(out)


def pct(values, q):
    if len(values) == 1:
        return values[0]
    return statistics.quantiles(values, n=4, method="inclusive")[{25: 0, 50: 1, 75: 2}[q]]


def r50(x):
    return int(round(x / 50.0) * 50)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--serp")
    src.add_argument("--urls", nargs="+")
    src.add_argument("--html-dir")
    ap.add_argument("--keyword", help="obligatoire avec --serp")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--exclude-domains", default="", help="domaines à ignorer, séparés par des virgules")
    ap.add_argument("--min-words", type=int, default=150,
                    help="en dessous, la page est considérée comme mal extraite et exclue du calcul")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--render", action="store_true", help="lire les pages dans un navigateur (contenu JavaScript)")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()

    if args.serp:
        if not args.keyword:
            sys.exit("--keyword est obligatoire avec --serp")
        targets = load_serp(args.serp, args.keyword, args.top)
        if not targets:
            sys.exit(f"Aucune URL pour « {args.keyword} » dans {args.serp}")
    elif args.urls:
        targets = list(enumerate(args.urls, 1))
    else:
        files = sorted(glob.glob(os.path.join(args.html_dir, "*.htm*")))
        targets = list(enumerate(files, 1))

    excluded = {d.strip().lower().removeprefix("www.") for d in args.exclude_domains.split(",") if d.strip()}
    renderer = Renderer(max(args.timeout, 30)) if args.render and not args.html_dir else None
    rows = []
    for pos, target in targets:
        status, note = "", ""
        if args.html_dir:
            html = open(target, encoding="utf-8", errors="replace").read()
            status = "fichier"
        else:
            host = urlsplit(target).netloc.lower().removeprefix("www.")
            if host in excluded:
                rows.append([pos, target, "exclu", "", "", "", "", "", "domaine exclu"])
                continue
            try:
                status, html = renderer.fetch(target) if renderer else fetch(target, args.timeout)
            except Exception as e:
                rows.append([pos, target, "erreur", "", "", "", "", "", str(e)[:120]])
                continue
        m = analyse(html)
        if m["words"] < args.min_words:
            note = ("contenu trop court : extraction probablement ratée (blocage, consentement)" if renderer
                    else "contenu trop court : extraction probablement ratée (JS, blocage, consentement) — relancer avec --render")
        rows.append([pos, target, status, m["title"], m["h1"], m["words"], m["h2"], m["h3"], note])

    if renderer:
        renderer.close()
    valid = sorted(r[5] for r in rows if isinstance(r[5], int) and not r[8])
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["position", "url", "statut", "title", "h1", "mots_contenu_principal", "nb_h2", "nb_h3", "note"])
        w.writerows(rows)

    lines = [f"Relevé du {date.today().isoformat()} · mot-clé : {args.keyword or '—'}",
             f"Pages analysées : {len(rows)} · prises en compte : {len(valid)}"]
    if valid:
        med, p25, p75 = statistics.median(valid), pct(valid, 25), pct(valid, 75)
        lines += [f"Mots (contenu principal) : min {valid[0]} · P25 {p25:.0f} · médiane {med:.0f} · "
                  f"P75 {p75:.0f} · max {valid[-1]}",
                  f"Fourchette indicative : {r50(p25)}–{r50(p75)} mots [Estimé — médiane de {len(valid)} pages]"]
        if len(valid) < 4:
            lines.append("Attention : moins de 4 pages exploitables, fourchette peu fiable.")
        if p75 > 2.5 * max(p25, 1):
            lines.append("Écart très large entre pages : formats probablement différents. Exclure les pages "
                         "d'un autre format que la page à produire et relancer.")
    else:
        lines.append("Aucune page exploitable : estimer la longueur à partir du plan [Hypothèse].")
    lines.append("Rappel : repère, pas objectif. Ne jamais allonger pour atteindre la fourchette.")
    resume = os.path.splitext(args.output)[0] + "_resume.txt"
    with open(resume, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"Détail : {args.output} · résumé : {resume}")


if __name__ == "__main__":
    main()
