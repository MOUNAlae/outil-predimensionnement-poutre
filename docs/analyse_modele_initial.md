# Analyse du modèle mécanique initial

## Problème étudié

Le programme étudie une poutre rectangulaire pleine, encastrée à une
extrémité et soumise à une force ponctuelle statique à l'extrémité libre.

Toutes les grandeurs utilisées par le cœur de calcul sont exprimées
dans le système international.

## Formules utilisées

### Moment quadratique

I = b h³ / 12

### Moment maximal à l'encastrement

M_max = F L

### Contrainte maximale de flexion

sigma_max = M_max (h / 2) / I

Pour une section rectangulaire :

sigma_max = 6 F L / (b h²)

### Flèche à l'extrémité libre

delta_max = F L³ / (3 E I)

Pour une section rectangulaire :

delta_max = 4 F L³ / (E b h³)

### Volume et masse

V = L b h

m = rho V

### Facteur de sécurité

FS = Re / sigma_max

### Flèche admissible

delta_admissible = L / 250

## Conditions d'acceptation

La section est acceptée si les deux conditions suivantes sont vérifiées :

- FS >= FS_min
- delta_max <= delta_admissible

## Algorithme d'optimisation

Le programme teste les hauteurs de 10 à 200 mm avec un pas de 1 mm.

Pour chaque hauteur, il calcule la contrainte, la flèche et le facteur
de sécurité. Il retourne la première hauteur qui satisfait simultanément
les critères de résistance et de rigidité.

Il s'agit donc d'une recherche discrète de la plus petite hauteur
admissible sur le domaine étudié.

Comme la masse est proportionnelle à la hauteur lorsque le matériau,
la longueur et la largeur sont fixés, la hauteur minimale correspond
également à la masse minimale.

## Cas de référence

Pour l'aluminium 2024-T3 avec :

- L = 1,00 m
- b = 0,05 m
- F = 1000 N
- FS_min = 2
- Re = 320 MPa
- E = 73,1 GPa

la résistance exige environ 27,39 mm, tandis que la rigidité exige
environ 64,9 mm.

Avec un pas de recherche de 1 mm, le programme sélectionne donc 65 mm.

Le critère dimensionnant est la rigidité.

## Hypothèses

- section rectangulaire pleine et constante ;
- matériau homogène, isotrope et linéaire élastique ;
- petites déformations ;
- théorie d'Euler-Bernoulli ;
- charge ponctuelle statique à l'extrémité libre ;
- absence de torsion et de charge axiale ;
- déformation due au cisaillement négligée ;
- effets locaux de l'encastrement négligés.

## Limites de la version initiale

- domaine de recherche codé en dur ;
- pas de recherche non configurable ;
- unités absentes des signatures des fonctions ;
- résultat d'optimisation retourné sous forme de tuple ;
- aucune identification automatique du critère dimensionnant ;
- absence de vérifications automatiques du code.