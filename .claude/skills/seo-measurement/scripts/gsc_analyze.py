#!/usr/bin/env python3
"""Analyse d'un export Google Search Console (requête × page, ou pages seules).

Colonnes reconnues (FR/EN) : query/requête, page/url, clicks/clics, impressions, ctr, position.
Le CTR peut être « 3,2 % », « 3.2% » ou 0.032.

Exemple :
  python gsc_analyze.py data/raw/gsc_3m.csv --previous data/raw/gsc_3m_n-1.csv -o data/clean/gsc
Sorties : synthese.txt, pages.csv, gains_rapides_position.csv, ctr_faible.csv,
          cannibalisation.csv (si requête + page), evolution_pages.csv (si --previous)
Seuils : voir references/HEURISTIQUES.md (règles de pratique, ajustables).
"""
import argparse
import csv
import os
import re
import statistics
import sys
import unicodedata
from collections import defaultdict

# Windows : éviter les erreurs d'affichage des accents et symboles quand la sortie est redirigée
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


COLS = {
    "query": ["query", "queries", "top queries", "requete", "requetes", "requetes les plus frequentes"],
    "page": ["page", "pages", "url", "landing page", "top pages", "pages les plus populaires", "adresse"],
    "clicks": ["clicks", "clics", "url clicks"],
    "impressions": ["impressions"],
    "ctr": ["ctr", "url ctr", "site ctr"],
    "position": ["position", "average position", "position moyenne"],
}


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def nh(h):
    return re.sub(r"\s+", " ", strip_accents((h or "").replace("﻿", "")).strip().lower())


def num(s):
    s = (s or "").replace(" ", "").replace(" ", "").replace(" ", "").strip()
    pct = s.endswith("%")
    s = s.rstrip("%")
    if s.count(",") == 1 and "." not in s:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        v = float(s)
    except ValueError:
        return 0.0
    return v / 100 if pct else v


def load(path):
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        text = raw.decode("utf-16")
    else:
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("cp1252")
    lines = text.splitlines()
    first = lines[0] if lines else ""
    delim = "\t" if "\t" in first else (";" if first.count(";") > first.count(",") else ",")
    reader = csv.DictReader(lines, delimiter=delim)
    mapping = {}
    for h in reader.fieldnames or []:
        for key, aliases in COLS.items():
            if nh(h) in aliases and key not in mapping:
                mapping[key] = h
    if "impressions" not in mapping or ("query" not in mapping and "page" not in mapping):
        sys.exit(f"{path} : colonnes requises introuvables. En-têtes lus : {reader.fieldnames}")
    rows = []
    for r in reader:
        d = {
            "query": (r.get(mapping.get("query", ""), "") or "").strip(),
            "page": (r.get(mapping.get("page", ""), "") or "").strip(),
            "clicks": num(r.get(mapping.get("clicks", ""), "0")),
            "impressions": num(r.get(mapping["impressions"], "0")),
            "position": num(r.get(mapping.get("position", ""), "0")),
        }
        if d["impressions"] <= 0:
            continue
        d["ctr"] = d["clicks"] / d["impressions"]
        rows.append(d)
    return rows, mapping


def agg_pages(rows):
    p = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0, "pos_w": 0.0, "queries": 0})
    for r in rows:
        if not r["page"]:
            continue
        a = p[r["page"]]
        a["clicks"] += r["clicks"]
        a["impressions"] += r["impressions"]
        a["pos_w"] += r["position"] * r["impressions"]
        a["queries"] += 1 if r["query"] else 0
    for a in p.values():
        a["position"] = a["pos_w"] / a["impressions"] if a["impressions"] else 0
        a["ctr"] = a["clicks"] / a["impressions"] if a["impressions"] else 0
    return p


def bucket(pos):
    if pos < 1.5:
        return "1"
    if pos < 2.5:
        return "2"
    if pos < 3.5:
        return "3"
    if pos < 5.5:
        return "4-5"
    if pos <= 10.5:
        return "6-10"
    if pos <= 20.5:
        return "11-20"
    return "21+"


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def pct(v):
    return f"{v * 100:.2f} %"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("current")
    ap.add_argument("--previous")
    ap.add_argument("--min-impressions", type=float, default=50)
    ap.add_argument("--cannib-share", type=float, default=0.20,
                    help="part d'impressions minimale de la 2e page (défaut 0.20)")
    ap.add_argument("-o", "--outdir", required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    rows, mapping = load(args.current)
    has_q, has_p = "query" in mapping, "page" in mapping
    unit = "requête × page" if has_q and has_p else ("requête" if has_q else "page")
    sig = [r for r in rows if r["impressions"] >= args.min_impressions]
    tot_c = sum(r["clicks"] for r in rows)
    tot_i = sum(r["impressions"] for r in rows)
    lines = [f"Fichier : {args.current}", f"Granularité : {unit} · {len(rows)} lignes",
             f"Clics : {tot_c:.0f} · Impressions : {tot_i:.0f} · CTR global : {pct(tot_c / tot_i if tot_i else 0)}",
             f"Lignes ≥ {args.min_impressions:.0f} impressions (utilisées pour les diagnostics) : {len(sig)}"]

    # gains rapides position
    qw = []
    if sig:
        q75 = statistics.quantiles([r["impressions"] for r in sig], n=4)[2] if len(sig) >= 4 else 0
        qw = sorted([r for r in sig if 4 <= r["position"] <= 20 and r["impressions"] >= q75],
                    key=lambda r: -r["impressions"])
        lines.append(f"Gains rapides position (pos. 4–20, impressions ≥ {q75:.0f}) : {len(qw)}")
    write(os.path.join(args.outdir, "gains_rapides_position.csv"),
          ["query", "page", "clicks", "impressions", "ctr", "position"],
          [[r["query"], r["page"], int(r["clicks"]), int(r["impressions"]), pct(r["ctr"]),
            round(r["position"], 1)] for r in qw])

    # CTR faible par tranche de position
    by_b = defaultdict(list)
    for r in sig:
        by_b[bucket(r["position"])].append(r)
    med = {b: statistics.median([x["ctr"] for x in v]) for b, v in by_b.items() if len(v) >= 3}
    low = []
    for r in sig:
        b = bucket(r["position"])
        if r["position"] <= 10.5 and b in med and r["ctr"] < 0.5 * med[b]:
            low.append((r, med[b]))
    low.sort(key=lambda x: -x[0]["impressions"])
    write(os.path.join(args.outdir, "ctr_faible.csv"),
          ["query", "page", "impressions", "clicks", "ctr", "ctr_median_tranche", "position", "tranche"],
          [[r["query"], r["page"], int(r["impressions"]), int(r["clicks"]), pct(r["ctr"]), pct(m),
            round(r["position"], 1), bucket(r["position"])] for r, m in low])
    lines.append(f"CTR faibles (< 50 % de la médiane de la tranche, pos. ≤ 10) : {len(low)}")
    lines.append("Médianes de CTR par tranche : " +
                 ", ".join(f"{b} → {pct(med[b])}" for b in ["1", "2", "3", "4-5", "6-10", "11-20", "21+"]
                           if b in med))

    # cannibalisation
    if has_q and has_p:
        byq = defaultdict(list)
        for r in rows:
            byq[r["query"]].append(r)
        can = []
        for q, rs in byq.items():
            total = sum(x["impressions"] for x in rs)
            if len(rs) < 2 or total < args.min_impressions:
                continue
            rs = sorted(rs, key=lambda x: -x["impressions"])
            share2 = rs[1]["impressions"] / total
            if share2 >= args.cannib_share:
                detail = " | ".join(f'{x["page"]} ({int(x["impressions"])} imp, {int(x["clicks"])} clics, '
                                    f'pos {x["position"]:.1f})' for x in rs[:5])
                can.append([q, int(total), len(rs), f"{share2 * 100:.0f} %", detail])
        can.sort(key=lambda x: -x[1])
        write(os.path.join(args.outdir, "cannibalisation.csv"),
              ["query", "impressions_totales", "nb_pages", "part_2e_page", "pages (top 5)"], can)
        lines.append(f"Cannibalisations probables (2e page ≥ {args.cannib_share * 100:.0f} % des impressions) : "
                     f"{len(can)} — à confirmer : intention identique ? alternance dans le temps ?")

    # pages
    if has_p:
        pages = agg_pages(rows)
        write(os.path.join(args.outdir, "pages.csv"),
              ["page", "clicks", "impressions", "ctr", "position_moyenne_ponderee", "nb_requetes"],
              [[p, int(a["clicks"]), int(a["impressions"]), pct(a["ctr"]), round(a["position"], 1), a["queries"]]
               for p, a in sorted(pages.items(), key=lambda x: -x[1]["clicks"])])
        lines.append(f"Pages : {len(pages)}")

        if args.previous:
            prev_rows, pm = load(args.previous)
            if "page" not in pm:
                lines.append("Fichier précédent sans colonne page : évolution non calculée.")
            else:
                prev = agg_pages(prev_rows)
                ev = []
                for p in set(pages) | set(prev):
                    c1, c0 = pages.get(p, {}).get("clicks", 0), prev.get(p, {}).get("clicks", 0)
                    i1, i0 = pages.get(p, {}).get("impressions", 0), prev.get(p, {}).get("impressions", 0)
                    var = (c1 - c0) / c0 if c0 else None
                    ev.append([p, int(c0), int(c1), int(c1 - c0), "" if var is None else f"{var * 100:.0f} %",
                               int(i0), int(i1)])
                ev.sort(key=lambda x: x[3])
                write(os.path.join(args.outdir, "evolution_pages.csv"),
                      ["page", "clics_avant", "clics_apres", "delta_clics", "variation", "imp_avant", "imp_apres"], ev)
                tc0 = sum(a["clicks"] for a in prev.values())
                declin = [e for e in ev if e[1] >= 20 and e[2] <= 0.7 * e[1]]
                lines.append(f"Évolution clics : {tc0:.0f} → {sum(a['clicks'] for a in pages.values()):.0f} · "
                             f"pages en déclin ≥ 30 % (≥ 20 clics avant) : {len(declin)}")
                lines.append("Vérifier que les deux périodes ont la même durée et une saisonnalité comparable.")

    lines.append("Rappel : position = moyenne pondérée par les impressions ; requêtes rares anonymisées par GSC.")
    with open(os.path.join(args.outdir, "synthese.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"Fichiers écrits dans {args.outdir}")


if __name__ == "__main__":
    main()
