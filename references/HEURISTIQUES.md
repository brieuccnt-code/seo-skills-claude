# Heuristiques de décision

Ces seuils sont des **règles de pratique**, pas des règles de Google. Ils servent à décider vite et de façon cohérente. Les ajuster au projet et le noter dans le livrable.

## Clustering par SERP
Recouvrement = nombre d'URL communes dans le top 10 organique de deux requêtes.
| URL communes | Décision par défaut |
|---|---|
| ≥ 4 | Même page |
| 3 | Même page, sauf si l'intention ou l'offre diffère nettement |
| 2 | Zone grise : arbitrer selon l'intention et le type de pages en SERP |
| 0–1 | Pages distinctes, ou la requête est une section d'une autre page |

- Seuil par défaut du script `serp_cluster.py` : 3.
- En marché de niche (peu de résultats pertinents), on peut descendre à 2.
- Un recouvrement fort entre une requête informationnelle et une requête transactionnelle reste suspect : vérifier la SERP.

## Opportunités Search Console
- **Gain rapide « position »** : position moyenne entre 4 et 20, impressions dans le quart supérieur de la propriété. Action : enrichir la page, mieux traiter l'intention, renforcer le maillage interne entrant.
- **Gain rapide « CTR »** : position ≤ 10 mais CTR nettement inférieur (< 50 %) à la médiane des requêtes à position comparable sur la même propriété. Action : réécrire title et meta description, vérifier les fonctionnalités de la SERP qui captent le clic.
- **Cannibalisation probable** : une même requête fait des impressions sur ≥ 2 URL, la 2ᵉ URL porte ≥ 20 % des impressions, et les URL alternent dans le temps. Ne pas conclure sans vérifier que les deux pages visent bien la même intention : deux pages peuvent légitimement se positionner.
- **Contenu en déclin** : baisse des clics ≥ 30 % en glissement annuel sur une page avec un volume de clics suffisant. Chercher d'abord une cause externe (saisonnalité, mise à jour Google, changement de SERP) avant une cause interne.
- Ignorer les lignes avec moins de ~50 impressions sur la période pour toute conclusion : trop de bruit.

## Pages
- **Title** : terme principal tôt, promesse spécifique, environ 50–60 caractères visibles. Unique sur le site.
- **Meta description** : résumé incitatif, environ 140–160 caractères. Google la réécrit souvent : ne pas y passer trop de temps sauf sur les pages à fort volume d'impressions.
- **H1** : unique, descriptif, cohérent avec le title (pas forcément identique).
- **Profondeur** : pages stratégiques à 3 clics maximum de l'accueil.
- **Page orpheline** : aucun lien interne entrant crawlable. Toujours un problème pour une page qu'on veut positionner.

## Core Web Vitals (seuils « bon » au 75ᵉ centile, données terrain)
- LCP ≤ 2,5 s · INP ≤ 200 ms · CLS ≤ 0,1.
- Utiliser les données terrain (CrUX, rapport GSC) avant les tests de laboratoire. Une mauvaise note Lighthouse seule ne prouve pas un problème réel.

## Fusion de pages (avant de recommander une redirection 301)
Fusionner seulement si **toutes** ces conditions sont réunies :
1. Même intention et recouvrement SERP ≥ 3.
2. L'une des pages n'a pas de rôle propre (offre, audience, format).
3. Les clics, backlinks et conversions de chaque page ont été relevés.
4. La page conservée est celle qui a le plus de signaux, ou la meilleure URL.
5. Le contenu utile de la page supprimée est réintégré.

## Données structurées : état connu à vérifier
- Les résultats enrichis FAQ sont réservés depuis 2023 à des sites gouvernementaux et de santé faisant autorité ; HowTo n'est plus affiché. Ne pas les promettre.
- Toujours revérifier la documentation Google Search Central en vigueur avant de recommander un type pour un résultat enrichi.

## Volumes
- Volume absent ou à 0 dans Keyword Planner ≠ pas de demande. Croiser avec GSC, les suggestions et les questions clients.
- Ne jamais transformer un volume en trafic prévu sans méthode explicite (ex. hypothèse de CTR par position, présentée comme [Estimé], avec une fourchette).
