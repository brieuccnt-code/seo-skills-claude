---
name: seo-editorial
description: SEO des sites éditoriaux, de niche et d'affiliation. À utiliser pour un blog ou un site de contenu (voyage, thématique), des liens d'affiliation, un comparatif ou une page « meilleur X », un test produit, la transparence commerciale, le risque de pénalité Google (contenu en masse, IA, affiliation pauvre), la visibilité dans les réponses des IA (GEO, AEO, aperçus IA, ChatGPT, Perplexity) ou un calendrier éditorial saisonnier.
---

# SEO éditorial, affiliation et GEO

Complète `seo-strategie` (architecture, données) et `redaction-seo` (écriture). Cette skill porte sur ce qui fait chuter un site éditorial ou d'affiliation, et sur ce qui est vrai ou faux en GEO. Les règles de vérité s'appliquent : rien d'inventé, statuts [Mesuré] / [Observé] / [Estimé] / [Hypothèse].

**Règles et politiques datées** : ce qui suit est vérifié en novembre 2026. Les politiques Google et le droit évoluent : pour une décision importante, revérifier la source officielle et le dire.

## 1. Les politiques anti-spam de Google qui visent ces sites
Source : Google Search Central, « Spam policies ». À vérifier avant toute stratégie de volume.
- **Contenu à grande échelle (scaled content abuse)** : produire beaucoup de pages surtout pour se classer plutôt que pour aider, **quelle que soit la méthode**, IA générative comprise (« générer de nombreuses pages sans valeur ajoutée pour les utilisateurs »). Conséquence pratique : jamais de génération de pages en série (une par ville, par produit, par question) sans valeur propre vérifiable sur chacune. L'IA n'est pas interdite ; l'absence de valeur l'est.
- **Affiliation pauvre (thin affiliation)** : pages d'affiliation qui reprennent les descriptions du marchand sans apport original. Google précise que tout site affilié n'est pas pauvre : il faut tests réels, avis originaux, comparaisons, fonctionnalités utiles.
- **Abus de réputation de site** : contenu tiers hébergé surtout pour profiter des signaux d'un domaine fort (pages « partenaires » de codes promo ou de casinos sur un média). Mise à jour 2026 : traitement différent dans l'Espace économique européen (pages classées à part du domaine principal plutôt qu'action manuelle). Ne jamais recommander d'héberger ou de louer ce type de section.
- **Domaine expiré** : racheter un domaine expiré pour y placer du contenu sans rapport et profiter de son historique.
- **Détournement du bouton retour** (pratique malveillante, 2026) : empêcher l'utilisateur de revenir à la page précédente. Interdire tout script de ce type (pop-under, redirections d'historique) même proposé par une régie.
- Aussi pertinents : liens achetés ou échangés pour le classement (link spam), pages satellites (doorways), bourrage de mots-clés.

## 2. Liens d'affiliation : technique et transparence
**Attributs** : un lien rémunéré (affiliation, placement payé) porte `rel="sponsored"` (Google l'indique pour les liens publicitaires et payants ; `nofollow` reste accepté). Vérifier aussi les redirections de liens (pas de cloaking : Googlebot et le visiteur arrivent au même endroit).

**Transparence (France)** — ce n'est pas un avis juridique ; pour un cas réel, faire valider :
- Le caractère publicitaire d'un contenu doit être clairement identifiable (principe de la loi pour la confiance dans l'économie numérique, article 20) ; cacher une rémunération peut constituer une pratique commerciale trompeuse.
- Pour les contenus d'influence commerciale (loi n° 2023-451, modifiée par l'ordonnance n° 2024-978), l'intention commerciale doit être signalée par « Publicité », « Collaboration commerciale » ou une mention équivalente compréhensible.
- Les programmes d'affiliation imposent souvent leur propre mention (ex. programmes de grandes plateformes de vente) : la reprendre telle qu'exigée.
**Mise en œuvre recommandée** : une phrase de transparence visible avant le premier lien affilié (pas seulement en pied de page) + une page « Comment nous gagnons de l'argent » liée depuis cette phrase. Ne jamais la noyer ni la formuler de façon ambiguë.

## 3. Comparatifs, tests et pages « meilleur X »
Ce que Google attend d'un avis (documentation « rédiger des avis de qualité ») et ce qui distingue un site affilié utile :
- **Preuve d'usage réel** : photos et vidéos originales, mesures, conditions de test, durée d'utilisation. Si le produit n'a pas été testé, le dire et présenter la page comme une sélection documentée, jamais comme un test.
- **Méthode publiée** : critères, pondération, sources, ce qui n'a pas été testé.
- **Comparaison** : avec les alternatives, points forts et faibles de chacune, pour quel profil d'usage. Un tableau comparatif sert la décision.
- **Expertise visible** : auteur identifié, pourquoi il est légitime sur ce sujet.
- **Honnêteté** : inclure les défauts ; ne pas recommander uniquement ce qui rapporte la meilleure commission ; dire quand une option non affiliée est meilleure.
- **Mises à jour réelles** : prix, disponibilités et modèles revérifiés ; la date de mise à jour ne change que si le contenu a changé.
Pour les avis d'hébergements, d'activités ou de voyages : prix relevés avec leur date, conditions réelles (saison, accès, temps de trajet), pas de note chiffrée inventée.

## 4. GEO / AEO : ce qui est établi et ce qui ne l'est pas
**Établi (Google, 2026)** :
- Les aperçus IA et le mode IA de Google s'appuient sur l'index de recherche normal (Googlebot). **Il n'existe ni index IA séparé, ni balise, ni fichier à soumettre** : une page doit être indexée et éligible à un extrait.
- Contrôles disponibles : `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex` — ils limitent aussi l'extrait dans les résultats classiques. Bloquer `Google-Extended` **ne retire pas** une page des aperçus IA ni de la recherche ; il concerne l'entraînement et certains autres produits Google.
- Les autres moteurs ont leurs propres robots (ex. robots de recherche distincts des robots d'entraînement chez plusieurs éditeurs) : vérifier leur documentation actuelle avant de bloquer ou autoriser dans le robots.txt, et faire de ce choix une décision business validée.

**Non établi — ne pas promettre ni présenter comme nécessaire** :
- `llms.txt` n'est pas un standard utilisé par Google ; aucune preuve qu'il améliore la visibilité.
- Aucun « score GEO », aucune densité, aucune structure garantissant une citation.

**Ce qui aide (et sert aussi le SEO classique)** : réponse directe et autonome en tête de section ; définitions claires ; chiffres datés et sourcés ; entités nommées sans ambiguïté ; informations de première main que les autres sources n'ont pas ; identité de l'auteur et du site cohérente partout.

**Mesure** : uniquement observable — trafic référent depuis les assistants IA dans analytics, rapports de Search Console sur les fonctionnalités IA lorsqu'ils sont disponibles, relevés manuels datés d'un panel de questions. Ne jamais estimer une « part de citations » sans relevé.

## 5. Calendrier éditorial saisonnier
- Partir des volumes mensuels (Keyword Planner, 12 mois) ou des impressions Search Console sur 16 mois : repérer le mois de pic de chaque thème.
- **Publier 2 à 3 mois avant le pic** (repère de pratique, à ajuster selon l'autorité du site : le temps d'être exploré, indexé et de gagner des positions) ; **mettre à jour 1 à 2 mois avant** le pic suivant pour les pages existantes.
- Prioriser : pages commerciales et d'affiliation proches de la décision (réservation, comparatif) avant les contenus informationnels d'appel ; mises à jour de pages qui ont déjà des impressions avant nouvelles pages.
- Contenus à informations périssables (prix, horaires, règles d'entrée, transports) : date de dernière vérification affichée et revue planifiée.
- Rythme soutenable plutôt que volume : mieux vaut moins de pages réellement utiles (§ 1).
Livrable : thème, page, type (création / mise à jour), mois de pic, date de publication ou de mise à jour, priorité, source de la saisonnalité.

## 6. Monétisation sans dégrader l'expérience
- Liens affiliés là où le lecteur en a besoin (au moment du choix), pas en tête de chaque paragraphe ; la réponse à la question passe avant le lien.
- Publicité display : ne pas dégrader les Core Web Vitals (emplacements réservés pour éviter les décalages, pas d'interstitiel intrusif) ni masquer le contenu.
- Mesurer les clics affiliés comme conversions (événements analytics) ; revenus analysés seulement si fournis.

## 7. Contrôle avant publication (en plus de la checklist de `redaction-seo`)
Pour l'audit d'une page ou d'un site existant, rendre un compte rendu en deux parties : **✅ ce qui va bien** et **❌ problèmes à régler** (triés par priorité, chacun avec preuve et correction), précédées d'un verdict et suivies des limites ; captures ciblées uniquement pour un problème visuel (ex. widget de réservation invisible sur mobile).
- [ ] La page apporte une valeur propre (test, données, expérience, comparaison) — pas une reprise du marchand ni une page de série.
- [ ] Mention de transparence visible avant le premier lien affilié ; liens en `rel="sponsored"`.
- [ ] Ce qui a été testé et ce qui ne l'a pas été est dit clairement.
- [ ] Prix, disponibilités et faits périssables datés.
- [ ] Aucun script publicitaire ou d'affiliation qui gêne la navigation ou le retour arrière.
- [ ] Aucune promesse de visibilité dans les IA.

Sources de référence : Google Search Central (politiques anti-spam ; qualifier les liens sortants ; rédiger des avis de qualité ; fonctionnalités IA et votre site web) ; Légifrance (LCEN art. 20 ; loi n° 2023-451 ; ordonnance n° 2024-978).

## 8. Outils dans le terminal (Claude Code)
Pour la saisonnalité (§ 5) : `kp_clean.py` (skill `seo-strategie`) calcule le mois de pic et un indice de saisonnalité à partir d'un export Keyword Planner avec volumes mensuels ; `gsc_analyze.py` compare deux périodes de Search Console. Livrable du calendrier dans `deliverables/`. Compte rendu HTML : `templates/compte-rendu.json` → `rapport.py` (skill `seo-strategie`).
