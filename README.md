# Pack SEO expert pour Claude Code

6 skills, 8 scripts et des modèles de livrables pour faire de Claude un consultant SEO senior qui travaille selon tes règles.

## Les 6 skills
| Skill | Contenu | Scripts |
|---|---|---|
| `seo-strategie` | Socle, modes création / optimisation, mots-clés, intention, clustering, mapping, cannibalisation, cocon, maillage, Search Console, audit et technique | `kp_clean.py`, `serp_cluster.py`, `gsc_analyze.py`, `link_graph.py`, `rapport.py` |
| `redaction-seo` | Charte de rédaction : style et ton, title ≠ H1, plan, longueur mesurée sur la SERP, livraison, checklist | `serp_length.py` |
| `ux-cro` | UX et conversion sous contrainte SEO, tests A/B sans risque SEO | `ux_snapshot.py`, `capture_zone.py` (Playwright) |
| `audit-digital` | Système d'audit : 8 types (SEO, technique, contenu, UX, CRO, UX/CRO, complet, vérification ciblée), listes de contrôles, données manquantes, compte rendu | (utilise `ux_snapshot.py`, `capture_zone.py` et `rapport.py`) |
| `seo-editorial` | Affiliation et transparence, comparatifs, politiques anti-spam Google, GEO, calendrier saisonnier | — |
| `design-web-seo` | Design et intégration d'une page ou d'un site (création, refonte visuelle) sans dégrader le SEO : système visuel, typo, couleurs, photos, mouvement, gabarit HTML/CSS. S'inspire de Taste Skill (Leonxlnx, MIT) | `assets/gabarit.html`, `assets/base.css` |

Les skills peuvent aussi être enregistrées sur le compte Claude (application et claude.ai), sans les scripts.

## Installation (une seule fois, valable dans tous les dossiers)
Le pack est un **plugin Claude Code**. Dans Claude Code :
```
/plugin marketplace add brieuccnt-code/seo-skills-claude
/plugin install seo-expert@seo-skills-claude
```
Puis quitter (`/exit`) et relancer `claude`. Les skills s'appellent `seo-expert:audit-digital`, `seo-expert:seo-strategie`, etc.

Mise à jour : `/plugin` → onglet des marketplaces → mettre à jour `seo-skills-claude`, ou `claude plugin update seo-expert@seo-skills-claude`, puis relancer Claude Code.

Python 3.9+ (commande `py` sous Windows). Optionnel : Playwright pour les captures et les sites en JavaScript : `py -m pip install playwright` puis `py -m playwright install chromium`.

## Démarrer un projet
1. Un dossier par site (par exemple `Sites\voyageenalbanie`), lancer `claude` dedans.
2. Claude y crée au besoin `data/raw/` (exports bruts), `data/clean/` (sorties des scripts) et `deliverables/` (livrables et comptes rendus).
3. Charte éditoriale : `references/CHARTE-EDITORIALE.md` dans le dossier du site ; Claude la crée à partir du modèle du plugin au premier contenu.
4. Demander en langage naturel : « analyse mon export Search Console », « fais le clustering », « écris un article sur… », « audit technique de https://… ».

## Comptes rendus
Tout audit ou toute vérification suit la skill `audit-digital` (périmètre strict selon le type demandé) et se termine par un compte rendu HTML dans `deliverables/` : verdict, **✅ ce qui va bien**, **❌ problèmes à régler** triés par priorité, limites. Il s'ouvre d'un double-clic dans le navigateur.

**Preuves visuelles** : seulement pour un problème visuel (texte invisible, bouton caché sur mobile…), avec une capture **ciblée** de la zone, entourée en rouge (`capture_zone.py`). Pas de captures générales de la page. Un problème non visuel se prouve par le code, une valeur ou une URL. Seule exception : la vérification du rendu JavaScript (captures sans JS / après JS).

**Images (audit technique)** : nombre et liste des images de plus de 150 Ko (seuil réglable), hors WebP/AVIF (SVG pour logos et icônes), surdimensionnées, en lazy-loading dans le premier écran ou sans width/height, sur desktop et sur mobile.

## Scripts
| Script | Entrée | Ce qu'il produit |
|---|---|---|
| `skills/seo-strategie/scripts/kp_clean.py` | export Keyword Planner | base normalisée, fourchettes, quasi-doublons, saisonnalité |
| `skills/seo-strategie/scripts/serp_cluster.py` | top 10 SERP par requête (+ volumes) | clusters par recouvrement d'URL, cas limites |
| `skills/seo-strategie/scripts/gsc_analyze.py` | export GSC requête × page (+ période précédente) | gains rapides, CTR faibles, cannibalisation, évolution |
| `skills/seo-strategie/scripts/link_graph.py` | export des liens internes (+ carte du cocon) | orphelines, profondeur, liens obligatoires manquants, liens hors cocon, ancres répétées |
| `skills/redaction-seo/scripts/serp_length.py` | URL du top 10 | longueur du contenu principal, fourchette recommandée (`--render` pour le JavaScript) |
| `skills/ux-cro/scripts/ux_snapshot.py` | URL | captures de travail, contrôles UX, inventaire des images (`images_desktop.csv`, `images_mobile.csv`, `--max-image-kb`), rendu JavaScript (`--js`), comparaison avant/après (`--baseline`) |
| `skills/ux-cro/scripts/capture_zone.py` | URL + texte ou sélecteur CSS | capture ciblée d'un élément entouré en rouge, contraste WCAG mesuré |
| `skills/seo-strategie/scripts/rapport.py` | compte rendu JSON (`templates/compte-rendu.json` du plugin) | compte rendu HTML : verdict, captures ciblées, ✅ ce qui va bien / ❌ problèmes à régler |

Les données et livrables restent dans le dossier de chaque site, jamais dans le plugin ni sur GitHub.
