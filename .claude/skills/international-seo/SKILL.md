---
name: international-seo
description: SEO international et multilingue : choix ccTLD / sous-domaine / sous-répertoire, hreflang, localisation des contenus, ciblage pays. À utiliser pour traduire ou décliner un site dans d'autres langues ou pays, corriger des erreurs hreflang, ou lancer un nouveau marché.
---

# International SEO

## Cadrage
Pays, langues, offres réellement disponibles, devise, livraison, support, réglementation. Ne pas traduire mécaniquement une stratégie française : refaire la recherche de mots-clés par marché.

## Architecture
| Option | Pour | Contre |
|---|---|---|
| ccTLD (.de, .es) | signal pays fort | autorité à reconstruire, coûts |
| Sous-répertoire (/de/) | autorité partagée, simple | signal pays plus faible |
| Sous-domaine (de.) | séparation technique | autorité moins partagée |
Par défaut : sous-répertoires, sauf contrainte business ou légale.

## Hreflang
- Réciprocité obligatoire entre versions équivalentes ; chaque page se cite elle-même.
- Codes valides : langue ISO 639-1, pays ISO 3166-1 alpha-2 (`en-GB` et non `en-UK`, `fr-BE` pour la Belgique).
- `x-default` pour la page de choix ou la version par défaut.
- Uniquement vers des URL canoniques, indexables, en 200.
- Ne pas relier des pages non équivalentes.

## Localisation
Vocabulaire local, intentions, unités, prix, exemples, mentions légales, preuves locales. Relecture par un locuteur compétent.

## Mesure
GSC segmenté par pays et par répertoire. Ne pas additionner des marchés différents.
