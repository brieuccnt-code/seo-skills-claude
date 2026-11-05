# Pack SEO expert pour Claude Code

4 skills, 7 scripts et des modèles de livrables pour faire de Claude un consultant SEO senior qui travaille selon tes règles.

## Les 4 skills
| Skill | Contenu | Scripts |
|---|---|---|
| `seo-strategie` | Socle, modes création / optimisation, mots-clés, intention, clustering, mapping, cannibalisation, cocon, maillage, Search Console, audit et technique | `kp_clean.py`, `serp_cluster.py`, `gsc_analyze.py`, `link_graph.py`, `rapport.py` |
| `redaction-seo` | Charte de rédaction : style et ton, title ≠ H1, plan, longueur mesurée sur la SERP, livraison, checklist | `serp_length.py` |
| `ux-cro` | UX et conversion sous contrainte SEO, tests A/B sans risque SEO | `ux_snapshot.py` (Playwright) |
| `seo-editorial` | Affiliation et transparence, comparatifs, politiques anti-spam Google, GEO, calendrier saisonnier | — |

Les mêmes 4 skills sont enregistrées sur le compte Claude (application et claude.ai), sans les scripts.

## Installation
1. Récupérer le pack : `git clone https://github.com/brieuccnt-code/seo-skills-claude "Nom du projet"`, ou copier le dossier.
2. Le dossier des skills doit s'appeler exactement `.claude` (s'il s'appelle `_claude`, le renommer : `Rename-Item _claude .claude`).
3. Ouvrir un terminal dans le dossier (clic droit → « Ouvrir dans le Terminal ») et lancer `claude`.
4. Python 3.9+ (commande `py` sous Windows). Optionnel : Playwright pour les captures et les sites en JavaScript : `py -m pip install playwright` puis `py -m playwright install chromium`.

## Démarrer un projet
1. Une copie du pack par projet (chaque projet garde ses données et livrables).
2. Remplir `references/CHARTE-EDITORIALE.md`, ou laisser Claude poser les questions au premier contenu.
3. Déposer les exports dans `data/raw/` puis demander en langage naturel : « analyse mon export Search Console », « fais le clustering », « écris un article sur… », « audit UX de cette page ».

## Comptes rendus
Tout audit ou toute vérification (site, page ou point précis comme le rendu JavaScript) se termine par un compte rendu HTML dans `deliverables/` : verdict, captures desktop et mobile, **✅ ce qui va bien**, **❌ problèmes à régler** triés par priorité, limites. Il s'ouvre d'un double-clic dans le navigateur.

## Scripts
| Script | Entrée | Ce qu'il produit |
|---|---|---|
| `seo-strategie/scripts/kp_clean.py` | export Keyword Planner | base normalisée, fourchettes, quasi-doublons, saisonnalité |
| `seo-strategie/scripts/serp_cluster.py` | top 10 SERP par requête (+ volumes) | clusters par recouvrement d'URL, cas limites |
| `seo-strategie/scripts/gsc_analyze.py` | export GSC requête × page (+ période précédente) | gains rapides, CTR faibles, cannibalisation, évolution |
| `seo-strategie/scripts/link_graph.py` | export des liens internes (+ carte du cocon) | orphelines, profondeur, liens obligatoires manquants, liens hors cocon, ancres répétées |
| `redaction-seo/scripts/serp_length.py` | URL du top 10 | longueur du contenu principal, fourchette recommandée (`--render` pour le JavaScript) |
| `ux-cro/scripts/ux_snapshot.py` | URL | captures desktop/mobile, contrôles UX, rendu JavaScript (`--js`), comparaison avant/après (`--baseline`) |
| `seo-strategie/scripts/rapport.py` | compte rendu JSON (`templates/compte-rendu.json`) | compte rendu HTML : verdict, captures, ✅ ce qui va bien / ❌ problèmes à régler |

Les données de `data/` et les livrables de `deliverables/` ne sont jamais envoyés sur GitHub (`.gitignore`).
