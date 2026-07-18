"""Calcul analytique des fréquences propres de flexion."""

import math
from dataclasses import dataclass

COEFFICIENTS_BETA_ENCASTREE_LIBRE = (
    1.875104068711961,
    4.694091132974174,
    7.854757438237612,
    10.995540734875467,
)


def _verifier_valeur_positive(nom: str, valeur: float) -> None:
    """Vérifie qu'une valeur est finie et strictement positive."""
    if not math.isfinite(valeur) or valeur <= 0:
        raise ValueError(f"{nom} doit être un nombre fini strictement positif.")


@dataclass(frozen=True)
class FrequencesFlexionRectangle:
    """Fréquences propres de flexion d'une section rectangulaire."""

    axe_faible_hz: tuple[float, ...]
    axe_fort_hz: tuple[float, ...]


def calculer_frequence_flexion(
    coefficient_beta: float,
    longueur_m: float,
    module_young_pa: float,
    masse_volumique_kg_m3: float,
    aire_m2: float,
    moment_quadratique_m4: float,
) -> float:
    """Calcule une fréquence propre de flexion Euler-Bernoulli.

    Le modèle correspond à une poutre uniforme encastrée-libre.

    Args:
        coefficient_beta: Coefficient modal de la poutre encastrée-libre.
        longueur_m: Longueur de la poutre en mètres.
        module_young_pa: Module de Young en pascals.
        masse_volumique_kg_m3: Masse volumique en kilogrammes par mètre cube.
        aire_m2: Aire de la section en mètres carrés.
        moment_quadratique_m4: Moment quadratique en mètres puissance quatre.

    Returns:
        Fréquence propre en hertz.
    """
    _verifier_valeur_positive("coefficient_beta", coefficient_beta)
    _verifier_valeur_positive("longueur_m", longueur_m)
    _verifier_valeur_positive("module_young_pa", module_young_pa)
    _verifier_valeur_positive(
        "masse_volumique_kg_m3",
        masse_volumique_kg_m3,
    )
    _verifier_valeur_positive("aire_m2", aire_m2)
    _verifier_valeur_positive(
        "moment_quadratique_m4",
        moment_quadratique_m4,
    )

    pulsation_rad_s = (
        coefficient_beta**2
        / longueur_m**2
        * math.sqrt(
            module_young_pa * moment_quadratique_m4 / (masse_volumique_kg_m3 * aire_m2)
        )
    )

    return pulsation_rad_s / (2.0 * math.pi)


def calculer_frequences_flexion_rectangle(
    longueur_m: float,
    largeur_m: float,
    hauteur_m: float,
    module_young_pa: float,
    masse_volumique_kg_m3: float,
    nombre_modes: int = 3,
) -> FrequencesFlexionRectangle:
    """Calcule les fréquences de flexion suivant les deux axes principaux."""
    _verifier_valeur_positive("longueur_m", longueur_m)
    _verifier_valeur_positive("largeur_m", largeur_m)
    _verifier_valeur_positive("hauteur_m", hauteur_m)
    _verifier_valeur_positive("module_young_pa", module_young_pa)
    _verifier_valeur_positive(
        "masse_volumique_kg_m3",
        masse_volumique_kg_m3,
    )

    if type(nombre_modes) is not int:
        raise TypeError("nombre_modes doit être un entier.")

    if not 1 <= nombre_modes <= len(COEFFICIENTS_BETA_ENCASTREE_LIBRE):
        raise ValueError(
            "nombre_modes doit être compris entre 1 et "
            f"{len(COEFFICIENTS_BETA_ENCASTREE_LIBRE)}."
        )

    aire_m2 = largeur_m * hauteur_m

    moment_quadratique_axe_fort_m4 = largeur_m * hauteur_m**3 / 12.0
    moment_quadratique_axe_faible_m4 = hauteur_m * largeur_m**3 / 12.0

    coefficients = COEFFICIENTS_BETA_ENCASTREE_LIBRE[:nombre_modes]

    frequences_axe_faible_hz = tuple(
        calculer_frequence_flexion(
            coefficient_beta=coefficient_beta,
            longueur_m=longueur_m,
            module_young_pa=module_young_pa,
            masse_volumique_kg_m3=masse_volumique_kg_m3,
            aire_m2=aire_m2,
            moment_quadratique_m4=moment_quadratique_axe_faible_m4,
        )
        for coefficient_beta in coefficients
    )

    frequences_axe_fort_hz = tuple(
        calculer_frequence_flexion(
            coefficient_beta=coefficient_beta,
            longueur_m=longueur_m,
            module_young_pa=module_young_pa,
            masse_volumique_kg_m3=masse_volumique_kg_m3,
            aire_m2=aire_m2,
            moment_quadratique_m4=moment_quadratique_axe_fort_m4,
        )
        for coefficient_beta in coefficients
    )

    return FrequencesFlexionRectangle(
        axe_faible_hz=frequences_axe_faible_hz,
        axe_fort_hz=frequences_axe_fort_hz,
    )
