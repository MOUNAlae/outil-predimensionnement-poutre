# Protocole de reconstruction et de validation ANSYS

## Identification

- Projet : pré-dimensionnement d’une poutre encastrée
- Séquence : Jour 11 — préparation de la validation ANSYS statique
- Branche Git : `ansys-statique-v2`
- Auteur : Mohamed Alae Mountassir
- Statut : protocole préparatoire
- Système d’unités ANSYS : mm, N, MPa

## 1. Objectif

L’objectif est de reconstruire depuis zéro un modèle éléments finis d’une poutre encastrée, puis de comparer ses résultats avec le modèle analytique Python.

La validation portera principalement sur :

- l’équilibre global ;
- la flèche maximale ;
- la convergence du déplacement ;
- la contrainte de flexion ;
- l’influence du raffinement du maillage ;
- les effets locaux de l’encastrement.

L’ancien modèle ANSYS est conservé uniquement comme référence historique. Les résultats de cette reconstruction devront être obtenus à nouveau et documentés.

## 2. Cas mécanique de référence

La structure étudiée est une poutre droite à section rectangulaire constante.

### Géométrie

| Paramètre | Symbole | Valeur |
|---|---:|---:|
| Longueur | L | 1 000 mm |
| Largeur | b | 50 mm |
| Hauteur | h | 100 mm |
| Section | — | rectangulaire pleine |

### Repère

- axe X : direction longitudinale de la poutre ;
- axe Y : direction de la largeur ;
- axe Z : direction de la hauteur et de la charge ;
- face encastrée : `X = 0 mm` ;
- face chargée : `X = 1 000 mm`.

### Chargement

- type : force statique ponctuelle équivalente appliquée sur la face libre ;
- intensité : `1 000 N` ;
- direction : axe Z ;
- sens : `-Z` ;
- gravité : désactivée ;
- poids propre : négligé.

### Conditions aux limites

- encastrement complet de la face située à `X = 0 mm` ;
- translations bloquées suivant X, Y et Z ;
- rotations implicitement bloquées par l’encastrement de la face ;
- aucune autre liaison.

## 3. Matériau

Le matériau utilisé est l’Aluminium 2024-T3, modélisé comme homogène, isotrope et linéaire élastique.

| Propriété | Symbole | Valeur |
|---|---:|---:|
| Module de Young | E | 73 100 MPa |
| Coefficient de Poisson | ν | 0,33 |
| Limite élastique | Re | 320 MPa |
| Masse volumique | ρ | 2 780 kg/m³ |

La limite élastique sert au calcul indicatif du facteur de sécurité. Aucun comportement plastique ne sera utilisé.

## 4. Résultats analytiques de référence

Pour une section rectangulaire :

$$
I = \frac{b h^3}{12}
$$

Avec `b = 50 mm` et `h = 100 mm` :

$$
I = 4\,166\,666{,}67\ \text{mm}^4
$$

Le moment maximal à l’encastrement est :

$$
M_{\max} = F L
$$

$$
M_{\max} = 1000 \times 1000
= 1\,000\,000\ \mathrm{N\,mm}
$$

La contrainte maximale nominale vaut :

$$
\sigma_{\max} = \frac{M_{\max}h}{2I}
$$

$$
\sigma_{\max} = 12{,}00\ \text{MPa}
$$

La flèche maximale selon Euler-Bernoulli est :

$$
\delta_{\max} = \frac{F L^3}{3EI}
$$

$$
\delta_{\max} = 1{,}0944\ \text{mm}
$$

Le facteur de sécurité analytique vaut :

$$
FS = \frac{R_e}{\sigma_{\max}}
$$

$$
FS = 26{,}67
$$

### Tableau de référence

| Grandeur | Valeur attendue |
|---|---:|
| Moment quadratique | 4 166 666,67 mm⁴ |
| Moment à l’encastrement | 1 000 000 N·mm |
| Contrainte nominale | 12,00 MPa |
| Flèche maximale | 1,0944 mm |
| Réaction verticale | 1 000 N |
| Moment de réaction | 1 000 000 N·mm |
| Facteur de sécurité | 26,67 |

## 5. Type d’analyse ANSYS

Le système utilisé sera :

```text
Static Structural