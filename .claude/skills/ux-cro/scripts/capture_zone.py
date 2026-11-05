#!/usr/bin/env python3
"""Capture ciblée d'un élément précis d'une page, entouré en rouge : la preuve visuelle d'un problème visuel.

L'élément est désigné par un sélecteur CSS (--selector) ou par un extrait de son texte (--text).
La capture montre l'élément avec une marge autour (--margin), sur desktop (1440 px) ou mobile (iPhone 13).
Pour un élément contenant du texte, le script mesure aussi la couleur du texte, la couleur de fond réelle
et le ratio de contraste WCAG (minimum 4,5:1 pour le texte courant, 3:1 pour le grand texte).

Exemples :
  py capture_zone.py https://exemple.com/ --text "Réserver maintenant" --device mobile -o deliverables/captures/cta-mobile.jpg
  py capture_zone.py https://exemple.com/ --selector "footer .mentions" -o deliverables/captures/footer.jpg
  py capture_zone.py https://exemple.com/ --selector "img.hero" --nth 0 --margin 60 -o deliverables/captures/hero.jpg
"""
import argparse
import json
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright n'est pas installé : py -m pip install playwright  puis  py -m playwright install chromium")

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

INFO_JS = r"""
(el) => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x)); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  let bgEl = el, bg = null, bgImage = false;
  while (bgEl) { const s = getComputedStyle(bgEl);
    if (s.backgroundImage && s.backgroundImage !== 'none') bgImage = true;
    const c = parse(s.backgroundColor); if (c && c.a > 0.5) { bg = c; break; } bgEl = bgEl.parentElement; }
  if (!bg) bg = {r: 255, g: 255, b: 255, a: 1};
  const s = getComputedStyle(el), fg = parse(s.color);
  const text = (el.innerText || el.getAttribute('alt') || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  let ratio = null;
  if (fg && text) { const l1 = lum(fg), l2 = lum(bg); ratio = Math.round(((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)) * 100) / 100; }
  const size = parseFloat(s.fontSize), bold = parseInt(s.fontWeight) >= 700;
  const large = size >= 24 || (bold && size >= 18.66);
  return {tag: el.tagName.toLowerCase(), text, font_size_px: size, bold,
    color: s.color, background: bgImage ? 'image de fond (contraste à vérifier sur la capture)' : `rgb(${bg.r}, ${bg.g}, ${bg.b})`,
    contrast_ratio: bgImage ? null : ratio, contrast_min: large ? 3 : 4.5,
    contrast_ok: (bgImage || ratio === null) ? null : ratio >= (large ? 3 : 4.5)};
}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--selector", help="sélecteur CSS de l'élément")
    g.add_argument("--text", help="extrait du texte visible de l'élément")
    ap.add_argument("--nth", type=int, default=0, help="n-ième élément correspondant (0 = le premier)")
    ap.add_argument("--device", choices=["desktop", "mobile"], default="desktop")
    ap.add_argument("--margin", type=int, default=40, help="marge autour de l'élément, en px")
    ap.add_argument("--no-outline", action="store_true", help="ne pas entourer l'élément")
    ap.add_argument("-o", "--output", required=True, help="fichier .jpg ou .png")
    ap.add_argument("--timeout", type=int, default=45)
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        opts = dict(p.devices["iPhone 13"]) if args.device == "mobile" else {"viewport": {"width": 1440, "height": 900}}
        ctx = browser.new_context(locale="fr-FR", **opts)
        page = ctx.new_page()
        page.goto(args.url, wait_until="load", timeout=args.timeout * 1000)
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        loc = page.locator(args.selector) if args.selector else page.get_by_text(args.text, exact=False)
        count = loc.count()
        if count == 0:
            sys.exit(f"Aucun élément trouvé pour {args.selector or repr(args.text)} sur {args.device}.")
        el = loc.nth(min(args.nth, count - 1))
        el.scroll_into_view_if_needed(timeout=5000)
        # attendre le chargement des images (lazy-loading) dans et autour de l'élément
        try:
            page.wait_for_function("""(e) => [e, ...e.querySelectorAll('img')].filter(i => i.tagName === 'IMG')
                                        .every(i => i.complete && i.naturalWidth > 0)""", arg=el.element_handle(), timeout=8000)
        except Exception:
            pass
        page.wait_for_timeout(400)
        info = el.evaluate(INFO_JS)
        if not args.no_outline:
            el.evaluate("e => { e.style.outline = '3px solid #e5322d'; e.style.outlineOffset = '3px'; }")
        box = el.bounding_box()
        if not box:
            sys.exit("Élément trouvé mais invisible (taille nulle ou masqué) : rien à capturer.")
        vw, vh = page.evaluate("() => [window.innerWidth, window.innerHeight]")
        m = args.margin
        os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
        kw = {"type": "jpeg", "quality": 85} if args.output.lower().endswith((".jpg", ".jpeg")) else {}
        if box["height"] + 2 * m <= vh:
            # l'élément tient dans l'écran : capture de la zone visible, coordonnées de l'écran
            x0, y0 = max(0, box["x"] - m), max(0, box["y"] - m)
            x1, y1 = min(vw, box["x"] + box["width"] + m), min(vh, box["y"] + box["height"] + m)
            page.screenshot(path=args.output, clip={"x": x0, "y": y0, "width": max(1, x1 - x0), "height": max(1, y1 - y0)}, **kw)
        else:
            # élément plus haut que l'écran : capture de l'élément entier
            el.screenshot(path=args.output, **kw)
        browser.close()

    info.update({"url": args.url, "device": args.device, "elements_correspondants": count, "capture": args.output})
    print(json.dumps(info, ensure_ascii=False, indent=1))
    if info.get("contrast_ok") is False:
        print(f"❌ Contraste {info['contrast_ratio']}:1 < {info['contrast_min']}:1 (WCAG AA)")
    elif info.get("contrast_ok"):
        print(f"✅ Contraste {info['contrast_ratio']}:1 ≥ {info['contrast_min']}:1 (WCAG AA)")


if __name__ == "__main__":
    main()
