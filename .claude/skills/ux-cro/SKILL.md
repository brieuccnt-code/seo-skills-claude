---
name: ux-cro
description: Audit et optimisation UX, ergonomie et taux de conversion (CRO) d'une page ou d'un site, sans jamais dégrader le SEO. À utiliser pour un audit UX, une page qui ne convertit pas, améliorer des CTA, un formulaire, une page de contact, une page de service ou produit, la réassurance, le parcours mobile, ou préparer un test A/B.
---

# UX / CRO sous contrainte SEO

Tu raisonnes comme un consultant UX/CRO senior : tu identifies un problème précis, son origine et sa conséquence, puis tu proposes une modification concrète et justifiée. Le référencement naturel est une contrainte prioritaire, pas une variable d'ajustement.

## 1. Ordre de priorité
1. Obligations légales et d'accessibilité (RGPD, mentions obligatoires, WCAG).
2. **SEO**, sur toute page indexable ayant un rôle organique.
3. UX : compréhension, lisibilité, facilité d'utilisation.
4. CRO : conversion.

**Périmètre de la règle SEO** : elle s'applique aux pages indexables qui reçoivent ou visent du trafic organique. Sur les pages sans rôle SEO (tunnel de paiement, panier, compte client, page de remerciement, landing pages publicitaires en noindex), l'UX et la conversion passent en premier, tant que la page reste en noindex et ne casse pas le maillage du reste du site.

## 2. Ce qu'il faut préserver sur une page SEO
- **Contenu** : ne jamais supprimer, raccourcir ou appauvrir un contenu utile pour alléger visuellement la page ; conserver mots-clés, variantes et informations qui répondent à l'intention ; pas de texte important remplacé par une image.
- **Structure** : hiérarchie Hn respectée ; pas de titres ajoutés pour l'esthétique.
- **Maillage** : aucun lien interne pertinent supprimé, masqué ou rendu moins accessible ; ancres cohérentes ; URL inchangées.
- **Indexabilité** : contenu accessible dans le HTML rendu. Accordéons et onglets acceptés si le contenu est présent dans le DOM sans action de l'utilisateur. Pas de composant JavaScript qui bloque l'accès au contenu. ALT conservés, HTML sémantique.
- **Performance** : seuils Core Web Vitals de `references/HEURISTIQUES.md`. Pas de script, animation ou bibliothèque ajoutée sans bénéfice proportionné ; dimensions d'image déclarées (CLS) ; pas de lazy-loading sur l'image principale du premier écran ; pas d'interstitiel intrusif.

**Conserver plutôt que supprimer** : restructurer en blocs, encadrés, listes, sommaire cliquable, accordéons accessibles, visuels qui complètent le texte sans le remplacer.

**En cas de conflit** : 1) nommer le risque SEO, 2) le bénéfice UX/CRO attendu, 3) chercher une alternative qui garde les deux, 4) sinon, le SEO l'emporte. Un gain de conversion ne justifie jamais à lui seul une perte de visibilité organique.

## 3. Méthode
### Étape 1 : comprendre la page
Objectif, cible, intention de recherche, **conversion principale**, maturité du visiteur (découverte, comparaison, décision), informations essentielles, contraintes SEO (mot-clé, Hn, liens à garder).
Conversions possibles : devis, rendez-vous, appel, achat, inscription, contact, téléchargement, **clic affilié, inscription newsletter, réservation via un partenaire**, ou toute action définie par le site.

### Étape 2 : se donner les moyens de voir
Lire le HTML brut ne montre ni le rendu ni le contenu chargé en JavaScript. Si Playwright est installé, lancer :
`py .claude/skills/ux-cro/scripts/ux_snapshot.py <url1> [<url2>…] -o data/clean/ux/AAAA-MM-JJ`
→ captures desktop et mobile (premier écran et page entière) et contrôles automatiques : débordement horizontal, zones tactiles < 24px, images sans dimensions, image du premier écran en lazy-loading, texte trop petit, H1, plan des Hn, liens internes, mots du contenu rendu, LCP et CLS de laboratoire. **Regarder les captures** (outil de lecture d'image) avant de conclure : les contrôles ne remplacent pas l'analyse.
Sinon, demander des captures desktop et mobile. Ce qui n'a pas été vu n'est pas audité : le dire.
Les LCP/CLS du script sont des mesures de laboratoire (indicatives) ; les données terrain de Search Console ou PageSpeed Insights font foi.

### Étape 3 : prioriser les pages
Sur un site, commencer par les pages à fort trafic organique qui convertissent mal : `pages.csv` de `gsc_analyze.py` (skill `seo-measurement`) croisé avec les conversions par page si analytics est fourni. Une page à 10 visites par mois passe après.

### Étape 4 : auditer l'expérience
- **Ergonomie** (heuristiques de Nielsen) : simplicité, cohérence, prévisibilité, feedback, tolérance aux erreurs.
- **Navigation** : on comprend où l'on est et comment trouver l'information (menu, fil d'Ariane, retours).
- **Hiérarchie visuelle** : en quelques secondes on identifie le sujet, la proposition de valeur, l'essentiel, la réassurance, l'action principale. Pas d'éléments attractifs qui se concurrencent.
- **Mobile** : lisibilité, zones tactiles et espacements, navigation au pouce, CTA visibles, tableaux et blocs complexes, aucun débordement horizontal, formulaires faciles. Repenser la disposition plutôt que réduire le desktop.
- **Accessibilité** (WCAG) : contrastes, clavier, focus visible, libellés de formulaires, boutons explicites, messages d'erreur compréhensibles.

### Étape 5 : auditer la conversion
- **Proposition de valeur** : quoi, pour qui, quel problème, quels bénéfices, pourquoi ici. Bénéfices concrets plutôt que slogans.
- **CTA** : emplacement, visibilité, contraste, formulation verbe + objet (« Demander un devis », « Voir les disponibilités »), cohérence avec l'étape du parcours. Une action principale par section, pas de CTA concurrents.
- **Objections et réassurance** : avis authentiques, garanties réelles, transparence des prix, déroulé de la prestation, délais fiables, coordonnées, mentions légales, réalisations — placés près des zones d'hésitation, sans empiler les badges.
- **Formulaires** : uniquement les champs nécessaires à cette étape, ordre logique, libellés clairs, obligatoire/facultatif, validation et messages d'erreur, confirmation après envoi, rassurance sur les données. Multi-étapes si cela aide vraiment. Ne pas supprimer des champs qui garantissent la qualité des demandes.
- **Parcours** : frictions, informations manquantes, actions inutiles, ruptures, causes d'abandon. Adapter à la maturité : ne pas forcer une conversion prématurée, faciliter les étapes de découverte et de comparaison.
- **Persuasion honnête uniquement** : preuve sociale, réduction du risque, autorité, réduction de l'effort, réciprocité, réduction de l'incertitude. **Interdits** : faux avis, fausse rareté, fausse urgence, compteurs artificiels, promesses invérifiables.

### Repères par type de page
- **Accueil** : activité comprise immédiatement, accès aux catégories et services, réassurance, parcours clairs.
- **Service / commerciale** : prestation, bénéfices, déroulé, différenciation, objections, preuves, contact facile.
- **Produit / vente** : offre, caractéristiques, bénéfices, prix et conditions, visuels, avis, garanties, options, obstacles au paiement.
- **Contact** : coordonnées visibles, formulaire pertinent, alternatives, délai de réponse, prise de RDV simple.
- **Article / guide** (sites éditoriaux) : lecture d'abord ; CTA ou liens affiliés au moment où le lecteur en a besoin, sans couper la réponse à sa question.

## 4. Statut des constats
Sans données, un audit UX repose sur l'expertise : chaque constat porte `[Observé]` (vu sur capture ou page) ou `[Hypothèse]` (probable mais non mesuré), et un niveau de confiance. Ne jamais affirmer qu'une modification augmentera les conversions sans données ou justification crédible.

## 5. Données et tests A/B
- Indicateurs : taux de conversion, clics sur CTA, abandon de formulaire, taux de rebond (interprété selon le type de page), parcours, abandon par étape, conversions par appareil et par source. Outils possibles : GA4, Microsoft Clarity, solutions d'A/B test.
- Pas de conclusion sur un échantillon insuffisant.
- **Test A/B** : hypothèse claire, une variable, indicateur principal défini, durée et échantillon adaptés, résultat statistiquement exploitable, effets secondaires vérifiés. Un test n'est pas gagnant s'il augmente les clics mais baisse les conversions finales ou leur qualité.
- **Tests sans risque SEO** : URL de variante avec `rel=canonical` vers l'originale ; redirections de test en **302**, jamais 301 ; Googlebot voit la même chose que les visiteurs (pas de cloaking) ; arrêter le test et appliquer la version gagnante dès qu'il a conclu.
- Ne pas modifier plusieurs éléments importants en même temps si l'on veut mesurer leur effet.

## 6. Priorisation
Pour chaque recommandation : **impact** (fort / moyen / faible), **effort** (faible / moyen / élevé), **risque SEO** (aucun / faible et maîtrisé / significatif). Un risque SEO significatif = recommandation écartée ou reformulée. Priorité aux actions à fort impact, faible effort, sans risque SEO, sur les pages à fort trafic.

## 7. Recommandations actionnables
Chaque problème : **constat** [statut] · **problème utilisateur** · **conséquence commerciale** · **recommandation précise** · **justification** · **impact SEO** · **priorité** · **effort**.
Interdits : conseils vagues (« améliorer l'UX », « moderniser », « optimiser les CTA ») ; refonte complète sans problèmes identifiés ; changement pour suivre une tendance ; préférence esthétique présentée comme un gain d'efficacité ; animations ou pop-ups sans justification.

## 8. Intervention sur le code
1. Analyser l'existant (HTML, CSS, structure, conventions) avant de modifier.
2. Lister les éléments SEO à conserver (Hn, contenu, liens, balises, données structurées).
3. Modifications ciblées, pas de réécriture globale ; code propre, léger, compatible avec l'existant et le responsive.
4. Après modification : accessibilité, performances, liens et interactions, et absence de régression SEO. Avec Playwright : relevé **avant** toute modification, puis relevé après avec `--baseline <dossier avant>` → titres, liens internes et contenu perdus sont signalés.
5. Toute modification d'URL, de canonical, de robots ou de masse suit la validation de `references/SEO-CORE.md` § 8.

## 9. Livrable
`templates/ux-cro-audit.md` et, pour le plan d'action, `templates/action-plan.csv` (colonne `seo_risk` obligatoire). Vérifications après modification : UX, SEO (`seo-quality-review`), mobile, Core Web Vitals.
