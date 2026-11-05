---
name: technical-seo
description: Diagnostiquer et corriger le SEO technique : exploration, indexation, canonical, redirections, robots.txt, sitemap, rendu JavaScript, Core Web Vitals, migrations. À utiliser pour un problème d'indexation, des pages exclues dans Search Console, une migration ou refonte, ou pour vérifier le code d'un site.
---

# Technical SEO

## Vérifications
- **HTTP** : 4xx, 5xx, chaînes et boucles de redirections, 302 durables qui devraient être des 301.
- **Directives** : robots.txt, meta robots, X-Robots-Tag, cohérence avec le sitemap (aucune URL noindex ou redirigée dans le sitemap).
- **Canonical** : auto-référente sur les pages indexables ; jamais vers une URL en noindex, redirigée ou en 404.
- **Duplication** : paramètres, majuscules, slash final, http/https, www, pagination, facettes, variantes.
- **Rendu** : le contenu principal et les liens sont présents dans le HTML rendu ; comparer source et rendu.
- **Architecture** : profondeur, orphelines, liens crawlables.
- **Performance** : seuils de `references/HEURISTIQUES.md`, données terrain d'abord ; poids des images, polices, JS bloquant.
- **Images** : formats modernes, dimensions déclarées, lazy-loading hors écran initial, alt utiles.
- **International** : hreflang (voir `international-seo`).
- **Logs / budget de crawl** : seulement pour les gros sites ou si des logs sont fournis.

## Lecture des rapports d'indexation Search Console
- « Explorée, actuellement non indexée » : souvent un signal de qualité ou de doublon, pas un bug technique.
- « Détectée, actuellement non indexée » : souvent découverte/priorité de crawl ; vérifier le maillage.
- « Autre page avec balise canonique correcte » : normal si voulu.
- « Doublon, Google a choisi une autre canonique » : vérifier les signaux contradictoires.

## Migration / refonte
Plan obligatoire : inventaire des URL avec leur trafic et leurs backlinks → table de redirections 1:1 → recette en préproduction → bascule → contrôle des 301, du sitemap et de GSC sous 48 h → suivi à 1, 4 et 12 semaines. Tout doit être validé avant exécution.

## Mise en œuvre dans du code
Lire la stack et les conventions avant de modifier. Proposer le changement, le test et le retour arrière. Ne jamais changer robots, canonical, noindex, URL ou redirections à grande échelle sans validation.

## Preuves
Distinguer test local, crawl, données GSC et inspection d'URL. Ne pas promettre l'indexation après une correction.
