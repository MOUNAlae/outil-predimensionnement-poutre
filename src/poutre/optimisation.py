"""Recherche discrète de la section admissible."""

import math

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
    CritereDimensionnant,
    DonneesPoutre,
    ResultatOptimisation,
)


def _identifier_critere_dimensionnant(
    taux_utilisation_resistance: float,
    taux_utilisation_rigidite: float,
) -> CritereDimensionnant:
    """Identifie le critère présentant le taux d'utilisation le plus élevé."""

    if math.isclose(
        taux_utilisation_resistance,
        taux_utilisation_rigidite,
        rel_tol=1e-6,
        abs_tol=1e-9,
    ):
        return CritereDimensionnant.MIXTE

    if taux_utilisation_resistance > taux_utilisation_rigidite:
        return CritereDimensionnant.RESISTANCE

    return CritereDimensionnant.RIGIDITE


def _valider_parametres_recherche(
    hauteur_min_mm: int,
    hauteur_max_mm: int,
    pas_mm: int,
) -> None:
    """Valide les bornes et le pas de la recherche discrète."""

    parametres = {
        "hauteur_min_mm": hauteur_min_mm,
        "hauteur_max_mm": hauteur_max_mm,
        "pas_mm": pas_mm,
    }

    for nom, valeur in parametres.items():
        if isinstance(valeur, bool) or not isinstance(valeur, int):
            raise TypeError(f"{nom} doit être un nombre entier.")

        if valeur <= 0:
            raise ValueError(f"{nom} doit être strictement positif.")

    if hauteur_min_mm > hauteur_max_mm:
        raise ValueError(
            "hauteur_min_mm doit être inférieure ou égale à hauteur_max_mm."
        )


def rechercher_hauteur_minimale(
    donnees: DonneesPoutre,
    hauteur_min_mm: int = 10,
    hauteur_max_mm: int = 200,
    pas_mm: int = 1,
) -> ResultatOptimisation | None:
    """Recherche la première hauteur respectant résistance et rigidité.

    Les hauteurs sont parcourues avec des nombres entiers exprimés en
    millimètres. Cette méthode évite les imprécisions de ``numpy.arange``
    lors de la construction de la grille de recherche.

    Args:
        donnees: Données mécaniques et géométriques de la poutre.
        hauteur_min_mm: Première hauteur évaluée, en millimètres.
        hauteur_max_mm: Dernière hauteur autorisée, en millimètres.
        pas_mm: Incrément de recherche, en millimètres.

    Returns:
        Le premier résultat admissible, donc celui de hauteur minimale.
        Retourne ``None`` si aucune hauteur testée n'est admissible.

    Raises:
        TypeError: Si les données ou les paramètres ont un type incorrect.
        ValueError: Si les bornes ou le pas sont invalides.
    """

    if not isinstance(donnees, DonneesPoutre):
        raise TypeError("donnees doit être une instance de DonneesPoutre.")

    _valider_parametres_recherche(
        hauteur_min_mm,
        hauteur_max_mm,
        pas_mm,
    )

    moment_maximal_nm = calculer_moment_maximal(
        donnees.force_n,
        donnees.longueur_m,
    )

    fleche_admissible_m = calculer_fleche_admissible(
        donnees.longueur_m,
        donnees.rapport_fleche,
    )

    for hauteur_mm in range(
        hauteur_min_mm,
        hauteur_max_mm + 1,
        pas_mm,
    ):
        hauteur_m = hauteur_mm / 1000.0

        moment_quadratique_m4 = calculer_moment_quadratique(
            donnees.largeur_m,
            hauteur_m,
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

        facteur_securite = calculer_facteur_securite(
            donnees.materiau.limite_elastique_pa,
            contrainte_maximale_pa,
        )

        taux_utilisation_resistance = (
            donnees.facteur_securite_minimal / facteur_securite
        )

        taux_utilisation_rigidite = fleche_maximale_m / fleche_admissible_m

        if taux_utilisation_resistance > 1.0 or taux_utilisation_rigidite > 1.0:
            continue

        volume_m3 = calculer_volume(
            donnees.longueur_m,
            donnees.largeur_m,
            hauteur_m,
        )

        masse_kg = calculer_masse(
            donnees.materiau.masse_volumique_kg_m3,
            volume_m3,
        )

        critere_dimensionnant = _identifier_critere_dimensionnant(
            taux_utilisation_resistance,
            taux_utilisation_rigidite,
        )

        return ResultatOptimisation(
            hauteur_mm=hauteur_mm,
            moment_quadratique_m4=moment_quadratique_m4,
            volume_m3=volume_m3,
            masse_kg=masse_kg,
            contrainte_maximale_pa=contrainte_maximale_pa,
            fleche_maximale_m=fleche_maximale_m,
            fleche_admissible_m=fleche_admissible_m,
            facteur_securite=facteur_securite,
            taux_utilisation_resistance=taux_utilisation_resistance,
            taux_utilisation_rigidite=taux_utilisation_rigidite,
            critere_dimensionnant=critere_dimensionnant,
        )

    return None
