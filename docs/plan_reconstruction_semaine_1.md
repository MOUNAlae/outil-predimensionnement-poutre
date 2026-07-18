# Plan fixe de reconstruction — Semaine 1

Période : du 20 au 26 juillet 2026

## Objectif

Reconstruire un cœur Python propre et indépendant de l'interface tout
en reproduisant exactement les résultats mécaniques de la version initiale.

## Règles fixes

- `projet_poutre_v10.py` reste la version de référence.
- Les calculs internes utilisent exclusivement les unités SI.
- Le cœur de calcul ne dépend ni de Tkinter ni de Matplotlib.
- Chaque module possède une responsabilité unique.
- Chaque résultat est nommé et documenté.
- Chaque étape terminée produit un commit local.
- Aucun changement n'est poussé sur GitHub avant la validation finale.
- Aucun ajout fonctionnel n'est réalisé avant reproduction du cas initial.

## Cas de référence obligatoire

### Entrées

- matériau : Aluminium 2024-T3 ;
- longueur : 1,00 m ;
- largeur : 0,05 m ;
- hauteur initiale : 0,10 m ;
- force : 1000 N ;
- facteur de sécurité minimal : 2 ;
- flèche admissible : L/250.

### Résultats initiaux attendus

- volume : 0,005000 m³ ;
- masse : 13,90 kg ;
- moment quadratique : 4,166667e-06 m⁴ ;
- moment maximal : 1000,00 N·m ;
- contrainte maximale : 12,00 MPa ;
- flèche maximale : 1,094 mm ;
- facteur de sécurité : 26,67.

### Résultats optimisés attendus

- hauteur : 65,0 mm ;
- masse : 9,03 kg ;
- contrainte maximale : 28,40 MPa ;
- flèche maximale : 3,985 mm ;
- facteur de sécurité : 11,27 ;
- gain de masse : 35,0 %.

## Lundi 20 juillet — formules RDM principales

Horaire : 19 h 30 à 21 h 30.

Travail :

- implémenter le moment quadratique ;
- implémenter le moment maximal ;
- implémenter la contrainte maximale ;
- implémenter la flèche maximale ;
- ajouter les unités et les hypothèses dans les docstrings ;
- conserver des fonctions indépendantes de l'interface.

Livrable : première version de `src/poutre/calculs.py`.

## Mardi 21 juillet — calculs complémentaires

Horaire : 19 h 30 à 21 h 30.

Travail :

- implémenter le volume ;
- implémenter la masse ;
- implémenter le facteur de sécurité ;
- implémenter la flèche admissible ;
- comparer les résultats avec le cas de référence ;
- corriger tout écart avant de continuer.

Livrable : cœur de calcul complet et reproductible.

## Mercredi 22 juillet — matériaux et données

Horaire : 19 h 30 à 21 h 30.

Travail :

- créer un modèle structuré pour un matériau ;
- documenter le module de Young, la limite élastique et la densité ;
- créer l'aluminium 2024-T3 ;
- créer l'acier de construction ;
- créer un modèle pour les données d'entrée ;
- refuser les valeurs non finies, nulles ou négatives.

Livrables :

- `src/poutre/materiaux.py` ;
- `src/poutre/modeles.py`.

## Jeudi 23 juillet — optimisation

Horaire : 19 h 30 à 21 h 30.

Travail :

- reconstruire la recherche de hauteur minimale ;
- utiliser des hauteurs entières en millimètres ;
- rendre les bornes et le pas configurables ;
- retourner un résultat nommé ;
- identifier le critère dimensionnant ;
- gérer explicitement l'absence de solution.

Livrable : `src/poutre/optimisation.py`.

## Vendredi 24 juillet — résultat initial et optimisé

Horaire : 20 h 00 à 21 h 30.

Travail :

- regrouper les résultats dans des objets structurés ;
- comparer la section initiale et la section optimisée ;
- calculer le gain de masse ;
- préparer un affichage indépendant de Tkinter ;
- vérifier une nouvelle fois le cas de référence.

Livrable : comparaison initiale/optimisée reproductible.

## Samedi 25 juillet — vérifications automatiques

Horaires :

- 09 h 00 à 12 h 00 ;
- 15 h 00 à 17 h 00.

Travail :

- vérifier chaque formule indépendamment ;
- vérifier le cas de référence complet ;
- vérifier la hauteur optimisée de 65 mm ;
- vérifier les entrées invalides ;
- vérifier le cas sans solution ;
- produire un rapport de couverture.

Livrables :

- `tests/test_calculs.py` ;
- `tests/test_optimisation.py`.

## Dimanche 26 juillet — intégration et documentation

Horaire : 09 h 00 à 12 h 00.

Travail :

- exécuter toutes les vérifications ;
- corriger les derniers écarts ;
- nettoyer la structure du projet ;
- actualiser le README ;
- comparer l'ancienne et la nouvelle version ;
- créer le commit stable de fin de semaine.

## Définition de terminé

La Semaine 1 est terminée uniquement si :

- l'ancienne application fonctionne toujours ;
- le nouveau cœur est indépendant de l'interface ;
- le cas de référence est reproduit ;
- la hauteur optimisée reste égale à 65 mm ;
- toutes les vérifications automatiques réussissent ;
- les unités et hypothèses sont documentées ;
- le dépôt ne contient aucun fichier temporaire ;
- le README permet de comprendre et d'exécuter le projet.