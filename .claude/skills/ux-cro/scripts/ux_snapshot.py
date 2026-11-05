#!/usr/bin/env python3
"""Captures desktop et mobile + contrôles UX/SEO automatiques d'une ou plusieurs pages (Playwright).

Pré-requis (une fois) :  py -m pip install playwright  puis  py -m playwright install chromium

Pour chaque page et chaque appareil (desktop 1440×900, mobile iPhone 13) :
- captures : premier écran et page entière (PNG) ;
- contrôles : débordement horizontal, zones tactiles trop petites (mobile), images sans
  dimensions (risque CLS), image du premier écran en lazy-loading (risque LCP), texte trop petit
  sur mobile, meta viewport, title, H1, plan des Hn, liens internes, mots du contenu rendu,
  LCP et CLS mesurés en laboratoire (indicatifs, ≠ données terrain CrUX/Search Console).
- --baseline : compare avec un relevé précédent (Hn, liens internes, nombre de mots) pour
  vérifier qu'une modification n'a rien retiré d'important pour le SEO.

Exemples :
  py ux_snapshot.py https://exemple.com/page -o data/clean/ux/2026-11-05
  py ux_snapshot.py https://exemple.com/a https://exemple.com/b -o data/clean/ux/apres --baseline data/clean/ux/avant
Sorties : <dossier>/<page>/{desktop,mobile}_{ecran,complet}.png, rapport.json, et <dossier>/rapport.md
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright n'est pas installé : py -m pip install playwright  puis  py -m playwright install chromium")

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
    title: document.title, viewport_meta: !!document.querySelector('meta[name=viewport]'),
    h1_count: document.querySelectorAll('h1').length, headings, internal_links: [...internal].sort(),
    words, overflow_px: Math.max(0, docW - vw), overflow, small_targets: small.slice(0, 15), small_targets_total: small.length,
    images_no_dimensions: noDims.slice(0, 15), images_no_dimensions_total: noDims.length, lazy_above_fold: lazyFold,
    small_text_blocks: smallText, links_buttons_first_screen: ctas,
    lab_lcp_ms: Math.round(window.__ux.lcp), lab_cls: Math.round(window.__ux.cls * 1000) / 1000,
  };
}
"""


def slug(url):
    p = urlsplit(url)
    s = (p.netloc + p.path).strip("/") or "page"
    return re.sub(r"[^\w.-]+", "_", s)[:80]


def audit(ctx, url, outdir, mobile, timeout, vw):
    page = ctx.new_page()
    page.add_init_script(INIT_JS)
    status = None
    try:
        resp = page.goto(url, wait_until="load", timeout=timeout)
        status = resp.status if resp else None
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        page.screenshot(path=os.path.join(outdir, f"{'mobile' if mobile else 'desktop'}_ecran.png"))
        # défiler pour déclencher le lazy-loading et mesurer les décalages pendant le scroll
        page.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight * 0.8) {
                          window.scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); } window.scrollTo(0, 0); }""")
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(outdir, f"{'mobile' if mobile else 'desktop'}_complet.png"), full_page=True)
        data = page.evaluate(AUDIT_JS, [mobile, vw])
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
                d = audit(ctx, target, pdir, mobile, args.timeout * 1000, opts["viewport"]["width"])
                ctx.close()
                result[name] = d
                report.append(f"### {name.capitalize()}")
                report += [f"- {i}" for i in issues(d, mobile)]
                if "erreur" not in d:
                    report.append(f"- Title : {d['title']!r} · mots du contenu : {d['words']} · liens internes : "
                                  f"{len(d['internal_links'])} · LCP labo : {d['lab_lcp_ms']} ms · CLS labo : {d['lab_cls']}")
                    report.append("- Liens et boutons du premier écran : " + (" | ".join(d["links_buttons_first_screen"]) or "aucun"))
                    report.append(f"- Captures : `{pdir}/{name}_ecran.png`, `{pdir}/{name}_complet.png`")
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
