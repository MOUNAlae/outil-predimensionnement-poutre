"""Vérifications de l'optimisation et du dimensionnement complet."""

import pytest

from poutre.dimensionnement import dimensionner_poutre
from poutre.materiaux import ACIER_CONSTRUCTION, ALUMINIUM_2024_T3
from poutre.modeles import (
    CritereDimensionnant,
    DonneesPoutre,
)
from poutre.optimisation import rechercher_hauteur_minimale


@pytest.fixture
def donnees_aluminium() -> DonneesPoutre:
    """Retourne le cas de référence en aluminium."""

    return DonneesPoutre(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_initiale_m=0.10,
        force_n=1000.0,
        facteur_securite_minimal=2.0,
        materiau=ALUMINIUM_2024_T3,
    )


def test_optimisation_cas_reference(
    donnees_aluminium: DonneesPoutre,
) -> None:
    """La hauteur minimale du cas de référence doit être de 65 mm."""

    resultat = rechercher_hauteur_minimale(donnees_aluminium)

    assert resultat is not None
    assert resultat.hauteur_mm == 65
    assert resultat.masse_kg == pytest.approx(9.035)
    assert resultat.contrainte_maximale_mpa == pytest.approx(
        28.40,
        rel=1e-3,
    )
    assert resultat.fleche_maximale_mm == pytest.approx(
        3.985,
        rel=1e-3,
    )
    assert resultat.facteur_securite == pytest.approx(
        11.27,
        rel=1e-3,
    )
    assert resultat.critere_dimensionnant is CritereDimensionnant.RIGIDITE


def test_aucune_solution_jusqua_64_mm(
    donnees_aluminium: DonneesPoutre,
) -> None:
    """Aucune section ne doit être admissible entre 10 et 64 mm."""

    resultat = rechercher_hauteur_minimale(
        donnees_aluminium,
        hauteur_min_mm=10,
        hauteur_max_mm=64,
        pas_mm=1,
    )

    assert resultat is None


def test_pas_de_deux_millimetres(
    donnees_aluminium: DonneesPoutre,
) -> None:
    """Une grille paire doit sélectionner la hauteur de 66 mm."""

    resultat = rechercher_hauteur_minimale(
        donnees_aluminium,
        hauteur_min_mm=10,
        hauteur_max_mm=200,
        pas_mm=2,
    )

    assert resultat is not None
    assert resultat.hauteur_mm == 66


@pytest.mark.parametrize(
    ("hauteur_min_mm", "hauteur_max_mm", "pas_mm"),
    [
        (0, 200, 1),
        (10, 0, 1),
        (10, 200, 0),
        (100, 50, 1),
    ],
)
def test_parametres_recherche_invalides(
    donnees_aluminium: DonneesPoutre,
    hauteur_min_mm: int,
    hauteur_max_mm: int,
    pas_mm: int,
) -> None:
    """Les bornes incohérentes ou nulles doivent être refusées."""

    with pytest.raises(ValueError):
        rechercher_hauteur_minimale(
            donnees_aluminium,
            hauteur_min_mm=hauteur_min_mm,
            hauteur_max_mm=hauteur_max_mm,
            pas_mm=pas_mm,
        )


@pytest.mark.parametrize(
    ("hauteur_min_mm", "hauteur_max_mm", "pas_mm"),
    [
        (10.0, 200, 1),
        (10, 200.0, 1),
        (10, 200, 1.0),
    ],
)
def test_types_parametres_recherche_invalides(
    donnees_aluminium: DonneesPoutre,
    hauteur_min_mm: float,
    hauteur_max_mm: float,
    pas_mm: float,
) -> None:
    """Les paramètres de grille doivent être des nombres entiers."""

    with pytest.raises(TypeError):
        rechercher_hauteur_minimale(
            donnees_aluminium,
            hauteur_min_mm=hauteur_min_mm,
            hauteur_max_mm=hauteur_max_mm,
            pas_mm=pas_mm,
        )


def test_type_donnees_invalide() -> None:
    """L’optimisation doit refuser un objet autre que DonneesPoutre."""

    with pytest.raises(TypeError):
        rechercher_hauteur_minimale("donnees invalides")


def test_dimensionnement_complet(
    donnees_aluminium: DonneesPoutre,
) -> None:
    """Le coordinateur doit regrouper et comparer les deux sections."""

    resultat = dimensionner_poutre(donnees_aluminium)

    assert resultat.section_initiale.hauteur_mm == pytest.approx(100.0)
    assert resultat.section_initiale.masse_kg == pytest.approx(13.9)
    assert resultat.section_initiale.est_admissible is True

    assert resultat.solution_trouvee is True
    assert resultat.optimisation is not None
    assert resultat.optimisation.hauteur_mm == 65

    assert resultat.difference_masse_kg == pytest.approx(4.865)
    assert resultat.difference_masse_pourcentage == pytest.approx(35.0)
    assert resultat.critere_dimensionnant is CritereDimensionnant.RIGIDITE


def test_dimensionnement_sans_solution(
    donnees_aluminium: DonneesPoutre,
) -> None:
    """Le résultat global doit accepter une optimisation sans solution."""

    resultat = dimensionner_poutre(
        donnees_aluminium,
        hauteur_min_mm=10,
        hauteur_max_mm=64,
        pas_mm=1,
    )

    assert resultat.solution_trouvee is False
    assert resultat.optimisation is None
    assert resultat.difference_masse_kg is None
    assert resultat.difference_masse_pourcentage is None
    assert resultat.critere_dimensionnant is None


def test_optimisation_acier() -> None:
    """Le matériau acier doit produire une hauteur minimale de 46 mm."""

    donnees = DonneesPoutre(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_initiale_m=0.10,
        force_n=1000.0,
        facteur_securite_minimal=2.0,
        materiau=ACIER_CONSTRUCTION,
    )

    resultat = rechercher_hauteur_minimale(donnees)

    assert resultat is not None
    assert resultat.hauteur_mm == 46
    assert resultat.masse_kg == pytest.approx(18.055)
    assert resultat.critere_dimensionnant is CritereDimensionnant.RIGIDITE
