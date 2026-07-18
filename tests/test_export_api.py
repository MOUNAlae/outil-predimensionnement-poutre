"""Vérifications de l'API publique et de l'export CSV."""

import csv
from pathlib import Path

import pytest

import poutre
from poutre import (
    ALUMINIUM_2024_T3,
    DonneesPoutre,
    dimensionner_poutre,
    exporter_dimensionnement_csv,
)
from poutre.modeles import ResultatDimensionnement


@pytest.fixture
def resultat_reference() -> ResultatDimensionnement:
    """Construit le dimensionnement complet du cas de référence."""

    donnees = DonneesPoutre(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_initiale_m=0.10,
        force_n=1000.0,
        facteur_securite_minimal=2.0,
        materiau=ALUMINIUM_2024_T3,
    )

    return dimensionner_poutre(donnees)


def lire_csv(chemin: Path) -> list[dict[str, str]]:
    """Lit un export avec le format réellement utilisé par le projet."""

    with chemin.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as fichier:
        return list(
            csv.DictReader(
                fichier,
                delimiter=";",
            )
        )


def test_api_publique() -> None:
    """Les principaux services doivent être accessibles depuis poutre."""

    assert poutre.__version__ == "0.1.0"
    assert "dimensionner_poutre" in poutre.__all__
    assert "exporter_dimensionnement_csv" in poutre.__all__
    assert callable(poutre.dimensionner_poutre)
    assert callable(poutre.exporter_dimensionnement_csv)


def test_export_csv_reference(
    resultat_reference: ResultatDimensionnement,
    tmp_path: Path,
) -> None:
    """Le cas de référence doit produire deux lignes cohérentes."""

    chemin = exporter_dimensionnement_csv(
        resultat_reference,
        tmp_path / "cas_reference.csv",
    )

    lignes = lire_csv(chemin)

    assert chemin.exists()
    assert len(lignes) == 2

    assert lignes[0]["section"] == "initiale"
    assert lignes[0]["hauteur_mm"] == "100"
    assert lignes[0]["masse_kg"] == "13.9"

    assert lignes[1]["section"] == "optimisee"
    assert lignes[1]["hauteur_mm"] == "65"
    assert lignes[1]["masse_kg"] == "9.035"
    assert lignes[1]["critere_dimensionnant"] == "rigidité"
    assert lignes[1]["reduction_masse_pourcentage"] == "35"


def test_extension_csv_ajoutee_automatiquement(
    resultat_reference: ResultatDimensionnement,
    tmp_path: Path,
) -> None:
    """L’extension CSV doit être ajoutée si elle est absente."""

    chemin = exporter_dimensionnement_csv(
        resultat_reference,
        tmp_path / "resultat",
    )

    assert chemin.suffix == ".csv"
    assert chemin.exists()


def test_export_sans_solution(
    tmp_path: Path,
) -> None:
    """Un dimensionnement sans optimisation doit rester exportable."""

    donnees = DonneesPoutre(
        longueur_m=1.0,
        largeur_m=0.05,
        hauteur_initiale_m=0.10,
        force_n=1000.0,
        facteur_securite_minimal=2.0,
        materiau=ALUMINIUM_2024_T3,
    )

    resultat = dimensionner_poutre(
        donnees,
        hauteur_min_mm=10,
        hauteur_max_mm=64,
        pas_mm=1,
    )

    chemin = exporter_dimensionnement_csv(
        resultat,
        tmp_path / "sans_solution.csv",
    )

    lignes = lire_csv(chemin)

    assert len(lignes) == 1
    assert lignes[0]["section"] == "initiale"


def test_export_refuse_un_resultat_invalide(
    tmp_path: Path,
) -> None:
    """L’export doit refuser un objet qui n’est pas un résultat."""

    with pytest.raises(TypeError):
        exporter_dimensionnement_csv(
            "resultat invalide",
            tmp_path / "invalide.csv",
        )


def test_export_refuse_destination_vide(
    resultat_reference: ResultatDimensionnement,
) -> None:
    """Une destination vide doit produire une erreur explicite."""

    with pytest.raises(ValueError):
        exporter_dimensionnement_csv(
            resultat_reference,
            "",
        )
