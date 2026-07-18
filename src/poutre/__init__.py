"""API publique de l'outil de pré-dimensionnement de poutres."""

from .dimensionnement import dimensionner_poutre, evaluer_section
from .export import exporter_dimensionnement_csv
from .materiaux import (
    ACIER_CONSTRUCTION,
    ALUMINIUM_2024_T3,
    MATERIAUX_DISPONIBLES,
    Materiau,
    obtenir_materiau,
)
from .modeles import (
    CritereDimensionnant,
    DonneesPoutre,
    ResultatDimensionnement,
    ResultatOptimisation,
    ResultatSection,
)
from .optimisation import rechercher_hauteur_minimale

__version__ = "0.1.0"

__all__ = [
    "ACIER_CONSTRUCTION",
    "ALUMINIUM_2024_T3",
    "CritereDimensionnant",
    "DonneesPoutre",
    "MATERIAUX_DISPONIBLES",
    "Materiau",
    "ResultatDimensionnement",
    "ResultatOptimisation",
    "ResultatSection",
    "dimensionner_poutre",
    "evaluer_section",
    "exporter_dimensionnement_csv",
    "obtenir_materiau",
    "rechercher_hauteur_minimale",
]
