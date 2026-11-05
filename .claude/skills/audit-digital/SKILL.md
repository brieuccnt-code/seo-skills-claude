---
name: audit-digital
description: Chef d'orchestre de tout audit ou vérification d'un site ou d'une page. À utiliser dès que l'utilisateur demande un audit SEO, un audit technique, un audit de contenu, un audit UX, un audit CRO, un audit UX/CRO, un audit complet, ou de « vérifier » un point précis (rendu JavaScript, ALT, balises, indexation, vitesse…). Fixe le périmètre, la liste de contrôles, la gestion des données manquantes et le compte rendu.
---

# Système d'audit digital

Objectif : un audit professionnel, rigoureux, exploitable et transparent sur ses limites. Cette skill fixe **quoi vérifier et comment restituer** ; l'expertise vient des skills `seo-strategie` (technique, indexation, données), `redaction-seo` (contenu, sémantique), `ux-cro` (expérience, conversion) et `seo-editorial` (monétisation, affiliation, politiques Google).

## 1. Périmètre : s'en tenir strictement au type demandé
| Type demandé | Périmètre | Listes du § 2 |
|---|---|---|
| Audit SEO | SEO technique + contenu + sémantique + éditorial | T + C |
| Audit technique | Technique uniquement | T |
| Audit contenu | Contenu + sémantique + éditorial | C |
| Audit UX | UX/UI uniquement | U |
| Audit CRO | Conversion et monétisation uniquement | R |
| Audit UX/CRO | UX/UI + conversion | U + R |
| Audit complet | Tous les piliers + analyse stratégique et business | T + C + U + R + S |
| Vérification ciblée (« vérifie le rendu JavaScript », « vérifie les ALT »…) | Le seul point demandé | les points concernés |

- Annoncer le type retenu et la ou les pages auditées en une ligne. Si la demande est ambiguë (« regarde mon site »), demander le type en une question, avec cette liste.
- **Ne jamais réaliser spontanément un audit complémentaire non demandé.**
- Un problème repéré par hasard hors du périmètre n'est ni analysé ni recommandé : il est seulement noté en une ligne dans la rubrique « Repéré hors périmètre » du compte rendu, avec le type d'audit qui le traiterait.

## 2. Listes de contrôles
Chaque point de la liste du type demandé reçoit **un statut** : ✅ conforme, ❌ problème, ou ◻️ non vérifié (avec la raison et le moyen de le vérifier). Rien n'est omis en silence. Un point peut être « non applicable » (ex. pas de formulaire) : le dire. Une recommandation n'est écrite que pour un ❌.

**T — Technique**
T1 Code HTTP et redirections de la page · T2 HTTPS et contenu mixte · T3 robots.txt (page autorisée, sitemap déclaré) · T4 Meta robots / X-Robots-Tag · T5 Canonical (présente, auto-référente ou justifiée, dans le HTML servi) · T6 Sitemap XML (page présente, URL en 200 et indexables) · T7 Rendu JavaScript (contenu, Hn, liens, balises présents sans JS) · T8 Compatibilité mobile (viewport, débordement) · T9 Core Web Vitals (terrain si disponibles, sinon laboratoire indiqué comme tel) · T10 Images : poids, format moderne, dimensions déclarées, lazy-loading hors premier écran · T11 Liens internes et externes cassés · T12 Profondeur de clic et pages orphelines (si crawl) · T13 Données structurées (valides, conformes au contenu visible) · T14 Hreflang (si site multilingue) · T15 Duplication et paramètres d'URL.

**C — Contenu, sémantique, éditorial**
C1 Mot-clé principal identifié et pertinent pour la page · C2 Mot-clé principal dans le title, le H1 et l'introduction · C3 Title ≠ H1, title unique, longueur d'affichage · C4 Meta description · C5 Structure Hn (un H1, hiérarchie logique, titres descriptifs, sans sur-optimisation) · C6 Adéquation à l'intention de recherche et au format dominant de la SERP · C7 Mots-clés secondaires, longue traîne et questions des internautes couvertes · C8 Couverture sémantique et entités · C9 Longueur comparée au top 10 (méthode de `redaction-seo`) · C10 Qualité : réponse rapide, originalité, expérience de première main · C11 Fiabilité : sources, chiffres datés, informations à jour · C12 Maillage interne dans le texte et ancres · C13 ALT des images (descriptifs, sans bourrage) · C14 Cannibalisation avec une autre page du site (si données disponibles) · C15 Respect du style et du ton de la charte (si fournie).

**U — UX/UI**
U1 Compréhension immédiate (sujet, proposition de valeur, action principale en quelques secondes) · U2 Navigation (menu, fil d'Ariane, retour arrière) · U3 Hiérarchie visuelle (éléments qui ne se concurrencent pas) · U4 Lisibilité (taille, contraste, largeur des blocs, paragraphes) desktop et mobile · U5 Mobile (zones tactiles ≥ 24 px, navigation au pouce, menu, tableaux, débordements) · U6 Accessibilité (contrastes, clavier, focus, libellés, intitulés des boutons, ALT) · U7 Cohérence graphique et états interactifs · U8 Interstitiels et éléments intrusifs.

**R — Conversion et monétisation**
R1 Conversion principale identifiée (devis, réservation, clic affilié, inscription…) · R2 Appels à l'action : visibilité, formulation verbe + objet, emplacement, cohérence avec l'étape du parcours, pas de CTA concurrents · R3 Monétisation : widgets, liens d'affiliation, boutons de réservation visibles au moment du choix, sans couper la lecture · R4 Transparence commerciale (mention avant le premier lien affilié, `rel="sponsored"`) · R5 Réassurance et preuves (avis authentiques, auteur, garanties) · R6 Persuasion honnête (aucune fausse urgence, rareté ou faux avis) · R7 Formulaires (si présents) · R8 Parcours et frictions selon la maturité du visiteur · R9 Mesure : conversions et clics affiliés suivis (si analytics accessible).

**S — Stratégie et business (audit complet uniquement)**
S1 Pages qui portent le trafic et le revenu · S2 Pages à fort potentiel (position 4–20, CTR faible) · S3 Écart entre trafic et conversion par page · S4 Opportunités de contenu ou de monétisation alignées sur l'offre · S5 Risques (dépendance à quelques pages, saisonnalité, politiques Google). Ces points demandent des données (Search Console, analytics, revenus) : appliquer le § 3.

## 3. Données externes
Quand une analyse demande des données ou un outil inaccessibles :
1. Identifier précisément l'information manquante.
2. Dire si elle est **indispensable** ou **facultative**.
3. Demander si l'utilisateur peut la fournir.
4. Indiquer où la récupérer et comment l'exporter, au format attendu.
5. Préciser quels points de la liste elle permettra de vérifier.
**Ne pas bloquer l'audit** : réaliser tout ce qui est possible, marquer le reste ◻️ non vérifié. Ne jamais redemander une donnée déjà fournie.

| Donnée | Où la récupérer | Format | Points |
|---|---|---|---|
| Performances de recherche | Search Console → Performances → Requêtes et Pages (3 à 16 mois), ou export requête × page | CSV | C1, C14, S1–S3 |
| Indexation d'une URL | Search Console → Inspection de l'URL → « Tester l'URL en direct » | capture | T4, T5, T7 |
| Core Web Vitals terrain | Search Console → Signaux Web essentiels, ou PageSpeed Insights (section « données réelles ») | capture ou CSV | T9 |
| Crawl du site | Screaming Frog : « Internal: All » et « All Inlinks » | CSV | T11, T12, T15, C12 |
| Comportement et conversions | GA4 (Rapports → Pages, Conversions) ; Microsoft Clarity (cartes de chaleur, clics de rage) | CSV ou captures | R1, R8, R9, S3 |
| Volumes de recherche | Google Keyword Planner | CSV | C1, C7 |

## 4. Fiabilité des diagnostics
- Ne jamais inventer une donnée, un résultat ou une mesure ; ne jamais prétendre avoir utilisé un outil inaccessible.
- Distinguer systématiquement **[Mesuré]** (outil, fichier), **[Observé]** (vu sur la page ou une capture), **[Déduit]** (raisonnement à partir de faits cités) et **[Hypothèse]** (plausible, non vérifié).
- Fournir une preuve précise pour chaque problème important (extrait de code, valeur mesurée, capture, URL).
- Ne pas présenter une estimation ou une mesure de laboratoire comme une mesure terrain.
- Ne pas appliquer mécaniquement des règles SEO dépassées ; adapter au type de site (éditorial, e-commerce, local, SaaS…).
- Ne jamais confondre : problème absent et problème non vérifié ; observation et mesure ; corrélation et causalité ; opportunité et résultat garanti.

## 5. Restitution
Chaque audit a sa propre synthèse et son propre plan d'action ; un audit complet a une synthèse globale puis une partie par pilier.

**Audit (tous types sauf vérification ciblée)** — dans cet ordre :
1. **Périmètre et état des lieux** : type, page(s), date, mode (création / optimisation), sources, données disponibles.
2. **Synthèse des constats** : verdict en 2 phrases + nombre de points conformes, de problèmes par criticité, de points non vérifiés.
3. **Preuves visuelles** : captures **desktop et mobile** dès qu'une page est concernée (sans JavaScript et après JavaScript pour T7), jointes que le résultat soit bon ou mauvais.
4. **✅ Ce qui va bien** : chaque point conforme, avec sa preuve.
5. **❌ Problèmes à régler** : triés par criticité (haute, moyenne, basse) ; pour chacun : constat, preuve, conséquence, recommandation concrète (avec exemple de correction quand c'est utile), effort, risque SEO, statut de preuve.
6. **Tableau des contrôles** : chaque point de la liste avec son statut ✅ / ❌ / ◻️ / non applicable.
7. **Niveau de confiance** du diagnostic (élevé, moyen, faible) et ce qui le limite.
8. **Plan d'action priorisé** : bloquants, gains rapides, chantiers de fond, avec effort.
9. **Données complémentaires** utiles (§ 3) et ce qu'elles amélioreraient.
10. **Conclusion**.
Puis : **Repéré hors périmètre** (une ligne par point, avec le type d'audit à lancer) et **Limites** (ce qui n'a pas pu être vérifié et comment le vérifier).

**Vérification ciblée** — version courte : périmètre, verdict, preuves visuelles, ✅, ❌, niveau de confiance, limites.

Si l'utilisateur veut garder ou partager le compte rendu hors du terminal, proposer d'en faire un document.

## 6. Qualité des recommandations
Chaque recommandation est précise, justifiée par un constat, adaptée au site, réalisable, priorisée, et accompagnée d'un exemple de correction quand c'est pertinent (balise corrigée, texte proposé, emplacement d'un CTA). Pas de recommandation générique, répétée ou ajoutée pour remplir la liste.

## 7. Outils dans le terminal (Claude Code)
1. Captures et contrôles automatiques : `py .claude/skills/ux-cro/scripts/ux_snapshot.py <url> -o data/clean/ux/AAAA-MM-JJ` ; ajouter `--js` pour T7 (captures desktop et mobile sans JavaScript, comparaison sans JS / après JS). **Regarder les captures** avant de conclure.
2. Autres scripts selon les points : `gsc_analyze.py`, `link_graph.py` (skill `seo-strategie`), `serp_length.py` (skill `redaction-seo`).
3. Compte rendu : copier `templates/compte-rendu.json` dans `deliverables/AAAA-MM-JJ_<projet>_<type-audit>.json`, le remplir (champs `controles`, `plan_action`, `confiance`, `donnees_complementaires`, `conclusion`, `hors_perimetre`), puis `py .claude/skills/seo-strategie/scripts/rapport.py deliverables/<fichier>.json` → page HTML autonome.
4. Donner le chemin du HTML et un résumé de 3 lignes : verdict, nombre de points conformes et de problèmes prioritaires, données qui manquent.
