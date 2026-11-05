# Principes communs obligatoires

## 1. Statut de chaque information
Tout constat, chiffre ou idée porte l'un de ces statuts (dans une colonne `evidence` ou entre crochets) :
- **[Mesuré]** : issu directement d'un outil ou d'un fichier (indiquer lequel).
- **[Observé]** : constat direct sur une page, une SERP ou un crawl (indiquer date, pays, appareil).
- **[Estimé]** : calcul dont la méthode est explicitée.
- **[Hypothèse]** : plausible mais non vérifié.
- **[Recommandation]** : action proposée.

Ne jamais présenter une hypothèse comme un fait. Ne jamais inventer un volume, une position, un trafic, une difficulté, un backlink, un avis, une certification, un prix ou une statistique.

## 2. Qualité des données
Pour chaque métrique : source, période, pays, langue, appareil si disponible, périmètre, limites.
- Ne pas mélanger des périodes ou des définitions incompatibles.
- Search Console = performances d'une propriété vérifiée, pas du marché.
- Keyword Planner = estimations, regroupement de variantes proches, dépend du ciblage et du compte.
- Comparer des périodes de même durée et de même saisonnalité (idéalement en glissement annuel).

## 3. Méthode générale
1. Cadrer : objectif, audience, offre, zone, langue, conversions, contraintes, ressources.
2. Inventorier les données disponibles et documenter les manques.
3. Comprendre l'intention de recherche et le parcours utilisateur.
4. Définir architecture et mapping **avant** toute rédaction.
5. Produire des contenus différenciés, utiles et vérifiables.
6. Contrôler technique, UX, maillage, données structurées et mesure.
7. Prioriser (voir §7).
8. Définir comment mesurer le résultat et quand réévaluer.

## 4. Règles éditoriales (résumé — détail dans la skill `seo-copywriting`)
- Écrire pour l'utilisateur, jamais pour une densité de mots-clés ni une longueur arbitraire.
- Le style et le ton du projet (`references/CHARTE-EDITORIALE.md`) priment sur toute optimisation.
- Apporter une valeur propre : expérience vécue, méthode, données, exemples, informations opérationnelles.
- Signaler `[À confirmer]` toute information qui doit venir du client ou d'un expert.

## 5. Architecture et cannibalisation
- Une requête ne justifie pas automatiquement une URL.
- Même intention + mêmes types de résultats en SERP → même page.
- Besoins, offres, audiences ou SERP différents → pages distinctes.
- Toujours vérifier les URL existantes avant d'en créer une.

## 6. SERP et concurrence
- Une analyse concurrentielle repose sur des résultats réellement observés, datés et localisés.
- Concurrents commerciaux ≠ concurrents SEO.
- Ne pas déduire trafic, conversions ou stratégie d'un concurrent sans source.

## 7. Priorisation
Score indicatif : `priorité = (impact × confiance) / effort`, chacun noté 1 à 3. Puis ajuster selon le risque et les dépendances.
Toujours séparer trois groupes :
1. **Bloquants** : empêchent l'indexation ou la conversion.
2. **Gains rapides** : effort faible, impact mesurable sous 4 à 8 semaines.
3. **Chantiers stratégiques** : architecture, contenus de fond, autorité.

## 8. Actions risquées : validation humaine obligatoire
Publication, suppression, redirection, canonical, noindex, robots.txt, migration, changement d'URL, déploiement, modification de masse. Proposer le plan, son mode de test et son retour arrière, puis attendre un « go » explicite.

## 9. Fin de chaque livrable
- Sources et dates.
- Hypothèses retenues.
- Données manquantes et leur impact sur la confiance.
- Prochaines vérifications et date de réévaluation.
