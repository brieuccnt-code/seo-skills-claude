---
name: structured-data
description: Choisir, générer et vérifier des données structurées Schema.org en JSON-LD. À utiliser pour ajouter du balisage schema, viser un résultat enrichi, corriger des erreurs de données structurées dans Search Console, ou baliser Organization, LocalBusiness, Product, Article, Breadcrumb, Event.
---

# Structured Data

1. Identifier le type de page et les entités **visibles** sur la page.
2. Choisir uniquement les types pertinents. Courants : Organization, WebSite, BreadcrumbList, Article/BlogPosting, Product + Offer, LocalBusiness (ou sous-type), Event, Recipe, VideoObject, SoftwareApplication, TouristAttraction/Place.
3. Générer un JSON-LD dont chaque valeur correspond au contenu visible. Relier les entités avec `@id` (ex. `Article.publisher` → `#organization`).
4. Vérifier les propriétés requises et recommandées dans la documentation Google Search Central **actuelle** (elle évolue) et sur schema.org.
5. Tester : test des résultats enrichis de Google et validateur schema.org. Ne jamais écrire « validé » sans test effectué.
6. Documenter l'éligibilité : un balisage valide ne garantit aucun affichage enrichi.

## Interdits
Pas de note, avis, prix ou disponibilité inventés ou invisibles. Pas de FAQPage/HowTo pour viser un affichage qui n'existe plus pour la plupart des sites (voir `references/HEURISTIQUES.md`). Pas de Review sur sa propre entreprise.
