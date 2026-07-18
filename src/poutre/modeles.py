"""Modèles de données utilisés pour le dimensionnement de la poutre."""

import math
from dataclasses import dataclass
from enum import Enum

from .materiaux import Materiau


def _verifier_valeur_positive(
    nom: str,
    valeur: int | float,
) -> None:
    """Vérifie qu'une valeur est numérique, finie et positive."""

    if isinstance(valeur, bool) or not isinstance(valeur, (int, float)):
        raise TypeError(f"{nom} doit être une valeur numérique.")

    if not math.isfinite(valeur) or valeur <= 0:
        raise ValueError(
            f"{nom} doit être un nombre fini strictement positif."
        )


@dataclass(frozen=True, slots=True)
class DonneesPoutre:
    """Données nécessaires au dimensionnement d'une poutre encastrée."""

    longueur_m: float
    largeur_m: float
    hauteur_initiale_m: float
    force_n: float
    facteur_securite_minimal: float
    materiau: Materiau
    rapport_fleche: float = 250.0

    def __post_init__(self) -> None:
        """Valide automatiquement les données après leur création."""

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


class CritereDimensionnant(str, Enum):
    """Critère mécanique le plus proche de sa limite admissible."""

    RESISTANCE = "résistance"
    RIGIDITE = "rigidité"
    MIXTE = "résistance et rigidité"


@dataclass(frozen=True, slots=True)
class ResultatSection:
    """Résultats mécaniques obtenus pour une section donnée."""

    hauteur_m: float
    moment_quadratique_m4: float
    moment_maximal_nm: float
    volume_m3: float
    masse_kg: float
    contrainte_maximale_pa: float
    fleche_maximale_m: float
    fleche_admissible_m: float
    facteur_securite: float
    facteur_securite_minimal: float

    def __post_init__(self) -> None:
        """Valide les valeurs calculées de la section."""

        valeurs = {
            "hauteur_m": self.hauteur_m,
            "moment_quadratique_m4": self.moment_quadratique_m4,
            "moment_maximal_nm": self.moment_maximal_nm,
            "volume_m3": self.volume_m3,
            "masse_kg": self.masse_kg,
            "contrainte_maximale_pa": self.contrainte_maximale_pa,
            "fleche_maximale_m": self.fleche_maximale_m,
            "fleche_admissible_m": self.fleche_admissible_m,
            "facteur_securite": self.facteur_securite,
            "facteur_securite_minimal": self.facteur_securite_minimal,
        }

        for nom, valeur in valeurs.items():
            _verifier_valeur_positive(nom, valeur)

    @property
    def hauteur_mm(self) -> float:
        """Retourne la hauteur en millimètres."""
        return self.hauteur_m * 1000.0

    @property
    def contrainte_maximale_mpa(self) -> float:
        """Retourne la contrainte maximale en mégapascals."""
        return self.contrainte_maximale_pa / 1e6

    @property
    def fleche_maximale_mm(self) -> float:
        """Retourne la flèche maximale en millimètres."""
        return self.fleche_maximale_m * 1000.0

    @property
    def fleche_admissible_mm(self) -> float:
        """Retourne la flèche admissible en millimètres."""
        return self.fleche_admissible_m * 1000.0

    @property
    def resistance_respectee(self) -> bool:
        """Indique si le facteur de sécurité minimal est respecté."""
        return self.facteur_securite >= self.facteur_securite_minimal

    @property
    def rigidite_respectee(self) -> bool:
        """Indique si la flèche reste inférieure à la limite."""
        return self.fleche_maximale_m <= self.fleche_admissible_m

    @property
    def est_admissible(self) -> bool:
        """Indique si résistance et rigidité sont respectées."""
        return self.resistance_respectee and self.rigidite_respectee


@dataclass(frozen=True, slots=True)
class ResultatOptimisation:
    """Résultat de la recherche d'une hauteur minimale admissible."""

    hauteur_mm: int
    moment_quadratique_m4: float
    volume_m3: float
    masse_kg: float
    contrainte_maximale_pa: float
    fleche_maximale_m: float
    fleche_admissible_m: float
    facteur_securite: float
    taux_utilisation_resistance: float
    taux_utilisation_rigidite: float
    critere_dimensionnant: CritereDimensionnant

    @property
    def hauteur_m(self) -> float:
        """Retourne la hauteur optimisée en mètres."""
        return self.hauteur_mm / 1000.0

    @property
    def contrainte_maximale_mpa(self) -> float:
        """Retourne la contrainte maximale en mégapascals."""
        return self.contrainte_maximale_pa / 1e6

    @property
    def fleche_maximale_mm(self) -> float:
        """Retourne la flèche maximale en millimètres."""
        return self.fleche_maximale_m * 1000.0


@dataclass(frozen=True, slots=True)
class ResultatDimensionnement:
    """Regroupe la section initiale et son optimisation."""

    section_initiale: ResultatSection
    optimisation: ResultatOptimisation | None

    def __post_init__(self) -> None:
        """Vérifie les types des résultats regroupés."""

        if not isinstance(self.section_initiale, ResultatSection):
            raise TypeError(
                "section_initiale doit être un ResultatSection."
            )

        if (
            self.optimisation is not None
            and not isinstance(self.optimisation, ResultatOptimisation)
        ):
            raise TypeError(
                "optimisation doit être un ResultatOptimisation ou None."
            )

    @property
    def solution_trouvee(self) -> bool:
        """Indique si l'optimisation a trouvé une section admissible."""
        return self.optimisation is not None

    @property
    def difference_masse_kg(self) -> float | None:
        """Retourne la différence entre les deux masses."""

        if self.optimisation is None:
            return None

        return self.section_initiale.masse_kg - self.optimisation.masse_kg

    @property
    def difference_masse_pourcentage(self) -> float | None:
        """Retourne la réduction de masse en pourcentage."""

        difference = self.difference_masse_kg

        if difference is None:
            return None

        return difference / self.section_initiale.masse_kg * 100.0

    @property
    def critere_dimensionnant(
        self,
    ) -> CritereDimensionnant | None:
        """Retourne le critère dimensionnant de la solution optimisée."""

        if self.optimisation is None:
            return None

        return self.optimisation.critere_dimensionnant