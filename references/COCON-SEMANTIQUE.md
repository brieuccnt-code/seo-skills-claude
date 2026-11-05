# Méthode du cocon sémantique

Le cocon sémantique est une méthode d'architecture et de maillage popularisée dans le SEO francophone (Laurent Bourrelly). Ce n'est pas un concept officiel de Google : c'est une manière d'organiser des pages pour qu'elles répondent au parcours de recherche de l'internaute et se renforcent mutuellement.

## Vocabulaire
- **Page cible** : la page qu'on veut faire progresser (souvent une page business ou un pilier).
- **Page mère** : page qui couvre un besoin large et oriente vers des besoins plus précis.
- **Pages filles** : pages qui traitent chacune un sous-besoin de la mère.
- **Pages sœurs** : filles d'une même mère.
- **Pages petites-filles** : niveau suivant, pour un besoin encore plus précis.

## Construire le cocon
1. Partir de la requête de la page cible et lister les **intentions qui la précèdent ou la précisent** : questions, comparaisons, étapes, contextes, publics, objections.
2. Regrouper ces intentions (skill `keyword-clustering`). Chaque cluster valide = une page candidate.
3. Hiérarchiser : du plus général (mère) au plus précis (filles, petites-filles). Le parcours doit sembler naturel à un lecteur.
4. Vérifier que chaque page a une raison d'exister par elle-même (intention propre, recouvrement SERP faible avec ses sœurs).
5. Limiter la largeur : en pratique 3 à 8 filles par mère, au-delà créer un niveau intermédiaire.
6. Dessiner le cocon (tableau `templates/cocon-map.csv`) avant d'écrire une seule page.

## Règles de maillage
| Type de lien | Règle |
|---|---|
| Mère → filles | Obligatoire, dans le corps du texte, contexte pertinent. |
| Fille → mère | Obligatoire (lien montant), de préférence tôt dans le texte. |
| Fille → sœurs | Recommandé quand le lecteur en a besoin (étape suivante, alternative). Pas obligatoire vers toutes les sœurs. |
| Fille → petites-filles | Obligatoire si elles existent. |
| Vers un autre cocon | À éviter dans le corps du texte, sauf lien vraiment utile au lecteur. Passer plutôt par la page mère ou la page cible. |
| Navigation, footer, breadcrumb | Ne cassent pas le cocon mais diluent le signal : rester sobre, garder le fil d'Ariane. |

## Ancres
- L'ancre décrit la page de destination, avec sa requête principale ou une variante naturelle.
- Varier les ancres d'une page source à l'autre : pas la même ancre exacte partout.
- Jamais « cliquez ici », « en savoir plus » seuls.

## Champ lexical
Chaque page du cocon emploie le vocabulaire de son sujet (entités, termes associés, questions) tel qu'il ressort des pages qui se classent et des questions réelles des internautes. Ne pas chercher un score de « densité » : vérifier que la page couvre les sous-sujets attendus.

## Contrôle d'un cocon existant
Le script `.claude/skills/cocon-semantique/scripts/link_graph.py` compare un export de liens internes à la carte du cocon et liste :
- liens obligatoires manquants (mère → fille, fille → mère) ;
- liens qui sortent du cocon depuis le corps du texte ;
- pages orphelines et profondeur de clic.

## Limites
- Un cocon ne compense pas un contenu faible ou une offre peu pertinente.
- Sur un site existant, réorganiser le maillage est moins risqué que changer les URL. Ne jamais changer d'URL pour « faire entrer » une page dans un cocon sans validation.
