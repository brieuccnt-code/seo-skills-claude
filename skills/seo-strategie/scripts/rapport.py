#!/usr/bin/env python3
"""Génère le compte rendu HTML d'un audit ou d'une vérification (SEO, UX/CRO, rendu JavaScript, contenu…).

Entrée : un fichier JSON rempli par Claude (modèle : templates/compte-rendu.json).
Sortie : une page HTML autonome (captures intégrées), qui s'ouvre d'un double-clic dans le navigateur.

Structure du compte rendu (skill audit-digital § 5) :
  périmètre → synthèse chiffrée et verdict → preuves visuelles (desktop / mobile) → ✅ ce qui va bien
  → ❌ problèmes à régler (triés par criticité) → tableau des contrôles → niveau de confiance
  → plan d'action → données complémentaires → conclusion → repéré hors périmètre → limites
Tous les champs sont facultatifs sauf le titre : une vérification ciblée n'utilise que les premiers.

Exemple :
  py rapport.py deliverables/2026-11-05_albanie_audit-ux.json -o deliverables/2026-11-05_albanie_audit-ux.html
Les chemins de captures du JSON sont relatifs au dossier du JSON, ou absolus.
"""
import argparse
import base64
import html
import json
import os
import sys
from datetime import date

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PRIO_ORDER = {"haute": 0, "moyenne": 1, "basse": 2}
PRIO_LABEL = {"haute": "Priorité haute", "moyenne": "Priorité moyenne", "basse": "Priorité basse"}

CSS = """
:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e4e3de;--ok:#1f7a4d;--okbg:#e8f5ee;
--ko:#b42318;--kobg:#fdecea;--mid:#b54708;--midbg:#fef3e2;--low:#475467;--lowbg:#eef1f5;--accent:#2f5bd3}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--card:#1e1e1c;--ink:#ecebe6;--muted:#a3a29b;--line:#33322e;
--ok:#6fd3a0;--okbg:#17322a;--ko:#ff8a7a;--kobg:#3a1d1a;--mid:#f5b56b;--midbg:#3a2a14;--low:#b8c2d3;--lowbg:#252a33;--accent:#8aa8ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:1100px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:28px;line-height:1.2;margin:0 0 6px}h2{font-size:21px;margin:40px 0 14px}
.meta{color:var(--muted);font-size:14px}.meta b{color:var(--ink);font-weight:600}
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:24px 0}
.tile{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.tile .n{font-size:30px;font-weight:700;line-height:1}.tile .l{color:var(--muted);font-size:13px;margin-top:6px}
.tile.ok .n{color:var(--ok)}.tile.ko .n{color:var(--ko)}.tile.mid .n{color:var(--mid)}
.verdict{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:14px 18px}
.shots{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px;flex:1 1 230px}
figure.narrow{flex:0 1 170px}figure img{width:100%;height:auto;display:block;border-radius:6px;border:1px solid var(--line)}
figcaption{font-size:13px;color:var(--muted);margin-top:8px}figcaption b{color:var(--ink)}
.item{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:10px 0}
.item h3{font-size:17px;margin:0 0 6px;display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.item p{margin:6px 0}.item .k{color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.03em;margin-right:6px}
.badge{font-size:12px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap}
.b-ok{background:var(--okbg);color:var(--ok)}.b-haute{background:var(--kobg);color:var(--ko)}
.b-moyenne{background:var(--midbg);color:var(--mid)}.b-basse{background:var(--lowbg);color:var(--low)}
.b-st{background:var(--lowbg);color:var(--low)}
.ok-list .item{border-left:4px solid var(--ok)}.ko-list .item.haute{border-left:4px solid var(--ko)}
.ko-list .item.moyenne{border-left:4px solid var(--mid)}.ko-list .item.basse{border-left:4px solid var(--low)}
.item img{max-width:100%;max-height:320px;margin-top:10px;border-radius:6px;border:1px solid var(--line)}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card);border-radius:10px;overflow:hidden}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}th{color:var(--muted);font-weight:600}
ul.plain{padding-left:20px}.empty{color:var(--muted);font-style:italic}
footer{margin-top:48px;color:var(--muted);font-size:13px}
@media print{body{background:#fff}.item,figure,.tile{break-inside:avoid}}
"""


def esc(s):
    return html.escape(str(s or ""))


def img_tag(path, base, alt):
    if not path:
        return ""
    p = path if os.path.isabs(path) else os.path.normpath(os.path.join(base, path))
    if not os.path.exists(p):
        return f'<p class="empty">Capture introuvable : {esc(path)}</p>'
    ext = os.path.splitext(p)[1].lower().lstrip(".") or "png"
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "webp": "webp", "gif": "gif"}.get(ext, "png")
    data = base64.b64encode(open(p, "rb").read()).decode()
    return f'<img alt="{esc(alt)}" src="data:image/{mime};base64,{data}">'


def item_html(it, base, kind):
    prio = (it.get("priorite") or "").lower()
    badges = []
    if kind == "ok":
        badges.append('<span class="badge b-ok">OK</span>')
    elif prio in PRIO_LABEL:
        badges.append(f'<span class="badge b-{prio}">{PRIO_LABEL[prio]}</span>')
    if it.get("statut"):
        badges.append(f'<span class="badge b-st">{esc(it["statut"])}</span>')
    rows = []
    for key, label in (("detail", ""), ("preuve", "Preuve"), ("impact", "Impact"), ("recommandation", "À faire"),
                       ("effort", "Effort"), ("risque_seo", "Risque SEO")):
        if it.get(key):
            lab = f'<span class="k">{label}</span>' if label else ""
            rows.append(f"<p>{lab}{esc(it[key])}</p>")
    img = img_tag(it.get("capture"), base, it.get("titre", ""))
    cls = f"item {prio}" if kind == "ko" else "item"
    return f'<div class="{cls}"><h3>{esc(it.get("titre"))} {" ".join(badges)}</h3>{"".join(rows)}{img}</div>'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("-o", "--output", help="fichier HTML (par défaut : même nom que le JSON)")
    args = ap.parse_args()
    d = json.load(open(args.json, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(args.json))
    out = args.output or os.path.splitext(args.json)[0] + ".html"

    ok = d.get("points_forts", []) or []
    ko = sorted(d.get("problemes", []) or [], key=lambda x: PRIO_ORDER.get((x.get("priorite") or "").lower(), 3))
    n_h = sum(1 for x in ko if (x.get("priorite") or "").lower() == "haute")
    n_m = sum(1 for x in ko if (x.get("priorite") or "").lower() == "moyenne")
    ctrl = d.get("controles", []) or []
    n_nv = sum(1 for c in ctrl if str(c.get("statut", "")).lower().startswith(("non v", "◻", "nv")))

    def ul(items):
        return '<ul class="plain">' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"

    meta = []
    for key, label in (("type", "Type"), ("url", "Page"), ("date", "Date"), ("mode", "Mode")):
        if d.get(key):
            val = f'<a href="{esc(d[key])}">{esc(d[key])}</a>' if key == "url" and str(d[key]).startswith("http") else esc(d[key])
            meta.append(f"<b>{label}</b> : {val}")
    if d.get("sources"):
        meta.append("<b>Sources</b> : " + esc(" · ".join(d["sources"])))

    parts = [f"<h1>{esc(d.get('titre', 'Compte rendu'))}</h1>", f'<div class="meta">{" &nbsp;·&nbsp; ".join(meta)}</div>']
    # 1. Périmètre et état des lieux
    if d.get("perimetre"):
        parts.append(f'<h2>Périmètre et état des lieux</h2><p>{esc(d["perimetre"])}</p>')
    # 2. Synthèse
    parts.append("<h2>Synthèse</h2>")
    tiles = [("ok", len(ok), "points qui vont bien"), ("ko", len(ko), "problèmes à régler"),
             ("ko", n_h, "criticité haute"), ("mid", n_m, "criticité moyenne")]
    if ctrl:
        tiles.append(("", n_nv, "points non vérifiés"))
    parts.append('<div class="summary">' + "".join(
        f'<div class="tile {c}"><div class="n">{n}</div><div class="l">{l}</div></div>' for c, n, l in tiles) + "</div>")
    if d.get("verdict"):
        parts.append(f'<div class="verdict">{esc(d["verdict"])}</div>')
    # 3. Preuves visuelles
    caps = d.get("captures", []) or []
    if caps:
        figs = []
        for c in caps:
            narrow = "mobile" in (c.get("titre", "") + c.get("fichier", "")).lower()
            figs.append(f'<figure class="{"narrow" if narrow else ""}">{img_tag(c.get("fichier"), base, c.get("titre"))}'
                        f'<figcaption><b>{esc(c.get("titre"))}</b>{(" — " + esc(c["legende"])) if c.get("legende") else ""}</figcaption></figure>')
        parts.append('<h2>Preuves visuelles</h2><div class="shots">' + "".join(figs) + "</div>")
    if d.get("tableau"):
        t = d["tableau"]
        head = "".join(f"<th>{esc(h)}</th>" for h in t.get("colonnes", []))
        body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in t.get("lignes", []))
        parts.append(f'<h2>{esc(t.get("titre", "Mesures"))}</h2><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
    # 4-5. Ce qui va bien / problèmes
    parts.append("<h2>✅ Ce qui va bien</h2>")
    parts.append('<div class="ok-list">' + ("".join(item_html(x, base, "ok") for x in ok)
                 or '<p class="empty">Aucun point positif relevé.</p>') + "</div>")
    parts.append("<h2>❌ Problèmes à régler</h2>")
    parts.append('<div class="ko-list">' + ("".join(item_html(x, base, "ko") for x in ko)
                 or '<p class="empty">Aucun problème détecté sur le périmètre vérifié.</p>') + "</div>")
    # 6. Tableau des contrôles
    if ctrl:
        icon = lambda s: ("✅ " if str(s).lower().startswith(("✅", "conforme", "ok")) else
                          "❌ " if str(s).lower().startswith(("❌", "probl")) else
                          "◻️ " if str(s).lower().startswith(("◻", "non v", "nv")) else "") + esc(s).lstrip("✅❌◻️ ")
        rows = "".join(f"<tr><td>{esc(c.get('id'))}</td><td>{esc(c.get('point'))}</td><td>{icon(c.get('statut', ''))}</td>"
                       f"<td>{esc(c.get('note'))}</td></tr>" for c in ctrl)
        parts.append('<h2>Tableau des contrôles</h2><table><thead><tr><th>#</th><th>Point</th><th>Statut</th><th>Note</th></tr>'
                     f"</thead><tbody>{rows}</tbody></table>")
    # 7. Confiance
    if d.get("confiance"):
        parts.append(f'<h2>Niveau de confiance</h2><p>{esc(d["confiance"])}</p>')
    # 8. Plan d'action
    plan = d.get("plan_action") or d.get("prochaines_etapes")
    if plan:
        if isinstance(plan[0], dict):
            rows = "".join(f"<tr><td>{i}</td><td>{esc(a.get('action'))}</td><td>{esc(a.get('priorite'))}</td>"
                           f"<td>{esc(a.get('effort'))}</td><td>{esc(a.get('groupe'))}</td></tr>" for i, a in enumerate(plan, 1))
            parts.append("<h2>Plan d'action priorisé</h2><table><thead><tr><th>#</th><th>Action</th><th>Priorité</th>"
                         f"<th>Effort</th><th>Groupe</th></tr></thead><tbody>{rows}</tbody></table>")
        else:
            parts.append("<h2>Plan d'action priorisé</h2>" + ul(plan))
    # 9-10. Données complémentaires, conclusion
    if d.get("donnees_complementaires"):
        parts.append("<h2>Données complémentaires utiles</h2>" + ul(d["donnees_complementaires"]))
    if d.get("conclusion"):
        parts.append(f'<h2>Conclusion</h2><p>{esc(d["conclusion"])}</p>')
    if d.get("hors_perimetre"):
        parts.append("<h2>🔎 Repéré hors périmètre</h2>" + ul(d["hors_perimetre"]))
    if d.get("limites"):
        parts.append("<h2>Limites et ce qui n'a pas été vérifié</h2>" + ul(d["limites"]))
    parts.append(f"<footer>Compte rendu généré le {date.today().isoformat()}. Statuts : [Mesuré] outil ou fichier · "
                 "[Observé] vu sur la page ou la capture · [Déduit] raisonnement sur des faits cités · [Hypothèse] non vérifié.</footer>")

    page = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{esc(d.get('titre', 'Compte rendu'))}</title><style>{CSS}</style></head><body><main>{''.join(parts)}</main></body></html>")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Compte rendu : {os.path.abspath(out)}  ({len(ok)} points OK, {len(ko)} problèmes dont {n_h} prioritaires, "
          f"{os.path.getsize(out) // 1024} Ko)")


if __name__ == "__main__":
    main()
