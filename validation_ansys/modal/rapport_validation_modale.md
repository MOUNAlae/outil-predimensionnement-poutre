# Validation modale analytique et numérique

## 1. Objectif

Cette étude compare les fréquences propres analytiques d’une poutre encastrée-libre avec les fréquences obtenues sous ANSYS Mechanical.

L’objectif est de :

- vérifier la cohérence dynamique du modèle éléments finis ;
- identifier les principaux modes de flexion, de torsion et de traction ;
- quantifier les écarts entre le modèle analytique Python et ANSYS ;
- préciser les limites de la théorie d’Euler-Bernoulli aux fréquences élevées.

## 2. Configuration du modèle

### Géométrie

- longueur : 1 000 mm ;
- largeur : 50 mm ;
- hauteur : 100 mm ;
- section rectangulaire pleine.

### Matériau

Aluminium 2024-T3 :

- module de Young : 73 100 MPa ;
- coefficient de Poisson : 0,33 ;
- masse volumique : 2 780 kg/m³.

### Conditions aux limites

- face située à X = 0 mm totalement encastrée ;
- extrémité située à X = 1 000 mm libre ;
- aucune charge extérieure ;
- aucune précontrainte ;
- amortissement non pris en compte.

### Modèle numérique

- analyse : modale linéaire ;
- solveur : contrôlé par le programme ;
- nombre de modes extraits : 10 ;
- maillage partagé avec l’analyse statique ;
- taille d’élément nominale : 25 mm.

## 3. Modèle analytique Python

Pour une poutre uniforme encastrée-libre, les fréquences propres de flexion sont calculées par :

$$
f_n =
\frac{\beta_n^2}{2\pi L^2}
\sqrt{\frac{EI}{\rho A}}
$$

avec :

- $f_n$ : fréquence propre du mode $n$ ;
- $\beta_n$ : coefficient modal de la poutre encastrée-libre ;
- $L$ : longueur de la poutre ;
- $E$ : module de Young ;
- $I$ : moment quadratique suivant l’axe de flexion ;
- $\rho$ : masse volumique ;
- $A$ : aire de la section.

Les coefficients utilisés sont :

| Mode de flexion | Coefficient $\beta_n$ |
|---:|---:|
| 1 | 1,875104 |
| 2 | 4,694091 |
| 3 | 7,854757 |
| 4 | 10,995541 |

Le modèle analytique est implémenté dans :

```text
src/poutre/modal.py
```

et vérifié automatiquement dans :

```text
tests/test_modal.py
```

## 4. Résultats ANSYS

| Mode ANSYS | Fréquence | Nature identifiée |
|---:|---:|---|
| 1 | 41,6005 Hz | première flexion suivant l’axe faible |
| 2 | 82,5370 Hz | première flexion suivant l’axe fort |
| 3 | 257,700 Hz | deuxième flexion suivant l’axe faible |
| 4 | 494,739 Hz | deuxième flexion suivant l’axe fort |
| 5 | 589,546 Hz | premier mode de torsion |
| 6 | 708,952 Hz | troisième flexion suivant l’axe faible |
| 7 | 1 285,730 Hz | premier mode axial |
| 8 | 1 301,740 Hz | troisième flexion suivant l’axe fort |
| 9 | 1 355,920 Hz | quatrième flexion suivant l’axe faible |
| 10 | 1 770,840 Hz | deuxième mode de torsion |

## 5. Comparaison Python–ANSYS

L’écart relatif est calculé par :

$$
\varepsilon =
\frac{\left|f_{\mathrm{ANSYS}}-f_{\mathrm{Python}}\right|}
{f_{\mathrm{Python}}}
\times 100
$$

| Mode de flexion | Axe | Python | ANSYS | Écart relatif |
|---:|---|---:|---:|---:|
| 1 | faible | 41,4178 Hz | 41,6005 Hz | 0,441 % |
| 1 | fort | 82,8355 Hz | 82,5370 Hz | 0,360 % |
| 2 | faible | 259,5606 Hz | 257,700 Hz | 0,717 % |
| 2 | fort | 519,1213 Hz | 494,739 Hz | 4,697 % |
| 3 | faible | 726,7773 Hz | 708,952 Hz | 2,453 % |
| 3 | fort | 1 453,5546 Hz | 1 301,740 Hz | 10,444 % |
| 4 | faible | 1 424,1935 Hz | 1 355,920 Hz | 4,794 % |

Les modes de torsion et le mode axial ne sont pas comparés au modèle Python actuel, limité aux fréquences de flexion calculées selon la théorie d’Euler-Bernoulli.

## 6. Interprétation des résultats

Les trois premières comparaisons présentent des écarts inférieurs à 1 %. Le modèle analytique et le modèle éléments finis sont donc très cohérents pour les premiers modes de flexion.

L’écart augmente pour les modes supérieurs. Le cas le plus marqué concerne la troisième flexion suivant l’axe fort, avec un écart d’environ 10,44 %.

Cette augmentation peut notamment être expliquée par les limites du modèle analytique utilisé :

- déformation due au cisaillement négligée ;
- inertie de rotation négligée ;
- comportement tridimensionnel de la section non représenté ;
- effets locaux de l’encastrement non représentés ;
- sensibilité plus importante des modes élevés au maillage.

Les modes 5 et 10 correspondent à des déformations principalement torsionnelles.

Le mode 7 correspond à une vibration axiale. Son identification est confirmée par sa forme modale et par sa participation dominante suivant l’axe longitudinal X.

## 7. Précautions d’interprétation

Les amplitudes affichées par ANSYS pour les formes modales sont normalisées.

Elles ne représentent donc pas des déplacements physiques réels sous un chargement donné. Seules les informations suivantes doivent être interprétées :

- la fréquence propre ;
- la forme de vibration ;
- le nombre de nœuds modaux ;
- la direction dominante du mouvement ;
- la nature du mode.

Une analyse harmonique ou transitoire serait nécessaire pour calculer des amplitudes réelles sous une excitation imposée.

## 8. Illustrations des modes

- [Mode 1 — flexion axe faible](mode_01_flexion_axe_faible.png)
- [Mode 2 — flexion axe fort](mode_02_flexion_axe_fort.png)
- [Mode 3 — flexion axe faible](mode_03_flexion_axe_faible.png)
- [Mode 4 — flexion axe fort](mode_04_flexion_axe_fort.png)
- [Mode 5 — torsion](mode_05_torsion.png)
- [Mode 6 — flexion axe faible](mode_06_flexion_axe_faible.png)
- [Mode 7 — axial](mode_07_axial.png)
- [Mode 8 — flexion axe fort](mode_08_flexion_axe_fort.png)
- [Mode 9 — flexion axe faible](mode_09_flexion_axe_faible.png)
- [Mode 10 — torsion](mode_10_torsion.png)

Les valeurs numériques sont également disponibles dans :

```text
validation_ansys/modal/frequences_modales.csv
```

## 9. Conclusion

L’analyse modale confirme la cohérence dynamique du modèle de poutre encastrée.

Les premiers modes de flexion obtenus sous ANSYS sont très proches des valeurs analytiques Python, avec des écarts inférieurs à 1 % pour les trois premières comparaisons.

Les écarts augmentent pour les modes supérieurs, ce qui montre que la théorie d’Euler-Bernoulli reste adaptée au pré-dimensionnement des premiers modes, mais devient moins précise lorsque les effets de cisaillement, l’inertie de rotation et le comportement tridimensionnel deviennent significatifs.

La validation modale complète ainsi la validation statique et l’étude de convergence du maillage.