---
name: seo-audit
description: Audit SEO complet d'un site existant (technique, contenu, architecture, maillage, mesure) avec problèmes prouvés et plan d'action priorisé. À utiliser pour auditer un site, diagnostiquer une baisse de trafic, faire un état des lieux SEO ou préparer une proposition client. Pour un point technique précis, utiliser technical-seo.
---

# SEO Audit

## Périmètre (à écrire en tête du livrable)
Domaine / sous-domaine / répertoire, pays, langue, appareil, période des données, sources utilisées et **non** utilisées.

## Sources
Crawl, Search Console, analytics si fournis, sitemap, robots.txt, rendu HTML, logs, CrUX/PageSpeed, inspection manuelle.
Lancer `gsc_analyze.py` (skill `seo-measurement`) si un export GSC est disponible, et `link_graph.py` (skill `cocon-semantique`) si un export de liens existe.

## Ordre des contrôles
1. **Indexation et exploration** (via `technical-seo`) : codes HTTP, robots, noindex, canonical, sitemap, duplication, rendu JS.
2. **Architecture et maillage** : profondeur, orphelines, navigation, pagination.
3. **Recherche et intentions** : pages vs clusters, cannibalisation, pages sans rôle.
4. **On-page** : title, H1, structure, meta, images, liens. Détecter les doublons de title/H1 dans le crawl.
5. **Qualité** : utilité, originalité, preuves, fraîcheur pertinente, pages faibles en nombre.
6. **Données structurées** (via `structured-data`).
7. **Performance et mobile** : données terrain d'abord.
7 bis. **UX et conversion** des pages à fort trafic : skill `ux-cro` (sans dégrader le SEO).
8. **Spécifique** : local, e-commerce, international selon le type.
9. **Mesure** : GSC configuré, conversions suivies.

## Règles de preuve
- Chaque problème : preuve, URL(s) d'exemple, nombre d'URL touchées, impact, confiance, effort, risque, recommandation concrète.
- Séparer **confirmé** et **à vérifier**.
- Un sitemap ne prouve pas l'indexation. Un rapport Lighthouse ne prouve pas un problème utilisateur.

## Livrable
`templates/seo-audit.md` + `templates/action-plan.csv` trié. Résumé exécutif en tête : 3 problèmes majeurs, 3 gains rapides, ce qu'il faut pour aller plus loin.
