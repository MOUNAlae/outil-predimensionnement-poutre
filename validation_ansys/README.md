# Validation par ANSYS Mechanical

Ce dossier regroupe les résultats de validation du modèle analytique Python par une analyse statique linéaire réalisée sous ANSYS Mechanical.

## Cas étudié

- Longueur : 1 000 mm
- Largeur : 50 mm
- Hauteur : 100 mm
- Force appliquée : 1 000 N suivant l’axe Z
- Matériau : Aluminium 2024-T3
- Module de Young : 73,1 GPa
- Coefficient de Poisson : 0,33
- Limite élastique utilisée : 320 MPa

## Étude de convergence

Trois tailles de maillage ont été étudiées :

- 50 mm : 393 nœuds et 40 éléments
- 25 mm : 2 117 nœuds et 320 éléments
- 12,5 mm : 13 401 nœuds et 2 560 éléments

Le maillage de 25 mm a été retenu comme compromis entre la précision de la réponse globale et le coût de calcul.

## Comparaison Python–ANSYS

### Calcul analytique Python

- Flèche maximale : 1,0944 mm
- Contrainte nominale de flexion : 12,00 MPa
- Facteur de sécurité : 26,67

### ANSYS — Maillage retenu de 25 mm

- Flèche directionnelle suivant Z : 1,0959 mm
- Déformation totale maximale : 1,099 mm
- Contrainte équivalente maximale : 12,525 MPa
- Réaction suivant Z : 1 000 N
- Facteur de sécurité calculé : environ 25,55

### Écarts principaux

- Écart relatif sur la flèche : environ 0,14 %
- Écart indicatif entre la contrainte analytique et la contrainte équivalente : environ 4,38 %
- Équilibre global : vérifié

## Conclusion

La réponse globale en déplacement est considérée comme convergée. La variation de la flèche entre les maillages de 25 mm et de 12,5 mm est d’environ 0,082 %.

Les contraintes maximales locales au voisinage de l’encastrement augmentent avec le raffinement du maillage. Elles restent sensibles à la modélisation de l’encastrement parfait et sont donc interprétées avec prudence.
