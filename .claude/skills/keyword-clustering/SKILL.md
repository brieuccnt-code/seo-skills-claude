---
name: keyword-clustering
description: Regrouper des mots-clés en clusters « une page = un groupe ». À utiliser pour faire un clustering, regrouper des requêtes, décider combien de pages créer, éviter la cannibalisation en amont, ou préparer un cocon sémantique. Utilise le recouvrement de SERP quand il est disponible (script fourni), sinon l'intention.
---

# Keyword Clustering

Principe : deux requêtes vont sur la même page si Google les traite comme le même besoin. Le meilleur indicateur disponible est le **recouvrement des URL dans leurs SERP**.

## Avec des SERP (méthode préférée)
1. Fichier attendu dans `data/raw/` : `keyword,position,url` (top 10 par requête), daté et localisé. Optionnel : volumes (`keyword,avg_monthly_searches` ou `volume_high`, ex. sortie de `kp_clean.py`). Sorties dans `data/clean/clusters/` : `clusters.csv`, `clusters_resume.csv`, `cas_limites.csv`.
2. Lancer :
   `python .claude/skills/keyword-clustering/scripts/serp_cluster.py data/raw/<serp>.csv --volumes data/clean/kp_clean.csv --threshold 3 -o data/clean/clusters`
3. Le script crée les clusters à partir de la requête la plus volumineuse (pivot) et y rattache les requêtes partageant au moins `threshold` URL avec le pivot. Il produit aussi la liste des **cas limites** (recouvrement = seuil − 1) à arbitrer.
4. Relire chaque cluster : un pivot informationnel avec des requêtes transactionnelles = à scinder.
Seuils et arbitrages : `references/HEURISTIQUES.md`.

## Sans SERP
1. Normaliser (casse, accents, pluriels) sans effacer les différences de sens.
2. Regrouper par intention et tâche (skill `search-intent-analysis`), puis par proximité lexicale.
3. Marquer chaque cluster `confiance: faible` et lister les 2 ou 3 requêtes par cluster dont la SERP trancherait.

## Règles de décision
- Un cluster = une page seulement si intention, besoin et format convergent.
- Mots proches ≠ même page (« location voiture Tirana » vs « louer voiture Albanie conseils »).
- Mots différents peuvent partager une page (synonymes, reformulations).
- Une requête très précise sans recouvrement devient souvent une **section** d'une page existante.

## Livrable
CSV : `cluster_id, pivot, keywords, total_volume, intention, type_de_page, serp_observée (oui/non, date), url_cible (existante ou à créer), confiance, risque_cannibalisation` + liste des cas limites + nombre de pages proposées.
