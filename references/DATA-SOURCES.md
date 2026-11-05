# Sources de données : quoi demander, comment lire

Claude Code n'a pas d'accès natif à Google. Deux options :
- **Exports déposés dans `data/raw/`** (option par défaut, toujours possible).
- **Serveurs MCP** (connecteurs Search Console, Google Ads, crawler…) si l'utilisateur en a configuré : vérifier qu'ils sont actifs avant d'y faire appel.

Ne jamais demander de coller un token, mot de passe ou clé API dans le chat. Utiliser OAuth ou des variables d'environnement. Ne jamais versionner un secret.

## Google Search Console
**Export à demander** : rapport Performances, onglets Requêtes et Pages, ou mieux un export requête × page (API, Looker Studio, ou extension d'export).
Colonnes utiles : `query, page, clicks, impressions, ctr, position`, avec la période, le pays et l'appareil.
**Limites à garder en tête** :
- L'export de l'interface est plafonné (environ 1 000 lignes par onglet) ; l'API permet d'aller beaucoup plus loin.
- Les requêtes rares sont anonymisées : la somme des requêtes < total de la propriété.
- La position est une moyenne pondérée par les impressions, pas un rang fixe.
- Les données ont un délai de quelques jours et l'historique couvre environ 16 mois.

## Google Keyword Planner
**Export à demander** : « Découvrir de nouveaux mots-clés » ou « Volume de recherche et prévisions », avec la localisation, la langue, le réseau (Google seul) et la période indiqués.
Format : souvent CSV UTF-16, séparateur tabulation, 2 lignes de titre avant les en-têtes. Le script `.claude/skills/keyword-research/scripts/kp_clean.py` le normalise.
**Limites** :
- Sans dépense publicitaire active, les volumes s'affichent en fourchettes (ex. « 1 k – 10 k »). Le dire et conserver la fourchette.
- Les variantes proches (pluriels, accents, fautes) sont souvent fusionnées sous un même volume.
- « Concurrence » = concurrence des annonceurs, **pas** la difficulté SEO.

## SERP
**Export à demander** : pour chaque mot-clé, le top 10 organique (`keyword, position, url`) avec la date, le pays, la langue et l'appareil. Source : outil SERP tiers, API SERP, ou relevé manuel.
Une SERP change : dater toute observation, et refaire le relevé au-delà de ~3 mois pour une décision d'architecture.

## Crawl
**Export à demander** (Screaming Frog ou équivalent) :
- Liste des URL internes : `url, status, indexability, canonical, title, h1, meta description, word count, crawl depth, inlinks`.
- Liens internes (« All Inlinks ») : `source, destination, anchor, type, link position`.

## CSV / Excel en général
Conserver le fichier source intact, ses en-têtes, son encodage, ses unités et sa période. Ne pas fusionner des colonnes de définitions différentes. Signaler les cellules vides ou incohérentes.
