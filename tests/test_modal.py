"""Tests des fréquences propres analytiques."""

import pytest

from poutre.modal import calculer_frequences_flexion_rectangle


def test_frequences_modales_du_cas_reference() -> None:
    """Les fréquences analytiques de la poutre doivent être retrouvées."""
    resultat = calculer_frequences_flexion_rectangle(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_m=0.10,
        module_young_pa=73.1e9,
        masse_volumique_kg_m3=2780.0,
        nombre_modes=3,
    )

    assert resultat.axe_faible_hz == pytest.approx(
        (
            41.4177550999,
            259.560640579,
            726.777309479,
        ),
        rel=1e-9,
    )

    assert resultat.axe_fort_hz == pytest.approx(
        (
            82.8355101998,
            519.121281157,
            1453.55461896,
        ),
        rel=1e-9,
    )


def test_axe_faible_plus_souple_que_axe_fort() -> None:
    """Le premier mode faible doit avoir une fréquence plus basse."""
    resultat = calculer_frequences_flexion_rectangle(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_m=0.10,
        module_young_pa=73.1e9,
        masse_volumique_kg_m3=2780.0,
        nombre_modes=1,
    )

    assert resultat.axe_faible_hz[0] < resultat.axe_fort_hz[0]


@pytest.mark.parametrize("nombre_modes", [0, 5])
def test_nombre_modes_invalide(nombre_modes: int) -> None:
    """Le nombre de modes doit rester dans la plage disponible."""
    with pytest.raises(ValueError):
        calculer_frequences_flexion_rectangle(
            longueur_m=1.0,
            largeur_m=0.05,
            hauteur_m=0.10,
            module_young_pa=73.1e9,
            masse_volumique_kg_m3=2780.0,
            nombre_modes=nombre_modes,
        )
