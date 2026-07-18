"""Fonctions de calcul RDM indépendantes de l'interface."""

import math


def _verifier_valeur_positive(nom: str, valeur: float) -> None:
    """Vérifie qu'une donnée est finie et strictement positive."""
    if not math.isfinite(valeur) or valeur <= 0:
        raise ValueError(f"{nom} doit être un nombre fini strictement positif.")


def calculer_moment_quadratique(
    largeur_m: float,
    hauteur_m: float,
) -> float:
    """Calcule le moment quadratique d'une section rectangulaire pleine.

    La flexion est réalisée autour de l'axe neutre parallèle à la largeur.

    Args:
        largeur_m: Largeur de la section en mètres.
        hauteur_m: Hauteur de la section en mètres.

    Returns:
        Moment quadratique en mètres puissance quatre.

    Raises:
        ValueError: Si une dimension est nulle, négative ou non finie.
    """
    _verifier_valeur_positive("largeur_m", largeur_m)
    _verifier_valeur_positive("hauteur_m", hauteur_m)

    return largeur_m * hauteur_m**3 / 12.0


def calculer_moment_maximal(
    force_n: float,
    longueur_m: float,
) -> float:
    """Calcule le moment maximal d'une poutre encastrée.

    Le modèle suppose une force ponctuelle perpendiculaire appliquée
    à l'extrémité libre de la poutre.

    Args:
        force_n: Force appliquée en newtons.
        longueur_m: Longueur de la poutre en mètres.

    Returns:
        Moment maximal à l'encastrement en newtons-mètres.

    Raises:
        ValueError: Si la force ou la longueur est non valide.
    """
    _verifier_valeur_positive("force_n", force_n)
    _verifier_valeur_positive("longueur_m", longueur_m)

    return force_n * longueur_m


def calculer_contrainte_maximale(
    moment_maximal_nm: float,
    hauteur_m: float,
    moment_quadratique_m4: float,
) -> float:
    """Calcule la contrainte normale maximale de flexion.

    La formule de Navier est appliquée sur la fibre la plus éloignée
    de l'axe neutre d'une section rectangulaire.

    Args:
        moment_maximal_nm: Moment maximal en newtons-mètres.
        hauteur_m: Hauteur de la section en mètres.
        moment_quadratique_m4: Moment quadratique en mètres puissance quatre.

    Returns:
        Contrainte maximale de flexion en pascals.

    Raises:
        ValueError: Si une donnée est nulle, négative ou non finie.
    """
    _verifier_valeur_positive("moment_maximal_nm", moment_maximal_nm)
    _verifier_valeur_positive("hauteur_m", hauteur_m)
    _verifier_valeur_positive(
        "moment_quadratique_m4",
        moment_quadratique_m4,
    )

    distance_fibre_extreme_m = hauteur_m / 2.0

    return moment_maximal_nm * distance_fibre_extreme_m / moment_quadratique_m4


def calculer_fleche_maximale(
    force_n: float,
    longueur_m: float,
    module_young_pa: float,
    moment_quadratique_m4: float,
) -> float:
    """Calcule la flèche maximale d'une poutre encastrée.

    Le modèle suppose une section constante, un comportement élastique
    linéaire, de petites déformations et une force ponctuelle appliquée
    à l'extrémité libre. La théorie d'Euler-Bernoulli est utilisée.

    Args:
        force_n: Force appliquée en newtons.
        longueur_m: Longueur de la poutre en mètres.
        module_young_pa: Module de Young en pascals.
        moment_quadratique_m4: Moment quadratique en mètres puissance quatre.

    Returns:
        Flèche maximale à l'extrémité libre en mètres.

    Raises:
        ValueError: Si une donnée est nulle, négative ou non finie.
    """
    _verifier_valeur_positive("force_n", force_n)
    _verifier_valeur_positive("longueur_m", longueur_m)
    _verifier_valeur_positive("module_young_pa", module_young_pa)
    _verifier_valeur_positive(
        "moment_quadratique_m4",
        moment_quadratique_m4,
    )

    return force_n * longueur_m**3 / (3.0 * module_young_pa * moment_quadratique_m4)


def calculer_volume(
    longueur_m: float,
    largeur_m: float,
    hauteur_m: float,
) -> float:
    """Calcule le volume d'une poutre rectangulaire pleine.

    La section est supposée constante sur toute la longueur.

    Args:
        longueur_m: Longueur de la poutre en mètres.
        largeur_m: Largeur de la section en mètres.
        hauteur_m: Hauteur de la section en mètres.

    Returns:
        Volume de la poutre en mètres cubes.

    Raises:
        ValueError: Si une dimension est nulle, négative ou non finie.
    """
    _verifier_valeur_positive("longueur_m", longueur_m)
    _verifier_valeur_positive("largeur_m", largeur_m)
    _verifier_valeur_positive("hauteur_m", hauteur_m)

    return longueur_m * largeur_m * hauteur_m


def calculer_masse(
    masse_volumique_kg_m3: float,
    volume_m3: float,
) -> float:
    """Calcule la masse d'une poutre à partir de son volume.

    Args:
        masse_volumique_kg_m3: Masse volumique du matériau en kg/m³.
        volume_m3: Volume de la poutre en mètres cubes.

    Returns:
        Masse de la poutre en kilogrammes.

    Raises:
        ValueError: Si une donnée est nulle, négative ou non finie.
    """
    _verifier_valeur_positive(
        "masse_volumique_kg_m3",
        masse_volumique_kg_m3,
    )
    _verifier_valeur_positive("volume_m3", volume_m3)

    return masse_volumique_kg_m3 * volume_m3


def calculer_facteur_securite(
    limite_elastique_pa: float,
    contrainte_maximale_pa: float,
) -> float:
    """Calcule le facteur de sécurité par rapport à la limite élastique.

    Le modèle considère une contrainte normale de flexion uniaxiale.

    Args:
        limite_elastique_pa: Limite élastique du matériau en pascals.
        contrainte_maximale_pa: Contrainte maximale en pascals.

    Returns:
        Facteur de sécurité sans unité.

    Raises:
        ValueError: Si une donnée est nulle, négative ou non finie.
    """
    _verifier_valeur_positive(
        "limite_elastique_pa",
        limite_elastique_pa,
    )
    _verifier_valeur_positive(
        "contrainte_maximale_pa",
        contrainte_maximale_pa,
    )

    return limite_elastique_pa / contrainte_maximale_pa


def calculer_fleche_admissible(
    longueur_m: float,
    rapport_fleche: float = 250.0,
) -> float:
    """Calcule la flèche admissible selon un rapport longueur/flèche.

    Le rapport utilisé par défaut est L/250. Il s'agit d'un critère
    de service choisi pour le projet, et non d'une loi universelle.

    Args:
        longueur_m: Longueur de la poutre en mètres.
        rapport_fleche: Diviseur du critère de flèche, égal à 250 par défaut.

    Returns:
        Flèche admissible en mètres.

    Raises:
        ValueError: Si la longueur ou le rapport est non valide.
    """
    _verifier_valeur_positive("longueur_m", longueur_m)
    _verifier_valeur_positive("rapport_fleche", rapport_fleche)

    return longueur_m / rapport_fleche
