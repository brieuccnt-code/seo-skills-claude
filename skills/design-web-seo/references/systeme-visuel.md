# Système visuel

Les valeurs de ce fichier sont les réglages par défaut de `assets/base.css`. Une charte client existante passe avant : on garde sa logique, on applique ces règles là où elle ne dit rien.

## 1. Grille et espacement

- Échelle d'espacement unique : 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px (`--s-1` à `--s-10`). Toute marge, tout écart, tout padding en vient.
- Conteneur `.wrap` : 1200 px de contenu au plus, marges latérales 80 px sur grand écran, 24 px sous 640 px, 16 px minimum. Tous les blocs s'alignent sur ses deux bords.
- Grille `.grid` de 12 colonnes, écart 24 px (12 px sous 640 px). Compositions courantes : 6/6, 7/5, 4/4/4, 3/3/3/3, 8 centré.
- Rythme des sections : 96 à 128 px en haut, 64 à 96 px en bas sur desktop ; 64 / 48 px sur mobile. Titre de section → contenu : 48 px (32 sur mobile). Cartes : 24 px d'écart.
- Colonne de lecture (éditorial) : `.measure` = 68 caractères (environ 680 px à 17 px), centrée ou alignée sur la colonne principale.
- Profondeur : deux boîtes imbriquées au plus.

## 2. Typographie

- Deux familles au plus : une de titrage, une de texte (ou une seule famille en plusieurs graisses). 4 fichiers woff2 au plus, auto-hébergés.
- Échelle (desktop / mobile) : H1 48-64 / 34-40 px ; H2 32-40 / 26-30 ; H3 20-24 / 18-20 ; texte 16-18 ; petit 14 ; libellé 13. Rien sous 13 px.
- Interligne : titres 1,05 à 1,2 ; texte 1,5 à 1,7. Approche légèrement resserrée sur les grands titres (−0,01 à −0,02 em).
- Casse de phrase partout. Italique pour citations seulement. Guillemets français « » et espaces insécables avant `: ; ! ?`, entre un nombre et son unité (« 12 km », « 45 € »).
- Un seul style par type d'élément sur toute la page (tous les titres de cartes identiques, toutes les dates identiques).
- La taille visuelle est portée par des classes (`.t-h1`, `.t-h2`, `.t-h3`) : un H3 peut paraître grand, un H2 peut paraître sobre, sans changer la hiérarchie.

### Paires de départ (à varier d'un projet à l'autre, toutes libres et auto-hébergeables)
| Ton | Titrage | Texte |
|---|---|---|
| Éditorial chaleureux | Fraunces | Source Sans 3 |
| Contemporain net | Inter Tight | Inter |
| Classique élégant | Cormorant Garamond | Lato |
| Voyage, nature | DM Serif Display | DM Sans |
| Technique | Space Grotesk | IBM Plex Sans |
| Artisan, local | Libre Caslon Display | Work Sans |

Éviter de reprendre la même paire que le projet précédent sans raison.

## 3. Couleur

- Jetons : `--ink` (texte, quasi-noir, jamais #000), `--muted` (texte secondaire, ≥ 4,5:1), `--line` (filets, 12-15 % de l'encre), `--bg` (fond principal), `--bg-alt` (fond secondaire, même teinte un peu plus soutenue), `--accent` (une seule couleur de marque), `--on-accent` (texte sur l'accent, ≥ 4,5:1).
- Interface à 90 % neutre. L'accent : bouton principal, liens, focus, petits repères, au plus une bande de couleur par page. Ailleurs, moins de 3 % de l'écran.
- L'accent vient du client : logo, façade, produit, paysage dominant de ses photos. À défaut, une teinte cohérente avec le secteur, jamais un violet ou indigo « par défaut ».
- Mise en avant par le contraste et la graisse, pas par des surlignages colorés.
- Thème sombre décoratif : type Tech uniquement. Si le site propose un mode sombre, il est piloté par `prefers-color-scheme`, jamais par le scroll.

## 4. Composants

**Boutons** : `.btn--primary` (rempli d'accent, un seul principal visible par écran) et `.btn--secondary` (contour ou texte souligné). 44 px de haut (48 sur un lieu et sur mobile), texte 16 px, 24 px de padding latéral, deux boutons côte à côte au plus, pleine largeur sous 640 px. Libellé : verbe + objet. Jamais de bouton en dégradé, incliné, fantôme sur photo ou avec ombre portée.

**En-tête** : collant en haut (`position: sticky`), fond opaque, filet de 1 px dessous, même aspect à tout niveau de scroll (pas de flou, de transparence, de rétrécissement ni de masquage). Logo à gauche, 4 à 6 entrées d'un mot issues du mapping, action principale à droite. Sous 1024 px : bouton menu de 44 × 44 px qui ouvre un panneau plein écran ; le menu reste un `<nav>` de liens présents dans le HTML.

**Barre d'action mobile** (lieu, conseillée ailleurs) : fixée en bas sous 640 px, une action (ou deux), hauteur 48 px + zone de sécurité ; le bas de page reçoit un padding équivalent pour que rien ne soit caché.

**Cartes** : un seul style par page ; une hauteur par rangée ; si la carte est cliquable, le lien entoure toute la carte et son titre reste un vrai titre. Pas de texte dans une boîte dans une boîte.

**Listes de prix, menus, caractéristiques** : lignes séparées par un filet, libellé à gauche, valeur alignée à droite, chiffres tabulaires.

**Horaires** : `<dl>` jours / heures, lisible sans JavaScript ; le JavaScript peut seulement mettre en gras le jour courant.

**FAQ** : questions en Hn selon le texte fourni, réponses visibles ou dans `<details>` natif (contenu dans le DOM).

**Formulaires** : champs de 48 px, libellé visible au-dessus (13-14 px), texte 16 px (évite le zoom iOS), 6 champs au plus sauf besoin réel, erreurs écrites en clair près du champ, une ligne qui dit quand arrive la réponse, jamais de faux message de succès.

**Pied de page** : coordonnées complètes si fournies (identiques à celles des données structurées), liens du mapping en colonnes, ligne légale (nom, année, Mentions légales, Confidentialité, Cookies, crédits photos s'il y en a).

**Bloc de transparence affiliation** : encadré discret mais lisible (fond `--bg-alt`, texte 14-16 px, contraste ≥ 4,5:1), placé avant le premier lien affilié, avec un lien vers la page qui explique la rémunération.

**Widgets tiers** (réservation, carte, avis, publicité) : conteneur à hauteur réservée (`min-height` ou `aspect-ratio`) pour éviter tout décalage.

## 5. Mouvement

| Élément | Réaction | Durée |
|---|---|---|
| Bouton | survol : fond assombri de 10-15 %, montée de 1 px ; clic : redescend et `scale(.985)` | 140 ms entrée, 200 ms sortie, 90 ms clic |
| Lien dans le texte | un soulignement fin au repos, un trait plein qui se trace de gauche à droite | 140 / 200 ms |
| Carte cliquable | monte de 2 px, filet un cran plus foncé, ombre très douce facultative | 180 ms |
| Photo dans un lien | zoom 1,02-1,03 à l'intérieur de son cadre (`overflow: hidden`) ; le cadre ne bouge pas | 600 ms |
| Focus clavier | anneau de 2 px à l'accent, décalé de 2 px | 200 ms |
| Panneau du menu | apparition en fondu + 6 px, uniquement après action de l'utilisateur | 200 ms |

- Courbe : `cubic-bezier(.2,.8,.2,1)` ; pas de rebond.
- Survol réservé aux pointeurs fins (`@media (hover: hover)`) ; tout ce qui réagit au survol marche aussi au clic et au clavier.
- Animer seulement `transform`, `opacity` et les couleurs ; jamais `height`, `padding`, `top` ni la mise en page.
- `prefers-reduced-motion: reduce` : toutes les transitions à ~0, rien de caché.
- Type Tech seulement : une boucle discrète dans une illustration d'interface (2,5 à 4 s par cycle), un effet de fond dans le premier écran avec image de repli ; tout ce qui bouge plus de 5 s a un bouton pause.

## 6. Premier écran

Il dit en quelques secondes ce que c'est, pour qui ou où, et quelle est l'action principale. Le H1 et l'accroche viennent de `redaction-seo`. Une seule action principale (deux au plus).

Compositions à faire tourner d'un projet à l'autre :
- **Photo pleine largeur** + texte dans une zone calme de la photo ou dans un aplat (lieu, voyage).
- **Partage 7/5** : texte à gauche, visuel à droite (service, produit, tech).
- **Éditorial** : surtitre de rubrique, H1, chapô, auteur et date, puis grande photo sous le texte (article, guide).
- **Mosaïque** : texte au-dessus, trois photos de tailles différentes dessous (lieu, produit).
- **Typographique** : H1 très grand sur aplat, visuel au second écran (marque forte, peu de photos).
- **Interface** : texte centré au-dessus d'une capture d'interface en HTML (tech).

Règles : l'image du premier écran est l'élément LCP probable, donc légère, `fetchpriority="high"`, sans lazy ; jamais de texte sur une photo chargée sans aplat ou zone calme garantie à toutes les largeurs ; jamais de vidéo en lecture automatique comme seul contenu du premier écran.

## 7. Gabarits par type de page

**Éditorial (article, guide, comparatif)**
Fil d'Ariane → H1 → chapô → auteur, date de publication et de mise à jour → photo principale → sommaire cliquable si plus de 4 H2 → corps en colonne `.measure` (texte 17-18 px) → encadrés, tableaux comparatifs et photos à pleine colonne → bloc auteur → articles liés (liens du cocon fournis par `seo-strategie`). Aucune section « un écran ». Les tableaux défilent horizontalement dans leur conteneur sur mobile, jamais la page.

**Lieu (hôtel, gîte, restaurant, commerce)**
Premier écran photo → infos pratiques (adresse complète, horaires, accès) dès le deuxième écran → l'offre (chambres, carte, produits) en photos → le lieu et les personnes → avis réels s'il y en a → réservation ou contact → pied avec coordonnées. 8 à 20 photos réelles selon la longueur. Carte : image statique + lien « Voir l'itinéraire ».

**Service**
Proposition de valeur → prestations → déroulé en étapes → réalisations (photos réelles) → équipe → questions → contact. Réassurance placée près des zones d'hésitation.

**Produit**
Produit en grand → bénéfices illustrés (une vue différente par section) → caractéristiques en lignes → prix et conditions → avis réels → questions → achat. Chaque variante de couleur change réellement la photo.

**Tech**
Interface réelle en HTML dans un cadre de fenêtre → fonctionnalités en cartes avec fragments d'interface → intégrations (logos réels) → prix → questions → essai. Un seul effet visuel sur la page.

## 8. Liste anti-« modèle »

Avant de livrer, la page ne doit présenter aucun de ces signes de page générée en série :
- dégradé violet-bleu, halo flou derrière le titre, fond à motif de points par défaut ;
- trois cartes identiques à icône ronde et trois lignes de texte, répétées section après section ;
- toutes les sections centrées, de la même hauteur, sur le même fond ;
- emojis en guise d'icônes ;
- titres slogans (« Là où X rencontre Y »), boutons « En savoir plus » ;
- faux témoignages avec photos de banque d'images, faux logos clients, chiffres ronds inventés ;
- ombres portées fortes partout, arrondis différents d'un bloc à l'autre ;
- photos qui ne montrent pas le vrai client.
