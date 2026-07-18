# Étude de convergence du maillage — validation ANSYS v2

## 1. Objectif

Cette étude vérifie que les résultats du modèle éléments finis ne dépendent plus significativement de la taille du maillage.

Trois tailles d’éléments quadratiques structurés ont été étudiées :

- 50 mm ;
- 25 mm ;
- 12,5 mm.

Les grandeurs principales étudiées sont :

- le déplacement directionnel suivant l’axe Z ;
- la déformation totale ;
- la contrainte normale suivant l’axe X ;
- la contrainte équivalente de von Mises ;
- la force de réaction à l’encastrement ;
- le moment de réaction à l’encastrement.

## 2. Configuration commune aux trois calculs

### Géométrie

- longueur : 1 000 mm ;
- largeur : 50 mm ;
- hauteur : 100 mm ;
- section rectangulaire pleine.

### Matériau

Aluminium 2024-T3 :

- module de Young : 73 100 MPa ;
- coefficient de Poisson : 0,33 ;
- masse volumique : 2 780 kg/m³ ;
- limite élastique : 320 MPa.

### Conditions aux limites

- encastrement parfait sur la face située à X = 0 ;
- force de 1 000 N suivant la direction négative de Z ;
- force appliquée sur la face libre située à X = 1 000 mm ;
- grands déplacements désactivés ;
- ressorts de faible raideur désactivés ;
- analyse statique linéaire.

## 3. Résultats analytiques de référence

Le calcul analytique selon la théorie d’Euler-Bernoulli donne :

| Grandeur | Valeur analytique |
|---|---:|
| Moment quadratique | 4 166 666,67 mm⁴ |
| Moment maximal | 1 000 000 N·mm |
| Contrainte normale nominale maximale | 12,000 MPa |
| Flèche maximale suivant Z | 1,0944 mm |
| Force de réaction suivant Z | 1 000 N |
| Moment de réaction autour de Y | 1 000 000 N·mm |

## 4. Caractéristiques des maillages

| Taille d’élément | Nombre de nœuds | Nombre d’éléments | Type d’éléments |
|---:|---:|---:|---|
| 50 mm | 393 | 40 | Quadratiques structurés |
| 25 mm | 2 117 | 320 | Quadratiques structurés |
| 12,5 mm | 13 401 | 2 560 | Quadratiques structurés |

Le nombre d’éléments est multiplié par huit à chaque division par deux de la taille du maillage.

## 5. Convergence des déplacements

La valeur utilisée pour comparer le modèle ANSYS au calcul analytique est la valeur absolue du déplacement directionnel suivant Z.

La déformation totale n’est pas utilisée pour cette comparaison, car elle inclut également les faibles composantes de déplacement suivant les autres directions.

| Taille du maillage | Déplacement Z maximal en valeur absolue | Écart absolu avec l’analytique | Écart relatif avec l’analytique | Déformation totale maximale |
|---:|---:|---:|---:|---:|
| 50 mm | 1,0941 mm | 0,0003 mm | 0,027 % | 1,0971 mm |
| 25 mm | 1,0959 mm | 0,0015 mm | 0,137 % | 1,0990 mm |
| 12,5 mm | 1,0968 mm | 0,0024 mm | 0,219 % | 1,0998 mm |

### Variation entre deux maillages successifs

| Passage de maillage | Variation absolue du déplacement Z | Variation relative |
|---|---:|---:|
| 50 mm vers 25 mm | 0,0018 mm | 0,164 % |
| 25 mm vers 12,5 mm | 0,0009 mm | 0,082 % |

La variation entre les deux derniers maillages est inférieure à 0,1 %.

Le déplacement peut donc être considéré comme convergé.

Le léger écart entre la solution éléments finis et la solution analytique reste inférieur à 0,23 %. Cet écart est cohérent avec les différences entre :

- le modèle analytique unidimensionnel d’Euler-Bernoulli ;
- le modèle tridimensionnel solide utilisé dans ANSYS ;
- l’application de la force sur une face complète ;
- la modélisation tridimensionnelle de l’encastrement.

## 6. Résultats des contraintes

| Taille du maillage | Contrainte normale X maximale | Contrainte équivalente de von Mises maximale |
|---:|---:|---:|
| 50 mm | 12,361 MPa | 12,238 MPa |
| 25 mm | 14,515 MPa | 12,525 MPa |
| 12,5 mm | 17,553 MPa | 14,651 MPa |

Les contraintes maximales locales augmentent lorsque le maillage est raffiné.

Cette évolution ne signifie pas que le modèle global diverge. Les valeurs maximales sont relevées au voisinage immédiat des arêtes de l’encastrement parfait.

À cet endroit, l’association de plusieurs éléments produit :

- une discontinuité brutale des déplacements ;
- une concentration locale de contrainte ;
- une forte sensibilité du maximum nodal à la taille des éléments ;
- une possible singularité numérique aux arêtes de l’encastrement.

Les maxima locaux situés exactement sur les arêtes de l’encastrement ne doivent donc pas être utilisés seuls pour valider la contrainte nominale analytique de 12 MPa.

Pour une comparaison plus représentative, une étude complémentaire pourra extraire la contrainte normale :

- sur une section située à une certaine distance de l’encastrement ;
- le long d’un chemin défini dans la poutre ;
- ou en utilisant une valeur moyennée sur une zone éloignée des arêtes.

## 7. Vérification de l’équilibre statique

| Taille du maillage | Réaction suivant Z | Moment principal autour de Y |
|---:|---:|---:|
| 50 mm | 1 000 N | -1 000 000 N·mm |
| 25 mm | 1 000 N | -1 000 000 N·mm |
| 12,5 mm | 1 000 N | -1 000 000 N·mm |
| Valeur analytique en module | 1 000 N | 1 000 000 N·mm |

Les composantes parasites suivant les autres axes sont négligeables devant les composantes principales.

Les résultats confirment donc :

- l’équilibre des forces ;
- l’équilibre des moments ;
- la bonne orientation du chargement ;
- la bonne définition de l’encastrement.

Le signe négatif du moment autour de Y dépend de la convention d’orientation du système de coordonnées ANSYS. Sa valeur absolue correspond exactement au moment analytique.

## 8. Choix du maillage retenu

Le maillage de 25 mm est retenu comme maillage de référence pour l’exploitation courante des déplacements.

Ce choix est justifié par les éléments suivants :

- la différence avec le maillage de 12,5 mm est seulement de 0,082 % pour le déplacement Z ;
- le déplacement est déjà convergé ;
- le maillage de 25 mm utilise 320 éléments contre 2 560 pour le maillage de 12,5 mm ;
- son coût de calcul est donc nettement inférieur ;
- le maillage de 12,5 mm sert de vérification finale de convergence.

Le maillage de 12,5 mm reste utile pour présenter la confirmation de convergence et étudier plus finement les champs locaux.

## 9. Conclusion

L’étude de convergence valide le comportement global du modèle ANSYS.

Les résultats essentiels sont les suivants :

- le déplacement directionnel Z converge vers environ 1,097 mm ;
- l’écart avec la solution analytique reste inférieur à 0,23 % ;
- la variation entre les deux derniers maillages est de 0,082 % ;
- la force de réaction vaut exactement 1 000 N ;
- le moment de réaction vaut exactement 1 000 000 N·mm en valeur absolue ;
- les équilibres statiques sont respectés ;
- les pics de contrainte situés aux arêtes de l’encastrement restent sensibles au maillage.

Le modèle est donc validé pour l’étude de la rigidité globale et du déplacement de la poutre.

Les contraintes locales à proximité immédiate de l’encastrement devront être interprétées avec précaution et pourront faire l’objet d’une étude locale séparée.

## 10. Illustrations

### Maillage de 50 mm

![Maillage de 50 mm](maillage_50mm_v2.png)

### Maillage de 25 mm

![Maillage de 25 mm](maillage_25mm_v2.png)

### Maillage de 12,5 mm

![Maillage de 12,5 mm](maillage_12_5mm_v2.png)