# Cas de référence avant reconstruction

Date : 17/07/2026
Branche de travail : reconstruction-v1
Commit de départ : ac3d275

## Entrées

- Matériau : Aluminium 2024-T3
- Longueur L : 1,00 m
- Largeur b : 0,05 m
- Hauteur initiale h : 0,10 m
- Force appliquée F : 1000 N
- Facteur de sécurité minimal demandé : 2,00
- Flèche admissible : L/250 = 4,000 mm

## Résultats de la section initiale

- Volume : 0,005000 m³
- Masse : 13,90 kg
- Moment quadratique : 4,166667e-06 m⁴
- Moment maximal : 1000,00 N·m
- Contrainte maximale : 12,00 MPa
- Flèche maximale : 1,094 mm
- Facteur de sécurité : 26,67

Conclusion : le dimensionnement initial est validé.

## Résultats de la section optimisée

- Hauteur minimale : 65,0 mm
- Masse optimisée : 9,03 kg
- Contrainte maximale : 28,40 MPa
- Flèche maximale : 3,985 mm
- Facteur de sécurité : 11,27
- Gain de masse : 4,87 kg
- Gain relatif : 35,0 %

## Conclusion technique

Le critère dimensionnant est la rigidité et non la résistance.

La hauteur minimale de 65 mm est retenue parce que la flèche obtenue,
3,985 mm, est très proche de la limite admissible de 4,000 mm.

En revanche, le facteur de sécurité obtenu reste égal à 11,27,
donc largement supérieur à la valeur minimale demandée de 2,00.
La contrainte mécanique n’est donc pas le critère limitant dans ce cas.