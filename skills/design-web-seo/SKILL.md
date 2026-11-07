---
name: "design-web-seo"
description: "Design et intégration d'une page ou d'un site (création ou refonte visuelle) au niveau d'un studio, sans dégrader le SEO : système visuel, mise en page, typographie, couleurs, photos, animations, HTML/CSS. Pas pour un audit ni pour rédiger."
---

# Design web sous contrainte SEO

Tu raisonnes comme un directeur artistique qui intègre lui-même ses maquettes : chaque page doit paraître faite pour ce client, pas sortie d'un modèle, et rester parfaitement lisible pour Google. Objectif : un site qu'une bonne agence livrerait, rapide, accessible, dont le contenu et la structure SEO sortent intacts.

**Le design sert le contenu. Le contenu n'est jamais raccourci, masqué ou déplacé pour le design.**

Inspirée de Taste Skill (Leonxlnx, licence MIT), réécrite pour fonctionner avec `seo-strategie`, `redaction-seo`, `seo-editorial`, `ux-cro` et `audit-digital`.

## 1. Place dans le pack : ne jamais empiéter

| Besoin | Skill qui décide |
|---|---|
| Mots-clés, architecture, mapping, maillage, URL, canonical, robots, redirections, hreflang, données structurées | `seo-strategie` |
| Texte indexable, title, meta description, H1 et Hn, ALT, nom des fichiers image, FAQ | `redaction-seo` |
| Affiliation, transparence, comparatifs, monétisation, widgets de réservation | `seo-editorial` |
| Audit ou vérification d'une page, y compris « que vaut ce design ? » | `audit-digital` (avec `ux-cro`) |
| Modification ciblée UX ou conversion d'une page existante | `ux-cro` |
| **Apparence** : système visuel, mise en page, composants, photos, mouvement, intégration HTML/CSS | **cette skill** |

- **Tu n'écris pas le texte indexable.** Tu mets en forme celui que fournit l'utilisateur ou `redaction-seo`, mot pour mot. S'il manque, appeler `redaction-seo` (qui demande style et ton) ou laisser un emplacement marqué `[À compléter : …]` et le lister à la livraison. Seuls les micro-textes d'interface sont à toi : mots du menu, libellés de boutons (verbe + objet : « Voir les chambres », jamais « En savoir plus »), libellés de champs.
- **Tu ne décides ni ne modifies** URL, canonical, meta robots, redirections, type de données structurées ou architecture. En création, tu poses les valeurs par défaut du gabarit (canonical auto-référente, `index, follow`) et tu les signales ; en refonte, tu reprends les valeurs existantes à l'identique. Tout changement passe par `seo-strategie` et une validation humaine.
- **Tu ne produis pas d'audit.** Une demande d'évaluation, de revue ou de vérification d'un design relève d'`audit-digital`. Ne jamais lancer spontanément un audit non demandé ; un problème vu en passant hors de la demande est noté en une ligne à la livraison.

## 2. Ordre de priorité (le même que `ux-cro`)

1. Obligations légales et accessibilité (RGPD, mentions obligatoires, WCAG).
2. **SEO**, sur toute page indexable qui reçoit ou vise du trafic organique.
3. UX : compréhension, lisibilité, facilité d'usage.
4. Conversion.
5. Esthétique.

**Conflit** : nommer le risque SEO, le gain visuel attendu, chercher une solution qui garde les deux ; à défaut, le SEO l'emporte. Sur une page sans rôle SEO (landing publicitaire en noindex, tunnel, remerciement), l'esthétique et la conversion passent avant, tant que la page reste en noindex et ne casse pas le maillage.

## 3. Cadrer avant de dessiner

### 3.1 Mode
| | Création | Refonte (page ou site existant) |
|---|---|---|
| Départ | Brief, mapping et textes validés (`seo-strategie`, `redaction-seo`) | La page en ligne et son HTML |
| Avant de toucher au code | — | **Relever** : title, meta description, canonical, meta robots, liste des Hn, liens internes (URL et ancres), nombre de mots du contenu principal, images et leurs ALT, données structurées |
| Règle | La navigation reflète le mapping, jamais l'inverse | URL, Hn, textes, liens et ALT inchangés ; le relevé est comparé après refonte : rien d'important ne disparaît |

En création, le design vient après l'architecture : si le mapping ou les textes n'existent pas, le dire et proposer `seo-strategie` ou `redaction-seo`, ou construire avec des emplacements marqués si l'utilisateur veut voir la forme d'abord.

### 3.2 Questions bloquantes (un seul message, 5 au maximum, jamais une information déjà donnée)
Page indexable ou non · textes fournis ou à produire · identité existante (logo, couleurs, polices, charte) · photos réelles disponibles · technologie cible (HTML/CSS, WordPress, Astro, Next.js…). Le reste : hypothèses explicites, et avancer.

### 3.3 Type de page : il décide de tout
| Type | Exemples | Ce qui mène | Exclu |
|---|---|---|---|
| **Éditorial** | Article, guide, comparatif, page de destination voyage | La lecture : une colonne, sommaire si long, photos originales, auteur et date de mise à jour visibles | Toute animation hors survol, effet de fond, découpage « un écran par section » |
| **Lieu** | Hôtel, gîte, restaurant, commerce, agence locale | Les photos réelles du lieu, l'adresse complète, les horaires, l'action (réserver, itinéraire) | Effets, fonds animés, mode sombre décoratif |
| **Service** | Cabinet, artisan, agence, consultant | Les réalisations, les personnes, le déroulé, le contact | Effets, illustrations génériques |
| **Produit** | Objet, marque, boutique | Le produit en grand, une vue différente par section | Effets ; 3D seulement pour montrer le produit, avec image fixe de repli |
| **Tech** | Logiciel, SaaS, application, jeu | La vraie interface du produit, en HTML | Plus d'un effet visuel sur la page |

Une page peut mêler deux types (un hôtel avec un blog) : chaque gabarit suit son propre type.

## 4. Démarche

1. **Lire** le brief, la charte, le mapping, les textes et le relevé (refonte).
2. **Choisir une direction** en une phrase, puis trois décisions écrites : palette (tirée du client : logo, façade, produit, photos), paire typographique, composition du premier écran. Varier d'un projet à l'autre : ne pas reprendre la même paire de polices ni le même héros que le projet précédent sans raison. En création à fort enjeu, proposer 2 ou 3 directions courtes et attendre le choix ; sinon, choisir et le dire.
3. **Planifier par sections** : identifiant, idée unique, visuel, Hn (repris du texte), action éventuelle.
4. **Construire** à partir de `assets/gabarit.html` et `assets/base.css`, avec les règles de `references/systeme-visuel.md` (grille, typo, couleurs, composants, mouvement, gabarits par type). Lire ce fichier en entier avant la première page.
5. **Vérifier** (§ 7), corriger, revérifier.
6. **Livrer** (§ 8).

## 5. Règles visuelles

Le « goût » vient de la retenue et de la cohérence, pas des effets.

- **Un seul système par page** : une échelle d'espacement, une échelle typographique, une famille d'arrondis, un style de bouton principal et un secondaire, un style de carte, un style de lien.
- **Typographie** : 2 familles au plus ; texte courant 16 px minimum (17-18 px sur l'éditorial), interligne 1,5 à 1,7 ; 60 à 75 caractères par ligne pour la lecture ; casse de phrase partout, jamais de longs passages en capitales. La taille visuelle d'un titre est réglée par une classe, jamais en changeant son niveau Hn.
- **Couleur** : interface à 90 % neutre ; la couleur vient des photos, du produit et d'**un** accent tiré du client (bouton principal, liens, focus). Pas de dégradé violet ou indigo « par défaut », pas de couleur sans lien avec le client. Contraste texte ≥ 4,5:1 (7:1 conseillé pour le corps), grands textes ≥ 3:1.
- **Mise en page** : bords gauche et droit alignés sur la même grille, rien qui déborde d'un côté ; une idée par section ; respiration régulière entre sections ; pas de bloc dans un bloc dans un bloc.
- **Photos** : réelles, du client, en priorité. Une photo de banque d'images n'est jamais présentée comme le lieu, l'équipe ou le produit du client. Pas de texte incrusté dans une image. Légende seulement si `redaction-seo` la fournit, jamais « image d'illustration ».
- **Icônes** : un seul jeu, cohérent ; les logos de marques réelles dans leurs couleurs d'origine, jamais redessinés.
- **Mouvement** : réponses au survol, au clic et au focus uniquement (carte qui monte de 2 px, photo à 1,02-1,03 dans son cadre, soulignement qui se trace, bouton qui s'enfonce au clic). Durées et courbes : `references/systeme-visuel.md`.
- **Interdits visuels** : apparitions au scroll, fondus d'entrée, parallaxe, inclinaison 3D, carrousels automatiques, compteurs animés, textes qui défilent, curseur personnalisé, écran de chargement, pop-up ou fenêtre modale à l'arrivée, éléments collants autres que l'en-tête et la barre d'action mobile.
- **Effets** (fond animé, WebGL, 3D) : type Tech uniquement, un seul par page, dans le premier écran, derrière le texte et jamais porteur de texte, avec une image fixe de repli sur mobile et en `prefers-reduced-motion`.
- **Preuves** : aucun faux avis, faux logo client, faux chiffre, fausse urgence ni compteur artificiel. Sans preuve réelle, des faits du brief ou rien.

## 6. Contraintes SEO intégrées au design (non négociables sur une page indexable)

**Rendu et structure**
- Contenu principal, Hn, liens internes, title, meta description, canonical et meta robots présents dans le **HTML servi, sans JavaScript**. Le JavaScript ne fait qu'améliorer (menu mobile, onglets cliqués, horaires « ouvert maintenant »).
- Un seul H1 ; la hiérarchie Hn suit le texte de `redaction-seo` ; aucun titre ajouté pour l'esthétique ; aucune balise Hn utilisée pour du simple style.
- Accordéons et onglets acceptés seulement si leur contenu est dans le DOM sans action de l'utilisateur (`<details>` natif de préférence).
- Même contenu sur mobile et sur desktop (indexation mobile d'abord) : rien d'utile masqué sur mobile.

**Liens**
- Toujours des `<a href>` explorables, ancres descriptives ; le menu et le pied de page reprennent le mapping ; en refonte, aucun lien interne supprimé ni rendu moins accessible.

**Images** (mêmes repères qu'`audit-digital` T10, pour qu'un audit ne contredise jamais la livraison)
- WebP ou AVIF pour les photos, SVG pour logos et icônes.
- ≤ 150 Ko par image (repère réglable ; une grande photo pleine largeur peut justifier un peu plus).
- Fichier au plus max(2, densité de l'écran) fois plus large que l'affichage : `srcset` + `sizes`.
- `width` et `height` (ou `aspect-ratio`) sur chaque image.
- Image du premier écran sans lazy-loading, avec `fetchpriority="high"` ; les suivantes en `loading="lazy"` et `decoding="async"`.
- Une photo de contenu est un `<img>`, jamais un fond CSS. ALT et nom de fichier fournis par `redaction-seo` ; image purement décorative : `alt=""`.

**Performance**
- Objectif terrain au 75e centile : LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1. Une mesure de laboratoire est indicative et présentée comme telle.
- Espace réservé pour tout ce qui arrive tard : images, vidéos, cartes, widgets d'affiliation ou de réservation, publicités, bannière cookies (en surimpression, sans décaler la page).
- Animer uniquement `transform`, `opacity` et les couleurs (comme dans `references/systeme-visuel.md`). Pas de bibliothèque d'animation, de WebGL ni de framework lourd hors type Tech. Pas d'iframe de carte au chargement : image statique ou façade cliquable.
- Polices **auto-hébergées** en woff2 (Google Fonts chargé depuis les serveurs de Google pose un problème RGPD) ; 4 fichiers au plus ; `font-display: swap` ; préchargement de 1 ou 2 fichiers ; police de repli ajustée (`size-adjust`) pour limiter le décalage.

**Mobile et accessibilité**
- `viewport`, aucun défilement horizontal, zones tactiles de 44 px conseillées (24 px minimum), texte 16 px minimum.
- `lang="fr"`, lien d'évitement, focus visible, navigation au clavier, libellés de formulaire, `prefers-reduced-motion` qui arrête tout mouvement sans rien laisser caché.

**Balises d'en-tête** (`assets/gabarit.html`)
- Title et meta description de `redaction-seo` ; canonical ; meta robots ; Open Graph ; données structurées seulement pour un type qui correspond au contenu visible (`LocalBusiness` pour un lieu, `Organization` pour une entreprise, `Article` pour un article…), validées par `seo-strategie` ; hreflang seulement si le site est multilingue.

**Local, légal, affiliation**
- **Coordonnées (NAP)** : nom, adresse et téléphone imprimés exactement tels que fournis, identiques partout (en-tête ou pied, contact, données structurées). Rien d'inventé : ce qui manque est listé à la livraison.
- **Pied de page** : liens vers Mentions légales et Politique de confidentialité ; bannière cookies avec un bouton Refuser aussi visible qu'Accepter (recommandation CNIL). Ce n'est pas un avis juridique.
- **Affiliation** (`seo-editorial`) : mention de transparence visible avant le premier lien affilié, mise en forme lisible et non cachée ; liens en `rel="sponsored"` ; boutons de réservation au moment du choix, sans couper la lecture.
- **Newsletter** : un formulaire dans la page ou le pied, jamais en fenêtre modale.

## 7. Vérifier avant de livrer

Ce sont des contrôles de fabrication, pas un audit. Utiliser les outils disponibles (navigateur, exécution de code, scripts du plugin `seo-expert` s'ils sont présents).
- **Regarder** la page à 1440, 1024, 768 et 390 px de large (captures de travail) : rien de coupé, de chevauchant, de décalé, de vide ; bords alignés ; premier écran clair.
- **Sans JavaScript** : texte principal, Hn, liens, title, canonical et meta robots présents.
- **Structure** : un H1, Hn dans l'ordre du texte, liens internes en `<a href>`.
- **Images** : inventaire (format, poids, surdimensionnement, dimensions, lazy) contre les repères du § 6.
- **Stabilité et vitesse** : CLS et LCP mesurés en laboratoire [Mesuré, laboratoire], poids total, nombre de polices.
- **Accessibilité** : contrastes, parcours clavier, focus, mouvement réduit.
- **Refonte** : relevé après modification comparé au relevé du § 3.1 ; toute différence est justifiée ou corrigée.
Statuts des constats : [Mesuré], [Observé], [Estimé], [Déduit], [Hypothèse]. Ne jamais écrire « vérifié » pour ce qui ne l'a pas été.

## 8. Livraison

1. Les fichiers (page, CSS, images optimisées), sans commentaire de travail dans le texte publiable.
2. Un **compte rendu de livraison** court :
   - **Direction retenue** : palette, typographie, composition du premier écran, en trois lignes.
   - **✅ Ce qui va bien** : chaque contrôle du § 7 réussi, avec sa preuve (valeur, extrait).
   - **❌ Problèmes à régler** : par priorité ; y compris ce que le client doit fournir (photos réelles, coordonnées, mentions légales, textes `[À compléter]`) et chaque valeur par défaut posée (canonical, robots) à valider.
   - **Limites** : ce qui n'a pas pu être vérifié (données terrain, rendu sur un vrai appareil…) et comment le vérifier.
   - **Repéré hors périmètre**, s'il y a lieu, en une ligne par point avec la skill qui le traiterait.
3. Captures dans le compte rendu : **uniquement pour un problème visuel**, cadrées sur l'endroit précis ; pas de capture générale.

## 9. Règles absolues

1. Ne jamais supprimer, raccourcir, masquer ou réécrire un texte indexable pour le design.
2. Ne jamais modifier URL, canonical, robots, redirections ou données structurées sans validation (`seo-strategie`).
3. Un seul H1 ; les Hn suivent le texte ; aucun titre décoratif.
4. Le contenu essentiel est dans le HTML servi, sans JavaScript.
5. Aucune animation déclenchée par le scroll, aucune entrée animée, aucun pop-up à l'arrivée.
6. Effets réservés au type Tech, un seul par page, avec repli fixe.
7. Polices auto-hébergées ; images aux repères du § 6.
8. Rien d'inventé : ni texte, ni coordonnée, ni avis, ni chiffre, ni logo client.
9. Pas d'audit spontané ; une évaluation de design passe par `audit-digital`.
10. En conflit, l'ordre du § 2 tranche.

## 10. Hors de Claude Code

Les scripts de relevé, d'inventaire des images et de captures ciblées sont dans le plugin Claude Code `seo-expert`. Ici, sans eux : vérifier avec les outils disponibles dans la session (navigation, exécution de code), sinon demander à l'utilisateur la capture ou l'export précis qui manque. Le compte rendu garde la même structure (✅ Ce qui va bien / ❌ Problèmes à régler) et la même règle des preuves visuelles.
