"""Coordination du calcul initial et de l'optimisation de la poutre."""

from .calculs import (
    calculer_contrainte_maximale,
    calculer_facteur_securite,
    calculer_fleche_admissible,
    calculer_fleche_maximale,
    calculer_masse,
    calculer_moment_maximal,
    calculer_moment_quadratique,
    calculer_volume,
)
from .modeles import (
    DonneesPoutre,
    ResultatDimensionnement,
    ResultatSection,
)
from .optimisation import rechercher_hauteur_minimale


def evaluer_section(
    donnees: DonneesPoutre,
    hauteur_m: float,
) -> ResultatSection:
    """Calcule tous les résultats mécaniques pour une hauteur donnée."""

    if not isinstance(donnees, DonneesPoutre):
        raise TypeError("donnees doit être une instance de DonneesPoutre.")

    moment_quadratique_m4 = calculer_moment_quadratique(
        donnees.largeur_m,
        hauteur_m,
    )

    moment_maximal_nm = calculer_moment_maximal(
        donnees.force_n,
        donnees.longueur_m,
    )

    contrainte_maximale_pa = calculer_contrainte_maximale(
        moment_maximal_nm,
        hauteur_m,
        moment_quadratique_m4,
    )

    fleche_maximale_m = calculer_fleche_maximale(
        donnees.force_n,
        donnees.longueur_m,
        donnees.materiau.module_young_pa,
        moment_quadratique_m4,
    )

    fleche_admissible_m = calculer_fleche_admissible(
        donnees.longueur_m,
        donnees.rapport_fleche,
    )

    volume_m3 = calculer_volume(
        donnees.longueur_m,
        donnees.largeur_m,
        hauteur_m,
    )

    masse_kg = calculer_masse(
        donnees.materiau.masse_volumique_kg_m3,
        volume_m3,
    )

    facteur_securite = calculer_facteur_securite(
        donnees.materiau.limite_elastique_pa,
        contrainte_maximale_pa,
    )

    return ResultatSection(
        hauteur_m=hauteur_m,
        moment_quadratique_m4=moment_quadratique_m4,
        moment_maximal_nm=moment_maximal_nm,
        volume_m3=volume_m3,
        masse_kg=masse_kg,
        contrainte_maximale_pa=contrainte_maximale_pa,
        fleche_maximale_m=fleche_maximale_m,
        fleche_admissible_m=fleche_admissible_m,
        facteur_securite=facteur_securite,
        facteur_securite_minimal=donnees.facteur_securite_minimal,
    )


def dimensionner_poutre(
    donnees: DonneesPoutre,
    hauteur_min_mm: int = 10,
    hauteur_max_mm: int = 200,
    pas_mm: int = 1,
) -> ResultatDimensionnement:
    """Évalue la section initiale puis recherche la hauteur minimale."""

    if not isinstance(donnees, DonneesPoutre):
        raise TypeError("donnees doit être une instance de DonneesPoutre.")

    section_initiale = evaluer_section(
        donnees,
        donnees.hauteur_initiale_m,
    )

    optimisation = rechercher_hauteur_minimale(
        donnees,
        hauteur_min_mm=hauteur_min_mm,
        hauteur_max_mm=hauteur_max_mm,
        pas_mm=pas_mm,
    )

    return ResultatDimensionnement(
        section_initiale=section_initiale,
        optimisation=optimisation,
    )