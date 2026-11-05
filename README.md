# Pack SEO expert pour Claude Code (v2)

## Installation
0. **Renommer le dossier `_claude` en `.claude`** (dans l'Explorateur, ou en PowerShell depuis ce dossier : `Rename-Item _claude .claude`). Sans ce renommage, Claude Code ne voit pas les skills.
1. Copier ce dossier où tu veux (un dossier par projet client, ou un dossier « atelier » commun).
2. Ouvrir un terminal dans ce dossier et lancer `claude`.
3. `CLAUDE.md` est chargé automatiquement (rôle, socle, conventions) ; les skills de `.claude/skills/` sont détectées toutes seules. Taper `/` dans Claude Code pour les voir.
4. Python 3.9+ pour les scripts (commande `py` sous Windows). Optionnel : Playwright pour les captures et les sites en JavaScript : `py -m pip install playwright` puis `py -m playwright install chromium`.

## Utilisation
- Dépose tes exports dans `data/raw/` (voir `references/DATA-SOURCES.md` pour savoir quoi exporter).
- Demande en langage naturel : « fais le clustering de mes mots-clés Albanie », « analyse mon export GSC », « audite le cocon plages ». La bonne skill se déclenche via sa description.
- Ou appelle une skill directement : `/seo-project-manager`, `/cocon-semantique`, `/ux-cro`…
- Claude identifie d'abord le **mode** : création (rien n'existe) ou optimisation (site existant). Ce mode fixe l'ordre des skills et les interdits.

## Contenu
| Élément | Rôle |
|---|---|
| `CLAUDE.md` | rôle de consultant senior, conventions de dossier, façon de travailler |
| `references/SEO-CORE.md` | principes non négociables (statut des preuves, priorisation, actions risquées) |
| `references/DATA-SOURCES.md` | quels exports fournir, limites de GSC / Keyword Planner / SERP / crawl |
| `references/HEURISTIQUES.md` | seuils de décision (clustering, quick wins, cannibalisation, fusion, CWV) |
| `references/COCON-SEMANTIQUE.md` | méthode cocon : rôles, règles de maillage, ancres |
| `references/CHARTE-EDITORIALE.md` | style, ton et conventions **du projet** : à remplir au démarrage de chaque projet |
| `.claude/skills/` | 23 skills spécialisées, dont `cocon-semantique`, `seo-copywriting` (charte de rédaction) et `ux-cro` |
| `templates/` | modèles CSV et Markdown des livrables |

## Scripts
| Script | Entrée | Ce qu'il produit |
|---|---|---|
| `keyword-research/scripts/kp_clean.py` | export Keyword Planner (FR/EN, UTF-16) | base normalisée, fourchettes, quasi-doublons, saisonnalité |
| `keyword-clustering/scripts/serp_cluster.py` | top 10 SERP par requête (+ volumes) | clusters par recouvrement d'URL, cas limites |
| `seo-measurement/scripts/gsc_analyze.py` | export GSC requête × page (+ période précédente) | quick wins, CTR faibles, cannibalisation, évolution |
| `seo-copywriting/scripts/serp_length.py` | URL du top 10 (fichier SERP, liste ou pages HTML) | longueur du contenu principal par page, fourchette recommandée (`--render` pour les pages en JavaScript) |
| `ux-cro/scripts/ux_snapshot.py` (Playwright) | une ou plusieurs URL | captures desktop/mobile, contrôles UX automatiques, comparaison avant/après (`--baseline`) |
| `cocon-semantique/scripts/link_graph.py` | export des liens internes (+ carte du cocon) | orphelines, profondeur, liens obligatoires manquants, liens hors cocon, ancres répétées |

## Démarrer un projet
1. Copier ou cloner le pack dans un dossier au nom du projet.
2. Remplir `references/CHARTE-EDITORIALE.md` (ou laisser Claude poser les questions au premier contenu).
3. Déposer les exports dans `data/raw/`.

## À personnaliser en priorité
Les seuils de `references/HEURISTIQUES.md` sont des valeurs de départ raisonnables. Remplace-les par **tes** règles de travail : c'est ce qui fera de Claude un expert qui travaille comme toi.
