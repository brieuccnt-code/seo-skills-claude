#!/usr/bin/env python3
"""Clustering de mots-clés par recouvrement de SERP (méthode « pivot »).

Entrée : CSV avec au moins keyword, position, url (top 10 organique par requête).
         En-têtes FR acceptés : mot-clé / mot clé, position, url / URL.
Volumes (optionnel) : CSV avec keyword + avg_monthly_searches ou volume_high
         (ex. sortie de kp_clean.py). Le volume sert à choisir les pivots.

Algorithme : les requêtes sont triées par volume décroissant. La première requête non
affectée devient pivot ; toute requête non affectée qui partage au moins --threshold URL
avec le pivot rejoint son cluster. On recommence jusqu'à épuisement.
Les requêtes à (threshold - 1) URL communes d'un pivot sans y être rattachées sont listées
comme cas limites à arbitrer.

Exemple :
  python serp_cluster.py data/raw/serp.csv --volumes data/clean/kp_clean.csv --threshold 3 -o data/clean/clusters
Sorties (dans le dossier -o) : clusters.csv, clusters_resume.csv, cas_limites.csv
"""
import argparse
import csv
import os
import re
import sys
import unicodedata
from collections import defaultdict
from urllib.parse import urlsplit

# Windows : éviter les erreurs d'affichage des accents et symboles quand la sortie est redirigée
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass



def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def nh(h):
    return strip_accents(h.replace("﻿", "")).strip().lower()


def open_csv(path):
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        text = raw.decode("utf-16")
    else:
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("cp1252")
    first = text.splitlines()[0] if text else ""
    delim = "\t" if "\t" in first else (";" if first.count(";") > first.count(",") else ",")
    return list(csv.DictReader(text.splitlines(), delimiter=delim))


def pick(row, *names):
    for k, v in row.items():
        if k is not None and nh(k) in names:
            return (v or "").strip()
    return ""


def norm_url(u):
    u = u.strip()
    if not u:
        return ""
    if "://" not in u:
        u = "http://" + u
    p = urlsplit(u)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/") or "/"
    return host + path


def to_num(s):
    s = (s or "").replace(" ", "").replace(" ", "")
    m = re.findall(r"[\d.,]+", s)
    if not m:
        return 0
    v = m[-1].replace(",", ".") if m[-1].count(",") == 1 and "." not in m[-1] else m[-1].replace(",", "")
    try:
        mult = 1000 if s.lower().endswith("k") else 1
        return float(v) * mult
    except ValueError:
        return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serp")
    ap.add_argument("--volumes")
    ap.add_argument("--threshold", type=int, default=3)
    ap.add_argument("--top", type=int, default=10, help="nombre de positions prises en compte")
    ap.add_argument("-o", "--outdir", required=True)
    args = ap.parse_args()

    serps = defaultdict(set)
    display = {}
    for r in open_csv(args.serp):
        kw = pick(r, "keyword", "mot-cle", "mot cle", "requete", "query")
        url = pick(r, "url", "page", "link")
        pos = to_num(pick(r, "position", "rank", "rang"))
        if not kw or not url or (pos and pos > args.top):
            continue
        key = kw.lower()
        display.setdefault(key, kw)
        serps[key].add(norm_url(url))
    if not serps:
        sys.exit("Aucune ligne exploitable : vérifier les colonnes keyword, position, url.")

    vol = {}
    if args.volumes:
        for r in open_csv(args.volumes):
            kw = pick(r, "keyword", "mot-cle", "mot cle")
            v = pick(r, "volume_high") or pick(r, "avg_monthly_searches", "volume", "search volume")
            if kw:
                vol[kw.lower()] = to_num(v)

    order = sorted(serps, key=lambda k: (-vol.get(k, 0), k))
    assigned = {}
    clusters = []
    for k in order:
        if k in assigned:
            continue
        cid = len(clusters) + 1
        members = [(k, len(serps[k]))]
        assigned[k] = cid
        for other in order:
            if other in assigned:
                continue
            ov = len(serps[k] & serps[other])
            if ov >= args.threshold:
                assigned[other] = cid
                members.append((other, ov))
        clusters.append((cid, k, members))

    edge, seen_pairs = [], set()
    pivots = {pivot for _, pivot, _ in clusters}
    for cid, pivot, members in clusters:
        mset = {m for m, _ in members}
        for other in order:
            if other in mset:
                continue
            pair = frozenset((pivot, other))
            if other in pivots and pair in seen_pairs:
                continue
            ov = len(serps[pivot] & serps[other])
            if ov == args.threshold - 1 and ov > 0:
                seen_pairs.add(pair)
                edge.append((display[other], assigned[other], cid, display[pivot], ov))

    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, "clusters.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["cluster_id", "pivot", "keyword", "is_pivot", "urls_communes_avec_pivot", "volume"])
        for cid, pivot, members in clusters:
            for m, ov in members:
                w.writerow([cid, display[pivot], display[m], "oui" if m == pivot else "non",
                            ov, vol.get(m, "")])
    with open(os.path.join(args.outdir, "clusters_resume.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["cluster_id", "pivot", "nb_keywords", "volume_total", "keywords"])
        for cid, pivot, members in clusters:
            w.writerow([cid, display[pivot], len(members),
                        int(sum(vol.get(m, 0) for m, _ in members)) or "",
                        " | ".join(display[m] for m, _ in members)])
    with open(os.path.join(args.outdir, "cas_limites.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["keyword", "cluster_actuel", "cluster_proche", "pivot_proche", "urls_communes"])
        w.writerows(edge)

    singles = sum(1 for _, _, m in clusters if len(m) == 1)
    print(f"{len(serps)} requêtes → {len(clusters)} clusters ({singles} requêtes isolées), seuil = {args.threshold}")
    print(f"Cas limites à arbitrer : {len(edge)}")
    if not vol:
        print("Sans volumes : pivots choisis par ordre alphabétique. Fournir --volumes pour de meilleurs pivots.")
    print(f"Fichiers écrits dans {args.outdir}")


if __name__ == "__main__":
    main()
