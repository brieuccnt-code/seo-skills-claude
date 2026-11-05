---
name: internal-linking
description: Planifier ou auditer le maillage interne. À utiliser pour trouver des liens internes à ajouter, repérer les pages orphelines ou trop profondes, choisir des ancres, pousser une page stratégique, ou relier des contenus entre eux. Pour un maillage en cocon strict, utiliser aussi cocon-semantique.
---

# Internal Linking

## Procédure
1. Base : mapping des mots-clés et architecture (piliers, pages business, guides).
2. Si un export de liens internes existe, lancer l'analyse de graphe (sans carte de cocon) :
   `py .claude/skills/cocon-semantique/scripts/link_graph.py --links data/raw/<inlinks>.csv --home https://exemple.com/ -o data/clean/links`
   → liens entrants par page, profondeur, orphelines, ancres répétées.
3. **Pages à pousser** : pages business et pages en position 4–20 dans GSC (sortie `gains_rapides_position.csv` de `gsc_analyze.py`).
4. **Pages sources** : pages du même thème avec le plus de clics ou de liens entrants.
5. Proposer des liens **contextuels** (dans le texte, là où le lecteur en a besoin).
6. Ancres : descriptives, variées, cohérentes avec la cible ; pas d'ancre exacte identique répétée partout.
7. Vérifier que les liens sont crawlables (balise `<a href>`, pas de JavaScript seul, pas de nofollow interne).

## Règles
- Pas de liens artificiels entre pages sans rapport.
- Pages stratégiques à 3 clics maximum de l'accueil.
- Pas de modification de centaines de pages sans validation.

## Livrable
`templates/internal-links.csv` : source, cible, ancre suggérée, emplacement (paragraphe ou section), raison, priorité.
