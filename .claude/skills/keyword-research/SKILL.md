---
name: keyword-research
description: Recherche et qualification de mots-clés. À utiliser pour trouver des mots-clés, exploiter un export Google Keyword Planner ou Search Console, estimer la demande, construire une base de requêtes, ou trier et nettoyer une liste de mots-clés. Produit un CSV qualifié (source, date, pays, intention, pertinence).
---

# Keyword Research

Objectif : une base de requêtes **qualifiée et sourcée**, pas une liste brute.

## 1. Seeds
Partir de l'offre, du vocabulaire réel des clients (avis, emails, FAQ fournis), des pages existantes et des requêtes GSC déjà présentes. 10 à 30 seeds suffisent.

## 2. Collecte
- **Keyword Planner** : déposer l'export dans `data/raw/`, puis le normaliser :
  `py .claude/skills/keyword-research/scripts/kp_clean.py data/raw/<export>.csv -o data/clean/kp_clean.csv --country FR --language fr`
  Le script gère l'UTF-16, les lignes de titre, les fourchettes (« 1 k – 10 k »), les doublons et signale les quasi-doublons (accents, pluriels).
- **Search Console** : requêtes avec impressions = demande réelle observée sur le site [Mesuré].
- **Idées générées** : voir `semantic-keyword-expansion`, toujours marquées [Hypothèse] tant qu'elles ne sont pas mesurées.

## 3. Nettoyage
- Supprimer : hors offre, hors zone, marques concurrentes (sauf stratégie assumée), requêtes absurdes.
- Garder : variantes à intention différente, même à faible volume.
- Regrouper les quasi-doublons signalés par le script, mais garder la trace de chaque forme.

## 4. Qualification (colonnes à remplir)
- `search_intent` : informationnelle, commerciale, transactionnelle, navigationnelle, locale, mixte.
- Pertinence business (1–3) : 3 = mène directement à l'offre.
- Saisonnalité si les volumes mensuels sont disponibles.
- `notes` : ambiguïté, SERP à vérifier, fourchette de volume.

## 5. SERP
Pour les 10 à 20 requêtes stratégiques et les cas ambigus, demander ou relever le top 10 (voir `search-intent-analysis`).

## Règles
- Concurrence Ads ≠ difficulté SEO.
- Un volume est une estimation : afficher la fourchette quand Keyword Planner n'en donne pas plus.
- Volume faible ou nul ≠ absence de demande.
- Pas de projection de trafic sans méthode [Estimé] explicite.

## Livrable
`deliverables/AAAA-MM-JJ_<projet>_keyword-research.csv` au format `templates/keyword-research.csv`, plus une synthèse : 5 à 10 opportunités principales, thèmes couverts, trous, prochaines vérifications.
