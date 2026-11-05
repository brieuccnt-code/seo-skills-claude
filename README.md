# Pack SEO expert pour Claude Code

5 skills, 8 scripts et des modèles de livrables pour faire de Claude un consultant SEO senior qui travaille selon tes règles.

## Les 5 skills
| Skill | Contenu | Scripts |
|---|---|---|
| `seo-strategie` | Socle, modes création / optimisation, mots-clés, intention, clustering, mapping, cannibalisation, cocon, maillage, Search Console, audit et technique | `kp_clean.py`, `serp_cluster.py`, `gsc_analyze.py`, `link_graph.py`, `rapport.py` |
| `redaction-seo` | Charte de rédaction : style et ton, title ≠ H1, plan, longueur mesurée sur la SERP, livraison, checklist | `serp_length.py` |
| `ux-cro` | UX et conversion sous contrainte SEO, tests A/B sans risque SEO | `ux_snapshot.py`, `capture_zone.py` (Playwright) |
| `audit-digital` | Système d'audit : 8 types (SEO, technique, contenu, UX, CRO, UX/CRO, complet, vérification ciblée), listes de contrôles, données manquantes, compte rendu | (utilise `ux_snapshot.py`, `capture_zone.py` et `rapport.py`) |
| `seo-editorial` | Affiliation et transparence, comparatifs, politiques anti-spam Google, GEO, calendrier saisonnier | — |

Les 4 skills d'expertise sont aussi enregistrées sur le compte Claude (application et claude.ai), sans les scripts.

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
Tout audit ou toute vérification suit la skill `audit-digital` (périmètre strict selon le type demandé) et se termine par un compte rendu HTML dans `deliverables/` : verdict, **✅ ce qui va bien**, **❌ problèmes à régler** triés par priorité, limites. Il s'ouvre d'un double-clic dans le navigateur.

**Preuves visuelles** : seulement pour un problème visuel (texte invisible, bouton caché sur mobile…), avec une capture **ciblée** de la zone, entourée en rouge (`capture_zone.py`). Pas de captures générales de la page. Un problème non visuel se prouve par le code, une valeur ou une URL. Seule exception : la vérification du rendu JavaScript (captures sans JS / après JS).

**Images (audit technique)** : nombre et liste des images de plus de 150 Ko (seuil réglable), hors WebP/AVIF (SVG pour logos et icônes), surdimensionnées, en lazy-loading dans le premier écran ou sans width/height, sur desktop et sur mobile.

## Scripts
| Script | Entrée | Ce qu'il produit |
|---|---|---|
| `seo-strategie/scripts/kp_clean.py` | export Keyword Planner | base normalisée, fourchettes, quasi-doublons, saisonnalité |
| `seo-strategie/scripts/serp_cluster.py` | top 10 SERP par requête (+ volumes) | clusters par recouvrement d'URL, cas limites |
| `seo-strategie/scripts/gsc_analyze.py` | export GSC requête × page (+ période précédente) | gains rapides, CTR faibles, cannibalisation, évolution |
| `seo-strategie/scripts/link_graph.py` | export des liens internes (+ carte du cocon) | orphelines, profondeur, liens obligatoires manquants, liens hors cocon, ancres répétées |
| `redaction-seo/scripts/serp_length.py` | URL du top 10 | longueur du contenu principal, fourchette recommandée (`--render` pour le JavaScript) |
| `ux-cro/scripts/ux_snapshot.py` | URL | captures de travail, contrôles UX, inventaire des images (`images_desktop.csv`, `images_mobile.csv`, `--max-image-kb`), rendu JavaScript (`--js`), comparaison avant/après (`--baseline`) |
| `ux-cro/scripts/capture_zone.py` | URL + texte ou sélecteur CSS | capture ciblée d'un élément entouré en rouge, contraste WCAG mesuré |
| `seo-strategie/scripts/rapport.py` | compte rendu JSON (`templates/compte-rendu.json`) | compte rendu HTML : verdict, captures ciblées, ✅ ce qui va bien / ❌ problèmes à régler |

Les données de `data/` et les livrables de `deliverables/` ne sont jamais envoyés sur GitHub (`.gitignore`).
