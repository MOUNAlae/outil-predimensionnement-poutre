# Configuration du modèle statique ANSYS — validation v2

## 1. Objectif

Ce document décrit la configuration du modèle ANSYS Mechanical utilisé pour valider indépendamment l’outil Python de pré-dimensionnement d’une poutre encastrée.

Le modèle numérique reproduit le cas analytique suivant :

- poutre droite à section rectangulaire constante ;
- encastrement à l’extrémité `X = 0 mm` ;
- force verticale appliquée à l’extrémité libre `X = 1000 mm` ;
- matériau Aluminium 2024-T3 ;
- analyse statique linéaire en petites déformations.

## 2. Géométrie de référence

La poutre possède les dimensions suivantes :

| Paramètre | Valeur |
|---|---:|
| Longueur suivant X | 1000 mm |
| Largeur suivant Y | 50 mm |
| Hauteur suivant Z | 100 mm |
| Volume | 5 000 000 mm³ |
| Masse | 13,90 kg |

Le modèle contient un seul corps solide.

Le repère global est défini de la manière suivante :

- axe X : direction longitudinale de la poutre ;
- axe Y : direction de la largeur ;
- axe Z : direction de la hauteur et du chargement.

## 3. Matériau

Le matériau affecté au corps est :

**Aluminium 2024-T3 — validation v2**

| Propriété | Valeur |
|---|---:|
| Module de Young | 73 100 MPa |
| Coefficient de Poisson | 0,33 |
| Limite élastique | 320 MPa |
| Masse volumique | 2780 kg/m³ |

Le comportement retenu est homogène, isotrope et linéaire élastique.

La limite élastique est uniquement utilisée pour calculer un facteur de sécurité indicatif. Aucun comportement plastique n’est activé.

## 4. Type d’analyse

L’analyse utilisée est une **Structure statique** avec le solveur Mechanical APDL.

Les réglages retenus sont :

| Réglage | Valeur |
|---|---|
| Nombre d’étapes | 1 |
| Temps final | 1 s |
| Pas de temps automatique | Contrôlé par le programme |
| Type de solveur | Contrôlé par le programme |
| Ressorts de faible raideur | Désactivés |
| Grands déplacements | Désactivés |
| Équilibre dynamique | Désactivé |
| Solution quasi-statique | Désactivée |
| Gravité | Non appliquée |

Le temps de `1 s` est un paramètre pseudo-temporel du chargement statique. Il ne représente pas une étude dynamique.

Les grands déplacements sont désactivés, car la flèche analytique attendue est faible devant la longueur :

$$
\frac{\delta_{\max}}{L}
=
\frac{1{,}0944}{1000}
=
0{,}0010944
$$

Cela représente environ `0,109 %` de la longueur.

## 5. Conditions aux limites

### 5.1 Encastrement

Le nom utilisé dans ANSYS est :

`Encastrement_X0`

L’encastrement est appliqué sur la face située à :

`X = 0 mm`

La condition impose des déplacements nuls suivant les trois directions globales sur cette face :

$$
U_X = U_Y = U_Z = 0
$$

### 5.2 Chargement

Le nom utilisé dans ANSYS est :

`Force_Z_-1000N_X1000`

La force est appliquée sur la face libre située à :

`X = 1000 mm`

Elle est définie dans le système de coordonnées global avec les composantes suivantes :

| Composante | Valeur |
|---|---:|
| Force X | 0 N |
| Force Y | 0 N |
| Force Z | -1000 N |

Il s’agit d’une force totale répartie sur la face d’extrémité, et non d’une pression.

La gravité et le poids propre ne sont pas pris en compte afin de reproduire exactement le modèle analytique de référence.

## 6. Résultats demandés

Les résultats suivants ont été ajoutés sous l’objet `Solution`.

### 6.1 Déformation directionnelle suivant Z

Nom dans ANSYS :

`Deformation_directionnelle_Z`

Ce résultat sera utilisé pour comparer la flèche numérique à la valeur analytique attendue :

$$
\delta_{\max} = -1{,}0944\ \text{mm}
$$

Le signe attendu est négatif suivant l’axe global Z.

### 6.2 Déformation totale

Nom dans ANSYS :

`Deformation_totale`

Elle permet de visualiser la forme déformée globale et de vérifier que la déformation maximale se situe à l’extrémité libre.

### 6.3 Contrainte équivalente de von Mises

Nom dans ANSYS :

`Contrainte_equivalente_von_Mises`

Cette contrainte est conservée comme résultat complémentaire.

La valeur maximale obtenue au voisinage de l’encastrement devra être interprétée avec prudence, car une concentration de contraintes et une sensibilité au maillage peuvent apparaître au bord du support fixe.

### 6.4 Contrainte normale suivant X

Nom dans ANSYS :

`Contrainte_normale_X`

Ce résultat est directement comparable à la contrainte normale de flexion calculée analytiquement :

$$
\sigma_{\max} = 12{,}00\ \text{MPa}
$$

### 6.5 Force de réaction

Nom dans ANSYS :

`Reaction_force_X0`

La force de réaction est évaluée sur la condition :

`Encastrement_X0`

La valeur analytique de référence en module est :

$$
R_Z = 1000\ \text{N}
$$

Son signe doit être opposé à celui de la force appliquée.

### 6.6 Moment de réaction

Nom dans ANSYS :

`Reaction_moment_X0`

Le moment de réaction est également évalué sur l’encastrement.

La valeur analytique de référence en module est :

$$
M = F L
$$

$$
M = 1000 \times 1000
= 1\,000\,000\ \mathrm{N\,mm}
$$

Le moment principal est attendu autour de l’axe global Y. Son signe dépend de la convention utilisée par ANSYS.

## 7. Valeurs analytiques de référence

| Grandeur | Valeur attendue |
|---|---:|
| Moment quadratique | 4 166 666,67 mm⁴ |
| Moment maximal | 1 000 000 N·mm |
| Contrainte normale maximale | 12,00 MPa |
| Flèche maximale | 1,0944 mm |
| Force de réaction | 1000 N |
| Moment de réaction | 1 000 000 N·mm |
| Facteur de sécurité indicatif | 26,67 |

Ces résultats serviront de références pour la comparaison avec les résultats obtenus par éléments finis.

## 8. Contrôles effectués avant le maillage

Les contrôles suivants ont été réalisés :

- présence d’un seul corps solide ;
- dimensions `1000 × 50 × 100 mm` vérifiées ;
- volume et masse conformes ;
- matériau Aluminium 2024-T3 correctement affecté ;
- encastrement appliqué uniquement sur la face `X = 0 mm` ;
- force appliquée uniquement sur la face `X = 1000 mm` ;
- force orientée suivant `-Z` ;
- absence de gravité ;
- grands déplacements désactivés ;
- ressorts de faible raideur désactivés ;
- résultats de déplacement, contrainte et réactions ajoutés ;
- modèle non encore maillé et non encore résolu.

## 9. Captures de vérification

### 9.1 Réglages de l’analyse linéaire

![Réglages de l’analyse linéaire](reglages_analyse_lineaire.png)

### 9.2 Conditions aux limites

![Conditions aux limites](conditions_limites_reference.png)

### 9.3 Résultats demandés

![Résultats demandés](resultats_demandes.png)

## 10. Étape suivante

L’étape suivante consistera à définir le maillage de référence puis à réaliser une étude de convergence avec plusieurs tailles d’éléments.

Aucune conclusion sur la précision du modèle éléments finis ne sera formulée avant l’étude de convergence du maillage.