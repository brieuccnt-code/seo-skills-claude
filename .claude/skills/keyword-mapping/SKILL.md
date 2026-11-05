---
name: keyword-mapping
description: Affecter les clusters de mots-clés à des URL existantes ou à créer, et détecter la cannibalisation. À utiliser pour un keyword mapping, savoir quelle page doit cibler quelle requête, repérer deux pages en concurrence, décider de fusionner, ou préparer une arborescence.
---

# Keyword Mapping

## Procédure
1. **Inventaire des URL** : crawl ou sitemap ; pour chacune : fonction, type, intention servie, clics/impressions GSC.
2. **Import** des clusters (`keyword-clustering`) et de leurs intentions.
3. **Affectation** : une URL principale par cluster. Priorité à une URL existante qui a déjà des impressions sur le cluster.
4. **Conflits** : lancer l'analyse de cannibalisation GSC si un export requête × page existe :
   `python .claude/skills/seo-measurement/scripts/gsc_analyze.py data/raw/<gsc>.csv -o data/clean/gsc`
   puis lire `data/clean/gsc/cannibalisation.csv`.
5. **Trous et doublons** : clusters sans page, pages sans rôle SEO, pages à fusionner.
6. **Par URL** : mot-clé principal, secondaires, questions, entités, objectif de conversion.
7. **Décisions** : documenter chaque arbitrage (pourquoi cette URL, pourquoi pas une nouvelle).

## Règles
- Ne pas forcer un mot-clé unique au détriment de la couverture naturelle d'une page.
- Pas deux pages pour le même besoin sans différenciation démontrable.
- Ne pas fusionner deux pages juste parce qu'elles partagent un terme.
- Fusion ou redirection : appliquer les 5 conditions de `references/HEURISTIQUES.md`, puis **validation humaine**.

## Livrable
`templates/keyword-map.csv` + synthèse : conflits (avec preuve), lacunes, pages à créer, fusions proposées (à valider), décisions.
