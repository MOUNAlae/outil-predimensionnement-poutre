"""Modèles de données d'entrée et de résultat."""

from dataclasses import dataclass
import math

from .materiaux import Materiau


def _verifier_valeur_positive(nom: str, valeur: float) -> None:
    """Vérifie qu'une donnée est finie et strictement positive."""
    if not math.isfinite(valeur) or valeur <= 0:
        raise ValueError(
            f"{nom} doit être un nombre fini strictement positif."
        )


@dataclass(frozen=True, slots=True)
class DonneesPoutre:
    """Regroupe les données nécessaires au dimensionnement d'une poutre.

    Toutes les grandeurs physiques utilisent le système international.

    Attributes:
        longueur_m: Longueur de la poutre en mètres.
        largeur_m: Largeur de la section en mètres.
        hauteur_initiale_m: Hauteur initiale de la section en mètres.
        force_n: Valeur positive de la force appliquée en newtons.
        facteur_securite_minimal: Facteur de sécurité minimal demandé.
        materiau: Matériau utilisé pour la poutre.
        rapport_fleche: Diviseur du critère de flèche, 250 par défaut.
    """

    longueur_m: float
    largeur_m: float
    hauteur_initiale_m: float
    force_n: float
    facteur_securite_minimal: float
    materiau: Materiau
    rapport_fleche: float = 250.0

    def __post_init__(self) -> None:
        """Valide automatiquement toutes les données d'entrée."""
        valeurs = {
            "longueur_m": self.longueur_m,
            "largeur_m": self.largeur_m,
            "hauteur_initiale_m": self.hauteur_initiale_m,
            "force_n": self.force_n,
            "facteur_securite_minimal": self.facteur_securite_minimal,
            "rapport_fleche": self.rapport_fleche,
        }

        for nom, valeur in valeurs.items():
            _verifier_valeur_positive(nom, valeur)

        if not isinstance(self.materiau, Materiau):
            raise TypeError(
                "materiau doit être une instance de Materiau."
            )