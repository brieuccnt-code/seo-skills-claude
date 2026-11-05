---
name: seo-project-manager
description: Point d'entrée de tout projet SEO. À utiliser pour une stratégie SEO globale, un nouveau site, une refonte, un audit transversal, un « par où commencer ? », ou toute demande SEO dont le périmètre n'est pas clair. Cadre le projet, choisit les skills spécialisées, planifie le travail et assemble un plan d'action priorisé.
---

# SEO Project Manager

Tu es l'orchestrateur. Tu ne fais pas le travail des spécialistes à leur place : tu cadres, tu choisis les skills, tu enchaînes leurs livrables et tu tranches les arbitrages.

## Étape 1 : cadrage
Remplir `templates/project-brief.md`. Ne poser que les questions **bloquantes** (en une seule fois, 5 maximum). Pour le reste, poser des hypothèses explicites et avancer.
Questions bloquantes typiques : site nouveau ou existant ? URL ? offre principale ? pays/langue ? conversion prioritaire ? données disponibles ?

## Étape 2 : classifier (plusieurs types possibles)
| Type | Signes | Skills à ajouter |
|---|---|---|
| E-commerce | catalogue, panier, filtres | `ecommerce-seo`, `structured-data` |
| Local | adresse, zone de service, GBP | `local-seo`, `structured-data` |
| Services / vitrine | devis, formulaire, prise de RDV | `content-strategy`, `seo-copywriting` |
| Éditorial / niche / affiliation | articles, comparatifs, monétisation | `editorial-affiliate-seo`, `topical-authority`, `cocon-semantique` |
| International | plusieurs pays ou langues | `international-seo` |
| SaaS | fonctionnalités, intégrations, docs | `content-strategy`, `competitor-analysis` |

## Étape 3 : inventaire des données
Lister ce qui est dans `data/raw/` et ce qui manque, en s'appuyant sur `references/DATA-SOURCES.md`. Pour chaque manque, dire l'export exact à fournir et ce qu'il permettra de décider.

## Étape 4 : plan de travail
**Nouveau site** : `keyword-research` → `semantic-keyword-expansion` → `search-intent-analysis` → `keyword-clustering` → `topical-authority` / `cocon-semantique` → `keyword-mapping` → briefs (`seo-copywriting`) → `internal-linking` → `structured-data` → `seo-quality-review` → `seo-measurement` (baseline).
**Site existant** : `seo-measurement` (baseline GSC) → `seo-audit` + `technical-seo` → gains rapides → `keyword-mapping` (existant vs cible) → corrections → `internal-linking` → suivi.
**Une page** : vérifier l'URL existante, l'intention, le mapping, les pages proches et la SERP avant tout brief.

Annoncer le plan en une liste courte, puis l'exécuter étape par étape. Ne jamais dire qu'une skill a été appliquée si elle n'a pas été lue.

## Étape 5 : livrables
- Résumé exécutif (5 à 10 lignes) : situation, 3 priorités, ce qui manque.
- `templates/action-plan.csv` rempli et trié par priorité (méthode §7 de `references/SEO-CORE.md`).
- Livrables des skills appelées, dans `deliverables/`.
- Hypothèses, données manquantes, date de réévaluation.

## Arbitrages fréquents
- Contenu vs technique : un blocage d'indexation passe toujours avant le contenu.
- Créer vs améliorer : améliorer une page existante qui a déjà des impressions passe avant une nouvelle page.
- Volume vs pertinence : une requête à faible volume mais proche de la conversion passe avant une requête volumineuse hors offre.
