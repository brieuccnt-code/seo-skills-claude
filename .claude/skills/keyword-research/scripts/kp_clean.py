#!/usr/bin/env python3
"""Normalise un export Google Keyword Planner (FR ou EN) vers le format keyword-research.csv.

- Gère UTF-16 / UTF-8 / Windows-1252, tabulation ou virgule/point-virgule, lignes de titre.
- Conserve les volumes tels quels et ajoute volume_low / volume_high (fourchettes « 1 k – 10 k »).
- Supprime les doublons exacts, signale les quasi-doublons (accents, pluriels, ordre des mots).
- Si des colonnes mensuelles existent, calcule le mois de pic et un indice de saisonnalité.

Exemple :
  python kp_clean.py data/raw/kp_export.csv -o data/clean/kp_clean.csv --country FR --language fr
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import date

OUT_COLS = ["keyword", "source", "date", "country", "language", "avg_monthly_searches",
            "volume_low", "volume_high", "competition", "competition_index",
            "top_of_page_bid_low", "top_of_page_bid_high", "peak_month", "seasonality_index",
            "search_intent", "notes"]

ALIASES = {
    "keyword": ["keyword", "mot cle", "mot-cle", "mots cles", "mots-cles"],
    "avg": ["avg. monthly searches", "avg monthly searches", "nombre moyen de recherches mensuelles",
            "recherches mensuelles moyennes", "volume de recherche mensuel moyen"],
    "competition": ["competition", "concurrence"],
    "index": ["competition (indexed value)", "indice de concurrence", "indice de la concurrence",
              "concurrence (valeur indexee)"],
    "bid_low": ["top of page bid (low range)", "enchere en haut de page (plage basse)",
                "enchere en haut de page (fourchette basse)"],
    "bid_high": ["top of page bid (high range)", "enchere en haut de page (plage haute)",
                 "enchere en haut de page (fourchette haute)"],
}
MONTHLY_PREFIXES = ("searches:", "searches :", "recherches:", "recherches :", "recherches mensuelles:",
                    "recherches mensuelles :")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm_header(h):
    return re.sub(r"\s+", " ", strip_accents(h.replace("﻿", "")).strip().lower())


def read_text(path):
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def read_table(path):
    text = read_text(path)
    lines = text.splitlines()
    # trouver la ligne d'en-tête : première ligne contenant un alias de "keyword"
    start = 0
    for i, line in enumerate(lines[:20]):
        cells = [norm_header(c).strip('"') for c in re.split(r"[\t;,]", line)]
        if len(cells) >= 3 and any(c in ALIASES["keyword"] for c in cells):
            start = i
            break
    body = "\n".join(lines[start:])
    sample = lines[start] if lines else ""
    delim = "\t" if "\t" in sample else (";" if sample.count(";") > sample.count(",") else ",")
    reader = csv.reader(io.StringIO(body), delimiter=delim)
    rows = [r for r in reader if any(c.strip() for c in r)]
    if not rows:
        sys.exit("Fichier vide ou illisible.")
    return rows[0], rows[1:]


def find_col(headers, key):
    nh = [norm_header(h) for h in headers]
    for alias in ALIASES[key]:
        if alias in nh:
            return nh.index(alias)
    return None


def to_number(s):
    """'1 200' -> 1200 ; '1,5 k' -> 1500 ; '1,23 €' -> 1.23 ; '' -> None"""
    if s is None:
        return None
    s = s.replace(" ", " ").replace(" ", " ").strip().lower()
    if not s or s in ("-", "--", "n/a"):
        return None
    mult = 1
    m = re.search(r"(k|m|md)\s*$", s)
    if m:
        mult = {"k": 1_000, "m": 1_000_000, "md": 1_000_000_000}[m.group(1)]
        s = s[: m.start()]
    s = re.sub(r"[^\d,.\-]", "", s)
    if s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        v = float(s) * mult
    except ValueError:
        return None
    return int(v) if v.is_integer() else round(v, 2)


def parse_volume(s):
    """Retourne (low, high). Fourchette '1 k – 10 k' ou valeur simple."""
    if not s or not s.strip():
        return None, None
    parts = re.split(r"\s*[–—-]\s*(?=\d)", s.strip())
    if len(parts) == 2:
        return to_number(parts[0]), to_number(parts[1])
    v = to_number(s)
    return v, v


def near_key(kw):
    k = strip_accents(kw.lower())
    k = re.sub(r"[^\w\s]", " ", k)
    words = []
    for w in k.split():
        if len(w) > 3 and w[-1] in "sx":
            w = w[:-1]
        words.append(w)
    return " ".join(sorted(words))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--country", default="")
    ap.add_argument("--language", default="")
    ap.add_argument("--date", default=date.today().isoformat(), help="date de l'export (AAAA-MM-JJ)")
    args = ap.parse_args()

    headers, rows = read_table(args.input)
    idx = {k: find_col(headers, k) for k in ALIASES}
    if idx["keyword"] is None:
        sys.exit(f"Colonne mot-clé introuvable. En-têtes lus : {headers}")
    monthly = [(i, h) for i, h in enumerate(headers) if norm_header(h).startswith(MONTHLY_PREFIXES)]

    def cell(r, k):
        i = idx[k]
        return r[i].strip() if i is not None and i < len(r) else ""

    seen, out, near = set(), [], {}
    dup_exact = 0
    for r in rows:
        kw = cell(r, "keyword")
        if not kw:
            continue
        kwl = re.sub(r"\s+", " ", kw.lower())
        if kwl in seen:
            dup_exact += 1
            continue
        seen.add(kwl)
        avg = cell(r, "avg")
        low, high = parse_volume(avg)
        peak, season = "", ""
        if monthly:
            vals = [(h, to_number(r[i]) if i < len(r) else None) for i, h in monthly]
            vals = [(h, v) for h, v in vals if v is not None]
            if vals:
                mean = sum(v for _, v in vals) / len(vals)
                h, v = max(vals, key=lambda x: x[1])
                peak = re.split(r":\s*", h, maxsplit=1)[-1].strip()
                season = round(v / mean, 2) if mean else ""
        notes = []
        if low is not None and high is not None and low != high:
            notes.append("volume en fourchette (compte sans dépense active ?)")
        nk = near_key(kw)
        if nk in near:
            notes.append(f"quasi-doublon de « {near[nk]} »")
        else:
            near[nk] = kw
        out.append({
            "keyword": kw, "source": "Google Keyword Planner", "date": args.date,
            "country": args.country, "language": args.language, "avg_monthly_searches": avg,
            "volume_low": "" if low is None else low, "volume_high": "" if high is None else high,
            "competition": cell(r, "competition"), "competition_index": cell(r, "index"),
            "top_of_page_bid_low": to_number(cell(r, "bid_low")) or "",
            "top_of_page_bid_high": to_number(cell(r, "bid_high")) or "",
            "peak_month": peak, "seasonality_index": season, "search_intent": "",
            "notes": " ; ".join(notes),
        })

    out.sort(key=lambda d: -d["volume_high"] if isinstance(d["volume_high"], (int, float)) else 1)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLS)
        w.writeheader()
        w.writerows(out)

    n_near = sum(1 for d in out if "quasi-doublon" in d["notes"])
    missing = [k for k, v in idx.items() if v is None]
    print(f"{len(out)} mots-clés écrits dans {args.output}")
    print(f"Doublons exacts supprimés : {dup_exact} · quasi-doublons signalés : {n_near}")
    print(f"Colonnes mensuelles détectées : {len(monthly)}")
    if missing:
        print(f"Colonnes absentes de l'export : {', '.join(missing)}")


if __name__ == "__main__":
    main()
