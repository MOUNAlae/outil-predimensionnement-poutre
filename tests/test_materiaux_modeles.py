"""Vérifications automatiques des matériaux et modèles de données."""

import math

import pytest

from poutre.materiaux import (
    ACIER_CONSTRUCTION,
    ALUMINIUM_2024_T3,
    Materiau,
    obtenir_materiau,
)
from poutre.modeles import DonneesPoutre, ResultatSection


def test_proprietes_materiaux_reference() -> None:
    """Les propriétés des deux matériaux doivent rester stables."""

    assert ALUMINIUM_2024_T3.module_young_pa == pytest.approx(73.1e9)
    assert ALUMINIUM_2024_T3.limite_elastique_pa == pytest.approx(320.0e6)
    assert ALUMINIUM_2024_T3.masse_volumique_kg_m3 == pytest.approx(2780.0)

    assert ACIER_CONSTRUCTION.module_young_pa == pytest.approx(210.0e9)
    assert ACIER_CONSTRUCTION.limite_elastique_pa == pytest.approx(235.0e6)
    assert ACIER_CONSTRUCTION.masse_volumique_kg_m3 == pytest.approx(7850.0)


@pytest.mark.parametrize(
    ("nom", "materiau_attendu"),
    [
        ("Aluminium 2024-T3", ALUMINIUM_2024_T3),
        ("Acier de construction", ACIER_CONSTRUCTION),
    ],
)
def test_obtenir_materiau(
    nom: str,
    materiau_attendu: Materiau,
) -> None:
    """La recherche par nom doit retourner l'objet de référence."""

    assert obtenir_materiau(nom) is materiau_attendu


def test_obtenir_materiau_inconnu() -> None:
    """Un nom inconnu doit produire une erreur explicite."""

    with pytest.raises(ValueError):
        obtenir_materiau("Titane inconnu")


@pytest.mark.parametrize(
    "arguments",
    [
        {
            "nom": "",
            "module_young_pa": 73.1e9,
            "limite_elastique_pa": 320.0e6,
            "masse_volumique_kg_m3": 2780.0,
        },
        {
            "nom": "Matériau",
            "module_young_pa": 0.0,
            "limite_elastique_pa": 320.0e6,
            "masse_volumique_kg_m3": 2780.0,
        },
        {
            "nom": "Matériau",
            "module_young_pa": 73.1e9,
            "limite_elastique_pa": 0.0,
            "masse_volumique_kg_m3": 2780.0,
        },
        {
            "nom": "Matériau",
            "module_young_pa": 73.1e9,
            "limite_elastique_pa": 320.0e6,
            "masse_volumique_kg_m3": math.nan,
        },
    ],
)
def test_materiau_invalide_rejete(
    arguments: dict[str, str | float],
) -> None:
    """Les propriétés invalides d'un matériau doivent être refusées."""

    with pytest.raises(ValueError):
        Materiau(**arguments)


def test_donnees_poutre_valides() -> None:
    """Le cas de référence doit créer un objet valide."""

    donnees = DonneesPoutre(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_initiale_m=0.10,
        force_n=1000.0,
        facteur_securite_minimal=2.0,
        materiau=ALUMINIUM_2024_T3,
    )

    assert donnees.longueur_m == pytest.approx(1.0)
    assert donnees.rapport_fleche == pytest.approx(250.0)
    assert donnees.materiau is ALUMINIUM_2024_T3


@pytest.mark.parametrize(
    ("champ", "valeur"),
    [
        ("longueur_m", 0.0),
        ("largeur_m", -0.05),
        ("hauteur_initiale_m", math.inf),
        ("force_n", 0.0),
        ("facteur_securite_minimal", 0.0),
        ("rapport_fleche", 0.0),
    ],
)
def test_donnees_poutre_invalides(
    champ: str,
    valeur: float,
) -> None:
    """Chaque donnée mécanique doit être finie et positive."""

    arguments = {
        "longueur_m": 1.0,
        "largeur_m": 0.05,
        "hauteur_initiale_m": 0.10,
        "force_n": 1000.0,
        "facteur_securite_minimal": 2.0,
        "materiau": ALUMINIUM_2024_T3,
        "rapport_fleche": 250.0,
    }

    arguments[champ] = valeur

    with pytest.raises(ValueError):
        DonneesPoutre(**arguments)


def test_type_materiau_invalide() -> None:
    """Une chaîne de caractères ne doit pas remplacer un objet Materiau."""

    with pytest.raises(TypeError):
        DonneesPoutre(
            longueur_m=1.0,
            largeur_m=0.05,
            hauteur_initiale_m=0.10,
            force_n=1000.0,
            facteur_securite_minimal=2.0,
            materiau="Aluminium 2024-T3",
        )


def test_resultat_section_admissible() -> None:
    """Le résultat initial de référence doit être admissible."""

    resultat = ResultatSection(
        hauteur_m=0.10,
        moment_quadratique_m4=4.166666666666668e-6,
        moment_maximal_nm=1000.0,
        volume_m3=0.005,
        masse_kg=13.9,
        contrainte_maximale_pa=12.0e6,
        fleche_maximale_m=1.094391244870041e-3,
        fleche_admissible_m=0.004,
        facteur_securite=26.666666666666668,
        facteur_securite_minimal=2.0,
    )

    assert resultat.hauteur_mm == pytest.approx(100.0)
    assert resultat.contrainte_maximale_mpa == pytest.approx(12.0)
    assert resultat.fleche_maximale_mm == pytest.approx(1.094391244870041)
    assert resultat.fleche_admissible_mm == pytest.approx(4.0)
    assert resultat.resistance_respectee is True
    assert resultat.rigidite_respectee is True
    assert resultat.est_admissible is True


def test_resultat_section_non_admissible() -> None:
    """Un dépassement de résistance et de flèche doit être détecté."""

    resultat = ResultatSection(
        hauteur_m=0.03,
        moment_quadratique_m4=1.0e-7,
        moment_maximal_nm=1000.0,
        volume_m3=0.0015,
        masse_kg=4.17,
        contrainte_maximale_pa=200.0e6,
        fleche_maximale_m=0.005,
        fleche_admissible_m=0.004,
        facteur_securite=1.6,
        facteur_securite_minimal=2.0,
    )

    assert resultat.resistance_respectee is False
    assert resultat.rigidite_respectee is False
    assert resultat.est_admissible is False
