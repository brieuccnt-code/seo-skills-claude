---
name: seo-measurement
description: Analyser les données Google Search Console (et analytics si fournies) : baseline, évolutions, gains rapides, CTR faibles, cannibalisation, pages en déclin, mesure d'impact d'une action. À utiliser pour lire un export GSC, expliquer une baisse ou une hausse, trouver des quick wins, ou faire un reporting SEO.
---

# SEO Measurement

## Analyse automatique d'un export GSC
Fichier attendu : export requête × page (`query,page,clicks,impressions,ctr,position`). Accepte aussi les en-têtes français de GSC.
```
python .claude/skills/seo-measurement/scripts/gsc_analyze.py data/raw/<periode_actuelle>.csv \
  [--previous data/raw/<periode_precedente>.csv] [--min-impressions 50] -o data/clean/gsc
```
Fichiers produits :
- `synthese.txt` : totaux, médianes, comptes par catégorie ;
- `gains_rapides_position.csv` : position 4–20 et fortes impressions ;
- `ctr_faible.csv` : CTR nettement sous la médiane de sa tranche de position ;
- `cannibalisation.csv` : requêtes partagées entre plusieurs pages ;
- `pages.csv` : agrégat par page ;
- `evolution_pages.csv` (si `--previous`) : variation de clics/impressions par page.
Lire `synthese.txt` d'abord, puis les fichiers dans l'ordre utile à la question.

## Interprétation
- Comparer des périodes de même durée, idéalement en glissement annuel.
- Avant d'attribuer une variation à une action du site, éliminer : saisonnalité, mise à jour Google connue, changement de SERP (aperçu IA, pack local…), problème de tracking, changement de périmètre.
- Corrélation ≠ causalité : le dire.
- Keyword Planner = demande estimée, pas trafic obtenu.
- Relier aux conversions uniquement si analytics/CRM sont fournis et fiables.

## Mesurer une action
Avant : baseline des pages concernées (4 semaines minimum). Après : même durée, même jour de semaine de départ, comparée à un groupe de pages non modifiées si possible. Laisser 4 à 8 semaines avant de conclure sur un changement de contenu.

## Livrable
Baseline, période, source, tendances, anomalies, hypothèses explicatives classées par probabilité, actions, métriques de suivi et date de réévaluation.
