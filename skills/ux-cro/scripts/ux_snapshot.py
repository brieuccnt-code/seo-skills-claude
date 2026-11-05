#!/usr/bin/env python3
"""Captures desktop et mobile + contrôles UX/SEO automatiques d'une ou plusieurs pages (Playwright).

Pré-requis (une fois) :  py -m pip install playwright  puis  py -m playwright install chromium

Pour chaque page et chaque appareil (desktop 1440×900, mobile iPhone 13) :
- captures : premier écran et page entière (PNG) ;
- contrôles : débordement horizontal, zones tactiles trop petites (mobile), images sans
  dimensions (risque CLS), image du premier écran en lazy-loading (risque LCP), texte trop petit
  sur mobile, meta viewport, title, H1, plan des Hn, liens internes, mots du contenu rendu,
  LCP et CLS mesurés en laboratoire (indicatifs, ≠ données terrain CrUX/Search Console).
- --js : vérifie le rendu JavaScript. Compare la page SANS JavaScript (HTML servi, ce que tout
  robot lit immédiatement) et la page rendue (title, canonical, meta robots, Hn, liens internes, mots)
  et prend des captures desktop et mobile sans JavaScript (desktop_sans_js.jpg, mobile_sans_js.jpg) comme preuves.
- images (toujours) : inventaire des images réellement téléchargées, par appareil : poids, format, dimensions du
  fichier et affichées, premier écran, lazy-loading, ALT → images_desktop.csv, images_mobile.csv ; signale les images
  de plus de --max-image-kb Ko (150 par défaut), hors WebP/AVIF/SVG, surdimensionnées (fichier plus de max(2, DPR) fois
  plus large qu'affiché) et celles du premier écran en lazy-loading.
- --baseline : compare avec un relevé précédent (Hn, liens internes, nombre de mots) pour
  vérifier qu'une modification n'a rien retiré d'important pour le SEO.

Exemples :
  py ux_snapshot.py https://exemple.com/page -o data/clean/ux/2026-11-05
  py ux_snapshot.py https://exemple.com/page -o data/clean/ux/2026-11-05 --js
  py ux_snapshot.py https://exemple.com/a https://exemple.com/b -o data/clean/ux/apres --baseline data/clean/ux/avant
Sorties : <dossier>/<page>/{desktop,mobile}_{ecran,complet}.jpg (+ *_sans_js.jpg avec --js), rapport.json,
et <dossier>/rapport.md. Captures en JPEG pour des comptes rendus légers.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright n'est pas installé : py -m pip install playwright  puis  py -m playwright install chromium")

# Windows : éviter les erreurs d'affichage des accents et symboles quand la sortie est redirigée
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


INIT_JS = """
window.__ux = {lcp: 0, cls: 0};
try {
  new PerformanceObserver(l => { for (const e of l.getEntries()) window.__ux.lcp = e.startTime; })
    .observe({type: 'largest-contentful-paint', buffered: true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__ux.cls += e.value; })
    .observe({type: 'layout-shift', buffered: true});
} catch (e) {}
"""

AUDIT_JS = r"""
([mobile, vwExpected]) => {
  const vw = vwExpected || window.innerWidth, vh = window.innerHeight, host = location.hostname.replace(/^www\./, '');
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; };
  const label = el => {
    let t = el.tagName.toLowerCase();
    if (el.id) t += '#' + el.id; else if (el.classList.length) t += '.' + [...el.classList].slice(0, 2).join('.');
    const txt = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('alt') || '').trim().replace(/\s+/g, ' ');
    return txt ? `${t} « ${txt.slice(0, 40)} »` : t;
  };
  const docW = document.documentElement.scrollWidth;
  const overflow = [];
  if (docW > vw + 1) {
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 && r.width > 0 && vis(el)) overflow.push(`${label(el)} (bord droit ${Math.round(r.right)}px)`);
      if (overflow.length >= 8) break;
    }
  }
  const small = [];
  if (mobile) {
    for (const el of document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, [role=button]')) {
      if (!vis(el)) continue;
      const r = el.getBoundingClientRect();
      const inline = getComputedStyle(el).display === 'inline' && el.closest('p, li, td');
      if (!inline && (r.width < 24 || r.height < 24)) small.push(`${label(el)} (${Math.round(r.width)}×${Math.round(r.height)}px)`);
    }
  }
  const imgs = [...document.images];
  const noDims = imgs.filter(i => vis(i) && !(i.getAttribute('width') && i.getAttribute('height'))
                     && !getComputedStyle(i).aspectRatio.includes('/')).map(i => (i.currentSrc || i.src).split('/').pop().slice(0, 60));
  const lazyFold = imgs.filter(i => i.loading === 'lazy' && i.getBoundingClientRect().top < vh && vis(i))
                       .map(i => (i.currentSrc || i.src).split('/').pop().slice(0, 60));
  let smallText = 0;
  if (mobile) for (const p of document.querySelectorAll('p, li')) {
    if (vis(p) && (p.innerText || '').trim().length > 40 && parseFloat(getComputedStyle(p).fontSize) < 14) smallText++;
  }
  const headings = [...document.querySelectorAll('h1,h2,h3,h4')].filter(vis)
      .map(h => `${h.tagName}: ${(h.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 90)}`);
  const internal = new Set();
  for (const a of document.querySelectorAll('a[href]')) {
    try { const u = new URL(a.href); if (u.hostname.replace(/^www\./, '') === host) internal.add(u.origin + u.pathname); } catch (e) {}
  }
  const main = document.querySelector('main, article') || document.body;
  const words = ((main.innerText || '').match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu) || []).length;
  const ctas = [...document.querySelectorAll('a[href], button')].filter(el => vis(el) && el.getBoundingClientRect().top < vh)
      .map(el => (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ')).filter(t => t).slice(0, 15);
  return {
    canonical: (document.querySelector('link[rel=canonical]') || {}).href || '',
    robots: (document.querySelector('meta[name=robots]') || {}).content || '',
    title: document.title, viewport_meta: !!document.querySelector('meta[name=viewport]'),
    h1_count: document.querySelectorAll('h1').length, headings, internal_links: [...internal].sort(),
    words, overflow_px: Math.max(0, docW - vw), overflow, small_targets: small.slice(0, 15), small_targets_total: small.length,
    images_no_dimensions: noDims.slice(0, 15), images_no_dimensions_total: noDims.length, lazy_above_fold: lazyFold,
    small_text_blocks: smallText, links_buttons_first_screen: ctas,
    lab_lcp_ms: Math.round(window.__ux.lcp), lab_cls: Math.round(window.__ux.cls * 1000) / 1000,
  };
}
"""


WORD = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*|\d+(?:[.,]\d+)*", re.UNICODE)


class RawParse(HTMLParser):
    """Lecture du HTML sans exécution de JavaScript : ce que les robots reçoivent avant le rendu."""
    SKIP = {"script", "style", "noscript", "template", "svg"}

    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.host = base, urlsplit(base).netloc.lower().removeprefix("www.")
        self.title, self.canonical, self.robots = "", "", ""
        self.headings, self.links, self.text = [], set(), []
        self._skip, self._in_title, self._h = 0, False, None
        self._main, self.main_text = 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("main", "article"):
            self._main += 1
        if tag in self.SKIP:
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = urljoin(self.base, a.get("href") or "")
        elif tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots = a.get("content") or ""
        elif tag in ("h1", "h2", "h3", "h4"):
            self._h = [tag.upper(), []]
        elif tag == "a" and a.get("href"):
            u = urlsplit(urljoin(self.base, a["href"]))
            if u.scheme in ("http", "https", "file") and u.netloc.lower().removeprefix("www.") == self.host:
                self.links.add(f"{u.scheme}://{u.netloc}{u.path}")

    def handle_endtag(self, tag):
        if tag in ("main", "article"):
            self._main = max(0, self._main - 1)
        if tag in self.SKIP:
            self._skip = max(0, self._skip - 1)
        elif tag == "title":
            self._in_title = False
        elif self._h and tag == self._h[0].lower():
            txt = " ".join(" ".join(self._h[1]).split())[:90]
            self.headings.append(f"{self._h[0]}: {txt}")
            self._h = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._skip:
            return
        self.text.append(data)
        if self._main:
            self.main_text.append(data)
        if self._h:
            self._h[1].append(data)


def js_check(browser, url, pdir, rendered, timeout, mobile_opts=None):
    """Compare la page sans JavaScript et la page rendue (desktop) ; captures desktop et mobile sans JavaScript.
    Retourne (constats, tableau, données)."""
    ctx = browser.new_context(locale="fr-FR", viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = ctx.new_page()
    try:
        page.goto(url, wait_until="load", timeout=timeout)
        page.screenshot(path=os.path.join(pdir, "desktop_sans_js.jpg"), type="jpeg", quality=78)
        page.screenshot(path=os.path.join(pdir, "desktop_sans_js_complet.jpg"), full_page=True, type="jpeg", quality=60)
        raw_html = page.content()
    except Exception as e:
        ctx.close()
        return [f"❌ Page sans JavaScript non chargée : {str(e)[:200]}"], None, {}
    ctx.close()
    if mobile_opts:
        mctx = browser.new_context(locale="fr-FR", java_script_enabled=False, **mobile_opts)
        mpage = mctx.new_page()
        try:
            mpage.goto(url, wait_until="load", timeout=timeout)
            mpage.screenshot(path=os.path.join(pdir, "mobile_sans_js.jpg"), type="jpeg", quality=78)
        except Exception:
            pass
        mctx.close()
    rp = RawParse(url)
    rp.feed(raw_html)
    raw = {"title": " ".join(rp.title.split()), "canonical": rp.canonical, "robots": rp.robots,
           "headings": rp.headings, "internal_links": sorted(rp.links), "words": len(WORD.findall(" ".join(rp.main_text or rp.text)))}
    rend = {k: rendered.get(k) for k in ("title", "canonical", "robots", "headings", "internal_links", "words")}
    out = []
    missing_h = [h for h in rend["headings"] or [] if h not in raw["headings"]]
    missing_l = sorted(set(rend["internal_links"] or []) - set(raw["internal_links"]))
    rw, ww = raw["words"], rend["words"] or 0
    ratio = rw / ww if ww else 1
    if ratio < 0.8:
        out.append(f"❌ {100 - ratio * 100:.0f} % du texte n'existe qu'après exécution du JavaScript ({rw} mots sans JS, {ww} avec)")
    if missing_h:
        out.append(f"❌ {len(missing_h)} titre(s) absent(s) sans JavaScript : " + " ; ".join(missing_h[:5]))
    if missing_l:
        out.append(f"⚠️ {len(missing_l)} lien(s) interne(s) absent(s) sans JavaScript : " + " ; ".join(missing_l[:5]))
    if (raw["title"] or "") != (rend["title"] or ""):
        out.append(f"⚠️ Title différent sans JavaScript : {raw['title']!r} → {rend['title']!r}")
    if (raw["canonical"] or "") != (rend["canonical"] or ""):
        out.append(f"❌ Canonical différente ou absente sans JavaScript : {raw['canonical'] or '(aucune)'} → {rend['canonical'] or '(aucune)'}")
    if (raw["robots"] or "").lower() != (rend["robots"] or "").lower():
        out.append(f"❌ Meta robots modifiée par JavaScript : {raw['robots'] or '(aucune)'} → {rend['robots'] or '(aucune)'}")
    if not out:
        out.append(f"✅ Contenu, titres, liens, title, canonical et meta robots présents sans JavaScript ({rw} mots sur {ww})")
    table = {"titre": "Rendu JavaScript : page sans JS vs page rendue (desktop)",
             "colonnes": ["Élément", "Sans JavaScript", "Après JavaScript"],
             "lignes": [["Mots du texte", rw, ww], ["Titres H1–H4", len(raw["headings"]), len(rend["headings"] or [])],
                        ["Liens internes", len(raw["internal_links"]), len(rend["internal_links"] or [])],
                        ["Title", raw["title"] or "(aucun)", rend["title"] or "(aucun)"],
                        ["Canonical", raw["canonical"] or "(aucune)", rend["canonical"] or "(aucune)"],
                        ["Meta robots", raw["robots"] or "(aucune)", rend["robots"] or "(aucune)"]]}
    return out, table, {"sans_js": raw, "titres_manquants": missing_h, "liens_manquants": missing_l}


IMG_DOM_JS = r"""
() => {
  const vh = window.innerHeight, out = [];
  const abs = u => { try { const x = new URL(u, location.href); x.hash = ''; return x.href; } catch (e) { return ''; } };
  for (const im of document.images) {
    const r = im.getBoundingClientRect();
    out.push({url: abs(im.currentSrc || im.src), kind: 'img', natural_w: im.naturalWidth, natural_h: im.naturalHeight,
      display_w: Math.round(r.width), display_h: Math.round(r.height), visible: r.width > 0 && r.height > 0,
      first_screen: r.width > 0 && r.top < vh && r.bottom > 0, loading: im.loading || '',
      has_dims: !!(im.getAttribute('width') && im.getAttribute('height')), alt: im.getAttribute('alt')});
  }
  let n = 0;
  for (const el of document.querySelectorAll('body *')) {
    if (n > 400) break;
    const bg = getComputedStyle(el).backgroundImage;
    if (!bg || bg === 'none' || !bg.includes('url(')) continue;
    const m = [...bg.matchAll(/url\(["']?([^"')]+)["']?\)/g)];
    const r = el.getBoundingClientRect();
    for (const x of m) { if (x[1].startsWith('data:')) continue; n++;
      out.push({url: abs(x[1]), kind: 'css', natural_w: 0, natural_h: 0, display_w: Math.round(r.width),
        display_h: Math.round(r.height), visible: r.width > 0 && r.height > 0,
        first_screen: r.width > 0 && r.top < vh && r.bottom > 0, loading: '', has_dims: true, alt: null}); }
  }
  return {dpr: window.devicePixelRatio || 1, images: out};
}
"""

MODERN = {"webp", "avif", "svg"}


def fmt_of(ctype, url):
    c = (ctype or "").split(";")[0].strip().lower()
    m = {"image/webp": "webp", "image/avif": "avif", "image/svg+xml": "svg", "image/jpeg": "jpeg", "image/jpg": "jpeg",
         "image/png": "png", "image/gif": "gif", "image/x-icon": "ico", "image/vnd.microsoft.icon": "ico"}
    if c in m:
        return m[c]
    ext = os.path.splitext(urlsplit(url).path)[1].lower().lstrip(".")
    return {"jpg": "jpeg"}.get(ext, ext or "?")


def image_inventory(responses, dom, max_kb, outfile):
    """Croise les images réellement téléchargées (réseau) et leur affichage (DOM). Écrit un CSV, retourne un résumé."""
    net = {}
    for resp in responses:
        try:
            url = resp.url.split("#")[0]
            if url.startswith("data:") or url in net:
                continue
            try:
                size = len(resp.body())
            except Exception:
                size = (resp.request.sizes() or {}).get("responseBodySize", 0)
            net[url] = {"status": resp.status, "format": fmt_of(resp.headers.get("content-type"), url), "bytes": size}
        except Exception:
            continue
    dpr = dom.get("dpr", 1)
    rows, seen = [], set()
    by_url = {}
    for im in dom.get("images", []):
        by_url.setdefault(im["url"], []).append(im)
    for url, info in net.items():
        uses = by_url.get(url, [])
        vis = [u for u in uses if u["visible"]] or uses
        u0 = max(vis, key=lambda u: u["display_w"]) if vis else {}
        fmt, kb = info["format"], round(info["bytes"] / 1024, 1)
        if fmt == "ico":
            continue
        nat_w, disp_w = u0.get("natural_w", 0), u0.get("display_w", 0)
        first = any(u.get("first_screen") for u in uses)
        flags = []
        if kb > max_kb:
            flags.append(f"plus de {max_kb} Ko")
        if fmt not in MODERN:
            flags.append(f"format {fmt.upper()} (WebP ou AVIF attendu)")
        if nat_w and disp_w and nat_w > max(2, dpr) * disp_w:
            flags.append(f"surdimensionnée ({nat_w} px pour {disp_w} px affichés)")
        if first and any(u.get("loading") == "lazy" for u in uses):
            flags.append("premier écran en lazy-loading")
        if uses and any(u["kind"] == "img" and u["visible"] and not u["has_dims"] for u in uses):
            flags.append("sans width/height")
        rows.append({"url": url, "format": fmt, "poids_ko": kb, "largeur_fichier": nat_w or "", "largeur_affichee": disp_w or "",
                     "premier_ecran": "oui" if first else "non", "type": (u0.get("kind") or "réseau"),
                     "alt": "" if not uses or uses[0]["alt"] is None else uses[0]["alt"][:80], "problemes": " ; ".join(flags)})
        seen.add(url)
    rows.sort(key=lambda x: -x["poids_ko"])
    import csv as _csv
    with open(outfile, "w", newline="", encoding="utf-8-sig") as f:
        w = _csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["url"])
        w.writeheader()
        w.writerows(rows)
    heavy = [r for r in rows if r["poids_ko"] > max_kb]
    old = [r for r in rows if r["format"] not in MODERN]
    over = [r for r in rows if "surdimensionnée" in r["problemes"]]
    lazy_first = [r for r in rows if "premier écran en lazy" in r["problemes"]]
    return {"total": len(rows), "poids_total_ko": round(sum(r["poids_ko"] for r in rows), 1), "seuil_ko": max_kb,
            "lourdes": [(r["url"], r["poids_ko"], r["format"]) for r in heavy],
            "format_ancien": [(r["url"], r["format"], r["poids_ko"]) for r in old],
            "surdimensionnees": [(r["url"], r["largeur_fichier"], r["largeur_affichee"]) for r in over],
            "lazy_premier_ecran": [r["url"] for r in lazy_first], "csv": outfile}


def slug(url):
    p = urlsplit(url)
    s = (p.netloc + p.path).strip("/") or "page"
    return re.sub(r"[^\w.-]+", "_", s)[:80]


def audit(ctx, url, outdir, mobile, timeout, vw, max_kb=150):
    page = ctx.new_page()
    page.add_init_script(INIT_JS)
    responses = []
    page.on("response", lambda r: responses.append(r) if r.request.resource_type == "image" else None)
    status = None
    try:
        resp = page.goto(url, wait_until="load", timeout=timeout)
        status = resp.status if resp else None
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        page.screenshot(path=os.path.join(outdir, f"{'mobile' if mobile else 'desktop'}_ecran.jpg"), type="jpeg", quality=78)
        # défiler pour déclencher le lazy-loading et mesurer les décalages pendant le scroll
        page.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight * 0.8) {
                          window.scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); } window.scrollTo(0, 0); }""")
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(outdir, f"{'mobile' if mobile else 'desktop'}_complet.jpg"), full_page=True,
                        type="jpeg", quality=60)
        data = page.evaluate(AUDIT_JS, [mobile, vw])
        try:
            dom = page.evaluate(IMG_DOM_JS)
            data["images"] = image_inventory(responses, dom, max_kb, os.path.join(
                outdir, f"images_{'mobile' if mobile else 'desktop'}.csv"))
        except Exception as e:
            data["images"] = {"erreur": str(e)[:200]}
    except Exception as e:
        data = {"erreur": str(e)[:300]}
    data["status"] = status
    page.close()
    return data


def issues(d, mobile):
    out = []
    if "erreur" in d:
        return [f"❌ Page non analysée : {d['erreur']}"]
    if d["status"] and d["status"] >= 400:
        out.append(f"❌ Statut HTTP {d['status']}")
    if d["overflow_px"]:
        out.append(f"❌ Débordement horizontal de {d['overflow_px']}px : " + " ; ".join(d["overflow"][:4]))
    if mobile and not d["viewport_meta"]:
        out.append("❌ Pas de balise meta viewport : la page n'est pas adaptée au mobile")
    if d["h1_count"] != 1:
        out.append(f"⚠️ {d['h1_count']} H1 sur la page (1 attendu)")
    if mobile and d["small_targets_total"]:
        out.append(f"⚠️ {d['small_targets_total']} zone(s) tactile(s) < 24px (WCAG 2.5.8) : " + " ; ".join(d["small_targets"][:4]))
    if d["images_no_dimensions_total"]:
        out.append(f"⚠️ {d['images_no_dimensions_total']} image(s) sans width/height (risque CLS) : "
                   + ", ".join(d["images_no_dimensions"][:4]))
    if d["lazy_above_fold"]:
        out.append("⚠️ Image(s) du premier écran en lazy-loading (risque LCP) : " + ", ".join(d["lazy_above_fold"][:3]))
    if mobile and d["small_text_blocks"]:
        out.append(f"⚠️ {d['small_text_blocks']} bloc(s) de texte < 14px sur mobile")
    if d["lab_lcp_ms"] > 2500:
        out.append(f"⚠️ LCP laboratoire {d['lab_lcp_ms']} ms (> 2 500) — à confirmer avec les données terrain")
    if d["lab_cls"] > 0.1:
        out.append(f"⚠️ CLS laboratoire {d['lab_cls']} (> 0,1) — à confirmer avec les données terrain")
    return out or ["✅ Aucun problème détecté par les contrôles automatiques"]


def compare(old, new):
    out = []
    oh, nh = old.get("headings", []), new.get("headings", [])
    lost_h = [h for h in oh if h not in nh]
    lost_l = sorted(set(old.get("internal_links", [])) - set(new.get("internal_links", [])))
    ow, nw = old.get("words", 0), new.get("words", 0)
    if lost_h:
        out.append(f"❌ Titres disparus ({len(lost_h)}) : " + " ; ".join(lost_h[:6]))
    if lost_l:
        out.append(f"❌ Liens internes disparus ({len(lost_l)}) : " + " ; ".join(lost_l[:6]))
    if ow and nw < 0.9 * ow:
        out.append(f"❌ Contenu réduit : {ow} → {nw} mots ({(nw - ow) / ow * 100:.0f} %)")
    elif ow:
        out.append(f"Mots : {ow} → {nw}")
    added = [h for h in nh if h not in oh]
    if added:
        out.append(f"Titres ajoutés ({len(added)}) : " + " ; ".join(added[:4]))
    return out or ["✅ Aucun titre, lien interne ou contenu perdu"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+", help="URL ou fichiers HTML locaux")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--baseline", help="dossier d'un relevé précédent du même script, pour comparaison")
    ap.add_argument("--timeout", type=int, default=45, help="secondes par page")
    ap.add_argument("--max-image-kb", type=int, default=150, help="seuil de poids d'une image en Ko (défaut 150)")
    ap.add_argument("--js", action="store_true", help="vérifier le rendu JavaScript (capture sans JS + comparaison)")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    report = [f"# Relevé UX automatique — {datetime.now():%Y-%m-%d %H:%M}",
              "Mesures de laboratoire (un chargement, une machine) : indicatives. Les Core Web Vitals de référence "
              "sont les données terrain (Search Console, CrUX). Les contrôles ne remplacent pas l'analyse UX.", ""]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        devices = [("desktop", {"viewport": {"width": 1440, "height": 900}}, False),
                   ("mobile", dict(p.devices["iPhone 13"]), True)]
        for url in args.urls:
            target = url if re.match(r"^(https?|file)://", url) else Path(url).resolve().as_uri()
            pdir = os.path.join(args.outdir, slug(target))
            os.makedirs(pdir, exist_ok=True)
            result = {"url": target, "date": datetime.now().isoformat(timespec="seconds")}
            report.append(f"## {target}")
            for name, opts, mobile in devices:
                ctx = browser.new_context(locale="fr-FR", **opts)
                d = audit(ctx, target, pdir, mobile, args.timeout * 1000, opts["viewport"]["width"], args.max_image_kb)
                ctx.close()
                result[name] = d
                report.append(f"### {name.capitalize()}")
                report += [f"- {i}" for i in issues(d, mobile)]
                if "erreur" not in d:
                    report.append(f"- Title : {d['title']!r} · mots du contenu : {d['words']} · liens internes : "
                                  f"{len(d['internal_links'])} · LCP labo : {d['lab_lcp_ms']} ms · CLS labo : {d['lab_cls']}")
                    im = d.get("images") or {}
                    if "erreur" in im:
                        report.append(f"- Images : inventaire impossible ({im['erreur']})")
                    elif im:
                        report.append(f"- Images : {im['total']} téléchargées, {im['poids_total_ko']:.0f} Ko au total · détail : `{im['csv']}`")
                        report.append(f"  - {len(im['lourdes'])} de plus de {im['seuil_ko']} Ko" + (" : " + " ; ".join(
                            f"{u.rsplit('/', 1)[-1][:50]} ({kb:.0f} Ko, {f})" for u, kb, f in im['lourdes'][:15]) if im['lourdes'] else ""))
                        report.append(f"  - {len(im['format_ancien'])} hors WebP/AVIF/SVG" + (" : " + " ; ".join(
                            f"{u.rsplit('/', 1)[-1][:50]} ({f.upper()}, {kb:.0f} Ko)" for u, f, kb in im['format_ancien'][:15]) if im['format_ancien'] else ""))
                        report.append(f"  - {len(im['surdimensionnees'])} surdimensionnée(s)" + (" : " + " ; ".join(
                            f"{u.rsplit('/', 1)[-1][:50]} ({a} px pour {b} px)" for u, a, b in im['surdimensionnees'][:10]) if im['surdimensionnees'] else ""))
                        if im["lazy_premier_ecran"]:
                            report.append("  - Premier écran en lazy-loading : " + " ; ".join(u.rsplit('/', 1)[-1][:50] for u in im["lazy_premier_ecran"]))
                    report.append("- Liens et boutons du premier écran : " + (" | ".join(d["links_buttons_first_screen"]) or "aucun"))
                    report.append(f"- Captures : `{pdir}/{name}_ecran.jpg`, `{pdir}/{name}_complet.jpg`")
            if args.js and "erreur" not in result.get("desktop", {"erreur": 1}):
                found, table, extra = js_check(browser, target, pdir, result["desktop"], args.timeout * 1000, devices[1][1])
                result["js"] = {"constats": found, "tableau": table, **extra}
                report.append("### Rendu JavaScript")
                report += [f"- {i}" for i in found]
                if table:
                    report.append("| " + " | ".join(table["colonnes"]) + " |")
                    report.append("|" + "---|" * len(table["colonnes"]))
                    report += ["| " + " | ".join(str(c) for c in row) + " |" for row in table["lignes"]]
                    report.append(f"- Preuves : `{pdir}/desktop_sans_js.jpg` et `{pdir}/mobile_sans_js.jpg` (sans JavaScript) "
                                  f"à comparer avec `{pdir}/desktop_ecran.jpg` et `{pdir}/mobile_ecran.jpg` (rendu)")
            if args.baseline:
                bfile = os.path.join(args.baseline, slug(target), "rapport.json")
                if os.path.exists(bfile):
                    old = json.load(open(bfile, encoding="utf-8"))
                    report.append("### Comparaison avec le relevé précédent (desktop)")
                    report += [f"- {i}" for i in compare(old.get("desktop", {}), result.get("desktop", {}))]
                else:
                    report.append(f"- Pas de relevé précédent pour cette page dans {args.baseline}")
            with open(os.path.join(pdir, "rapport.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=1)
            report.append("")
        browser.close()

    path = os.path.join(args.outdir, "rapport.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))
    print(f"\nRapport : {path}")


if __name__ == "__main__":
    main()
