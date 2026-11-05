---
name: cocon-semantique
description: Concevoir ou auditer un cocon sémantique (page cible, mère, filles, sœurs) et son maillage strict. À utiliser pour créer un cocon, structurer un silo, organiser l'arborescence d'un site de contenu, vérifier le maillage d'un cocon existant ou trouver les liens manquants.
---

# Cocon sémantique

Lire d'abord `references/COCON-SEMANTIQUE.md` (vocabulaire, règles de maillage, ancres).

## Concevoir un cocon
1. **Page cible** : la page à faire progresser et sa requête principale.
2. **Intentions amont et latérales** : `semantic-keyword-expansion` à partir de la cible.
3. **Clusters** : `keyword-clustering` (avec SERP si possible). Chaque cluster valide = une page candidate.
4. **Hiérarchie** : du général au précis. 3 à 8 filles par mère. Vérifier qu'un lecteur passerait naturellement de la mère à chaque fille.
5. **Carte** : remplir `templates/cocon-map.csv` (url, cocon, role = cible|mere|fille|petite-fille, parent_url, mots-clés, intention, statut).
6. **Plan de liens** : générer les liens obligatoires (mère↔filles, fille→petites-filles) et proposer les liens sœurs utiles dans `templates/internal-links.csv`, avec ancre et emplacement.
7. **Ordre de production** : pages filles et mère avant ou en même temps que la cible, pour que le cocon soit complet rapidement.

## Auditer un cocon existant
1. Fichiers : carte du cocon (`cocon-map.csv`) + export des liens internes du crawl (`source,destination,anchor`, idéalement avec `link_position`).
2. Lancer :
   `py .claude/skills/cocon-semantique/scripts/link_graph.py --links data/raw/<inlinks>.csv --cocon deliverables/<cocon-map>.csv --home https://exemple.com/ -o data/clean/cocon-audit`
3. Lire les fichiers produits :
   - `liens_manquants.csv` : liens obligatoires absents ;
   - `liens_sortants_hors_cocon.csv` : liens de contenu vers d'autres cocons ;
   - `pages.csv` : liens entrants, profondeur depuis l'accueil, orphelines ;
   - `ancres_repetees.csv` : même ancre exacte utilisée sur beaucoup de sources.
4. Prioriser : liens montants manquants vers la cible > liens mère → filles > orphelines > liens hors cocon > variété des ancres.

## Points d'attention
- Un cocon n'est pas une fin en soi : chaque page doit avoir une utilité réelle.
- Modifier les liens est peu risqué ; modifier les URL ou supprimer des pages exige une validation.
- Ne pas casser la navigation utile aux visiteurs pour « purifier » le cocon.

## Livrable
Carte du cocon, schéma texte de l'arborescence, plan de liens CSV, et pour un audit : liste priorisée des corrections.
