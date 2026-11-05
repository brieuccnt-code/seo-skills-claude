---
name: semantic-keyword-expansion
description: Élargir un sujet en longue traîne, questions, entités, champ lexical et sous-thèmes. À utiliser pour trouver des idées de requêtes, des questions d'internautes, des variantes, des entités à couvrir, ou préparer un cocon sémantique. Ne fabrique jamais de volumes : chaque idée est étiquetée mesurée ou hypothèse.
---

# Semantic Keyword Expansion

## Axes d'expansion (passer chaque axe en revue)
1. **Problèmes et questions** : comment, pourquoi, quand, combien, est-ce que…
2. **Publics et contextes** : débutant/expert, famille/solo, budget, saison, situation.
3. **Objets** : produits, services, caractéristiques, lieux, matériaux, compatibilités.
4. **Décision** : prix, coût, devis, avis, comparatif, alternative, « vs », meilleur, avantages/inconvénients.
5. **Parcours** : découverte → évaluation → choix → achat → usage → entretien/après.
6. **Localisation** : seulement si une offre réelle existe dans la zone.
7. **Langue** : synonymes, formes fléchies, vocabulaire métier vs grand public, fautes fréquentes.
8. **Entités** : personnes, lieux, organisations, marques, concepts liés (ce que Google associe au sujet).

## Processus
1. Partir des requêtes GSC et Keyword Planner disponibles dans `data/`.
2. Ajouter les formulations issues de sources fournies : questions clients, avis, forums, suggestions de recherche, « Autres questions posées » relevées.
3. Générer les idées par axe.
4. Étiqueter chacune : `[Mesuré]` (présente dans GSC/KP), `[Observé]` (vue en SERP/suggestion, datée), `[Hypothèse]` (générée).
5. Écarter : redondant, artificiel, hors offre, sans valeur pour le lecteur.
6. Regrouper par besoin : beaucoup d'idées deviennent des **sections** d'une page, pas des pages.
7. Lister les `[Hypothèse]` stratégiques à faire valider dans Keyword Planner (prêtes à coller, une par ligne).

## Interdictions
Aucun volume, tendance, difficulté ou position inventé. Pas de recommandation d'insérer toutes les variantes dans une page. Pas une page par question.

## Livrable
`templates/semantic-expansion.csv` + liste de requêtes à vérifier dans Keyword Planner + entités clés par thème.
