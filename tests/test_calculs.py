"""Vérifications automatiques des calculs mécaniques élémentaires."""

import pytest

from poutre.calculs import (
    calculer_contrainte_maximale,
    calculer_facteur_securite,
    calculer_fleche_admissible,
    calculer_fleche_maximale,
    calculer_masse,
    calculer_moment_maximal,
    calculer_moment_quadratique,
    calculer_volume,
)

MOMENT_QUADRATIQUE_REFERENCE_M4 = 4.166666666666668e-6


def test_calculer_moment_quadratique() -> None:
    """Le moment quadratique du cas de référence doit être retrouvé."""

    resultat = calculer_moment_quadratique(
        largeur_m=0.05,
        hauteur_m=0.10,
    )

    assert resultat == pytest.approx(
        MOMENT_QUADRATIQUE_REFERENCE_M4,
        rel=1e-12,
    )


def test_calculer_moment_maximal() -> None:
    """Le moment à l'encastrement doit être égal à F multiplié par L."""

    resultat = calculer_moment_maximal(
        force_n=1000.0,
        longueur_m=1.0,
    )

    assert resultat == pytest.approx(1000.0)


def test_calculer_contrainte_maximale() -> None:
    """La contrainte du cas de référence doit être de 12 MPa."""

    resultat = calculer_contrainte_maximale(
        moment_maximal_nm=1000.0,
        hauteur_m=0.10,
        moment_quadratique_m4=MOMENT_QUADRATIQUE_REFERENCE_M4,
    )

    assert resultat == pytest.approx(12.0e6, rel=1e-12)


def test_calculer_fleche_maximale() -> None:
    """La flèche du cas de référence doit être proche de 1,094 mm."""

    resultat = calculer_fleche_maximale(
        force_n=1000.0,
        longueur_m=1.0,
        module_young_pa=73.1e9,
        moment_quadratique_m4=MOMENT_QUADRATIQUE_REFERENCE_M4,
    )

    assert resultat == pytest.approx(
        1.094391244870041e-3,
        rel=1e-9,
    )


def test_calculer_volume_et_masse() -> None:
    """Le volume et la masse initiaux doivent être retrouvés."""

    volume_m3 = calculer_volume(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_m=0.10,
    )

    masse_kg = calculer_masse(
        masse_volumique_kg_m3=2780.0,
        volume_m3=volume_m3,
    )

    assert volume_m3 == pytest.approx(0.005)
    assert masse_kg == pytest.approx(13.9)


def test_calculer_facteur_securite() -> None:
    """Le facteur de sécurité doit être égal à Re divisé par sigma."""

    resultat = calculer_facteur_securite(
        limite_elastique_pa=320.0e6,
        contrainte_maximale_pa=12.0e6,
    )

    assert resultat == pytest.approx(26.666666666666668)


def test_calculer_fleche_admissible() -> None:
    """La limite L/250 doit donner 4 mm pour une poutre de 1 m."""

    resultat_standard = calculer_fleche_admissible(
        longueur_m=1.0,
    )

    resultat_personnalise = calculer_fleche_admissible(
        longueur_m=1.0,
        rapport_fleche=500.0,
    )

    assert resultat_standard == pytest.approx(0.004)
    assert resultat_personnalise == pytest.approx(0.002)


@pytest.mark.parametrize(
    ("fonction", "arguments"),
    [
        (calculer_moment_quadratique, (0.0, 0.10)),
        (calculer_moment_maximal, (0.0, 1.0)),
        (
            calculer_contrainte_maximale,
            (0.0, 0.10, MOMENT_QUADRATIQUE_REFERENCE_M4),
        ),
        (
            calculer_fleche_maximale,
            (0.0, 1.0, 73.1e9, MOMENT_QUADRATIQUE_REFERENCE_M4),
        ),
        (calculer_volume, (0.0, 0.05, 0.10)),
        (calculer_masse, (0.0, 0.005)),
        (calculer_facteur_securite, (0.0, 12.0e6)),
        (calculer_fleche_admissible, (0.0, 250.0)),
    ],
)
def test_valeurs_nulles_rejetees(
    fonction,
    arguments: tuple[float, ...],
) -> None:
    """Les dimensions et propriétés nulles doivent être refusées."""

    with pytest.raises(ValueError):
        fonction(*arguments)
