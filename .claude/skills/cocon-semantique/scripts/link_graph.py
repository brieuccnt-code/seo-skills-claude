#!/usr/bin/env python3
"""Analyse du maillage interne et contrôle d'un cocon sémantique.

--links : export des liens internes (ex. Screaming Frog « All Inlinks »).
          Colonnes reconnues : source, destination (ou target), anchor/ancre,
          type (seuls les liens hypertexte sont gardés), link position/position du lien (optionnel).
--cocon : carte du cocon (templates/cocon-map.csv) : url, cocon, role, parent_url (optionnel).
          role ∈ cible | mere | fille | petite-fille
--home  : URL de l'accueil, pour calculer la profondeur de clic et filtrer les liens externes.

Exemple :
  python link_graph.py --links data/raw/inlinks.csv --cocon deliverables/cocon-map.csv \
      --home https://exemple.com/ -o data/clean/cocon-audit
Sorties : pages.csv, ancres_repetees.csv, et avec --cocon : liens_manquants.csv,
          liens_sortants_hors_cocon.csv
"""
import argparse
import csv
import os
import re
import sys
import unicodedata
from collections import defaultdict, deque
from urllib.parse import urlsplit

# Windows : éviter les erreurs d'affichage des accents et symboles quand la sortie est redirigée
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


CONTENT_POSITIONS = {"content", "contenu", "corps", "body"}


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def nh(h):
    return re.sub(r"\s+", " ", strip_accents((h or "").replace("﻿", "")).strip().lower())


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
    return list(csv.DictReader(lines, delimiter=delim))


def pick(row, *names):
    for k, v in row.items():
        if k is not None and nh(k) in names:
            return (v or "").strip()
    return ""


def norm(u):
    u = (u or "").strip()
    if not u:
        return ""
    if "://" not in u:
        u = "http://" + u.lstrip("/")
    p = urlsplit(u)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host + (p.path.rstrip("/") or "/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--links", required=True)
    ap.add_argument("--cocon")
    ap.add_argument("--home")
    ap.add_argument("--min-sources-anchor", type=int, default=3,
                    help="nombre de pages sources utilisant la même ancre exacte pour la signaler")
    ap.add_argument("-o", "--outdir", required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    home = norm(args.home) if args.home else ""
    home_host = home.split("/")[0] if home else ""

    edges = {}  # (src, dst) -> {"anchors": set, "positions": set}
    has_pos = False
    for r in load(args.links):
        typ = nh(pick(r, "type"))
        if typ and typ not in ("hyperlink", "lien hypertexte", "ahref", "a href", "lien"):
            continue
        src = norm(pick(r, "source", "from", "url source", "page source"))
        dst = norm(pick(r, "destination", "target", "to", "url destination", "cible", "page cible"))
        if not src or not dst or src == dst:
            continue
        if home_host and (src.split("/")[0] != home_host or dst.split("/")[0] != home_host):
            continue
        anchor = pick(r, "anchor", "anchor text", "ancre", "texte d'ancrage")
        pos = nh(pick(r, "link position", "position du lien", "position"))
        has_pos = has_pos or bool(pos)
        e = edges.setdefault((src, dst), {"anchors": set(), "positions": set()})
        if anchor:
            e["anchors"].add(anchor)
        if pos:
            e["positions"].add(pos)
    if not edges:
        sys.exit("Aucun lien interne exploitable : vérifier les colonnes source / destination et --home.")

    out_l, in_l = defaultdict(set), defaultdict(set)
    for s, d in edges:
        out_l[s].add(d)
        in_l[d].add(s)

    cocon = {}
    if args.cocon:
        for r in load(args.cocon):
            u = norm(pick(r, "url"))
            if u:
                cocon[u] = {"cocon": pick(r, "cocon"), "role": nh(pick(r, "role")),
                            "parent": norm(pick(r, "parent_url", "parent", "mere"))}

    depth = {}
    if home:
        depth[home] = 0
        q = deque([home])
        while q:
            u = q.popleft()
            for v in out_l.get(u, ()):
                if v not in depth:
                    depth[v] = depth[u] + 1
                    q.append(v)

    all_pages = set(out_l) | set(in_l) | set(cocon)
    rows = []
    for p in sorted(all_pages, key=lambda x: (-len(in_l.get(x, ())), x)):
        n_in = len(in_l.get(p, ()))
        rows.append([p, n_in, len(out_l.get(p, ())), depth.get(p, "non atteinte" if home else ""),
                     "oui" if n_in == 0 and p != home else "non",
                     cocon.get(p, {}).get("cocon", ""), cocon.get(p, {}).get("role", "")])
    with open(os.path.join(args.outdir, "pages.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["url", "liens_entrants", "liens_sortants", "profondeur", "orpheline", "cocon", "role"])
        w.writerows(rows)

    anchor_src = defaultdict(set)
    for (s, d), e in edges.items():
        for a in e["anchors"]:
            anchor_src[(d, a.strip().lower())].add(s)
    rep = sorted([[d, a, len(srcs), len(in_l[d]), f"{len(srcs) / len(in_l[d]) * 100:.0f} %"]
                  for (d, a), srcs in anchor_src.items() if len(srcs) >= args.min_sources_anchor],
                 key=lambda x: -x[2])
    with open(os.path.join(args.outdir, "ancres_repetees.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["cible", "ancre", "nb_sources", "liens_entrants_cible", "part"])
        w.writerows(rep)

    summary = [f"Liens internes uniques : {len(edges)} · pages : {len(all_pages)}",
               f"Orphelines : {sum(1 for r in rows if r[4] == 'oui')}",
               f"Ancres exactes répétées (≥ {args.min_sources_anchor} sources) : {len(rep)}"]
    if home:
        deep = sum(1 for r in rows if isinstance(r[3], int) and r[3] > 3)
        unreached = sum(1 for r in rows if r[3] == "non atteinte")
        summary.append(f"Pages à plus de 3 clics : {deep} · non atteintes depuis l'accueil : {unreached}")

    if cocon:
        def content_only(e):
            return (not has_pos) or bool(e["positions"] & CONTENT_POSITIONS)

        missing = []
        for u, c in cocon.items():
            par = c["parent"]
            if not par:
                continue
            for s, d, sens in ((par, u, "descendant (parent → enfant)"), (u, par, "montant (enfant → parent)")):
                e = edges.get((s, d))
                if e is None:
                    missing.append([s, d, sens, "absent", c["cocon"]])
                elif not content_only(e):
                    missing.append([s, d, sens, "présent hors contenu seulement : " + ", ".join(sorted(e["positions"])),
                                    c["cocon"]])
        with open(os.path.join(args.outdir, "liens_manquants.csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["source", "cible", "sens", "etat", "cocon"])
            w.writerows(missing)

        cross = []
        for (s, d), e in edges.items():
            if s in cocon and d in cocon and cocon[s]["cocon"] != cocon[d]["cocon"] and content_only(e):
                cross.append([s, cocon[s]["cocon"], d, cocon[d]["cocon"], cocon[d]["role"],
                              " | ".join(sorted(e["anchors"]))])
        with open(os.path.join(args.outdir, "liens_sortants_hors_cocon.csv"), "w", newline="",
                  encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["source", "cocon_source", "cible", "cocon_cible", "role_cible", "ancres"])
            w.writerows(cross)
        summary.append(f"Liens obligatoires manquants ou hors contenu : {len(missing)}")
        summary.append(f"Liens de contenu vers un autre cocon : {len(cross)} (à justifier ou retirer)")
        if not has_pos:
            summary.append("Pas de colonne de position de lien : navigation et contenu ne sont pas distingués.")

    with open(os.path.join(args.outdir, "synthese.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(summary) + "\n")
    print("\n".join(summary))
    print(f"Fichiers écrits dans {args.outdir}")


if __name__ == "__main__":
    main()
