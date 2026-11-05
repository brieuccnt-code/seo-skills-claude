# Pack SEO expert pour Claude Code (v2)

## Installation
0. **Renommer le dossier `_claude` en `.claude`** (dans l'Explorateur, ou en PowerShell depuis ce dossier : `Rename-Item _claude .claude`). Sans ce renommage, Claude Code ne voit pas les skills.
1. Copier ce dossier où tu veux (un dossier par projet client, ou un dossier « atelier » commun).
2. Ouvrir un terminal dans ce dossier et lancer `claude`.
3. `CLAUDE.md` est chargé automatiquement (rôle, socle, conventions) ; les skills de `.claude/skills/` sont détectées toutes seules. Taper `/` dans Claude Code pour les voir.
4. Python 3.9+ suffit pour les scripts (aucune bibliothèque à installer).

## Utilisation
- Dépose tes exports dans `data/raw/` (voir `references/DATA-SOURCES.md` pour savoir quoi exporter).
- Demande en langage naturel : « fais le clustering de mes mots-clés Albanie », « analyse mon export GSC », « audite le cocon plages ». La bonne skill se déclenche via sa description.
- Ou appelle une skill directement : `/seo-project-manager`, `/cocon-semantique`…

## Contenu
| Élément | Rôle |
|---|---|
| `CLAUDE.md` | rôle de consultant senior, conventions de dossier, façon de travailler |
| `references/SEO-CORE.md` | principes non négociables (statut des preuves, priorisation, actions risquées) |
| `references/DATA-SOURCES.md` | quels exports fournir, limites de GSC / Keyword Planner / SERP / crawl |
| `references/HEURISTIQUES.md` | seuils de décision (clustering, quick wins, cannibalisation, fusion, CWV) |
| `references/COCON-SEMANTIQUE.md` | méthode cocon : rôles, règles de maillage, ancres |
| `.claude/skills/` | 22 skills spécialisées (dont `cocon-semantique`, nouvelle) |
| `templates/` | modèles CSV et Markdown des livrables |

## Scripts
| Script | Entrée | Ce qu'il produit |
|---|---|---|
| `keyword-research/scripts/kp_clean.py` | export Keyword Planner (FR/EN, UTF-16) | base normalisée, fourchettes, quasi-doublons, saisonnalité |
| `keyword-clustering/scripts/serp_cluster.py` | top 10 SERP par requête (+ volumes) | clusters par recouvrement d'URL, cas limites |
| `seo-measurement/scripts/gsc_analyze.py` | export GSC requête × page (+ période précédente) | quick wins, CTR faibles, cannibalisation, évolution |
| `cocon-semantique/scripts/link_graph.py` | export des liens internes (+ carte du cocon) | orphelines, profondeur, liens obligatoires manquants, liens hors cocon, ancres répétées |

## À personnaliser en priorité
Les seuils de `references/HEURISTIQUES.md` sont des valeurs de départ raisonnables. Remplace-les par **tes** règles de travail : c'est ce qui fera de Claude un expert qui travaille comme toi.
