"""Propriétés et catalogue des matériaux."""

from dataclasses import dataclass
import math
from typing import Final


@dataclass(frozen=True, slots=True)
class Materiau:
    """Représente les propriétés mécaniques utiles d'un matériau.

    Toutes les propriétés sont stockées dans le système international.

    Attributes:
        nom: Désignation du matériau.
        module_young_pa: Module de Young en pascals.
        limite_elastique_pa: Limite élastique en pascals.
        masse_volumique_kg_m3: Masse volumique en kilogrammes par mètre cube.
    """

    nom: str
    module_young_pa: float
    limite_elastique_pa: float
    masse_volumique_kg_m3: float

    def __post_init__(self) -> None:
        """Valide automatiquement les propriétés après création."""
        if not self.nom.strip():
            raise ValueError("Le nom du matériau ne peut pas être vide.")

        proprietes = {
            "module_young_pa": self.module_young_pa,
            "limite_elastique_pa": self.limite_elastique_pa,
            "masse_volumique_kg_m3": self.masse_volumique_kg_m3,
        }

        for nom, valeur in proprietes.items():
            if not math.isfinite(valeur) or valeur <= 0:
                raise ValueError(
                    f"{nom} doit être un nombre fini strictement positif."
                )


ALUMINIUM_2024_T3: Final[Materiau] = Materiau(
    nom="Aluminium 2024-T3",
    module_young_pa=73.1e9,
    limite_elastique_pa=320e6,
    masse_volumique_kg_m3=2780.0,
)

ACIER_CONSTRUCTION: Final[Materiau] = Materiau(
    nom="Acier de construction",
    module_young_pa=210e9,
    limite_elastique_pa=235e6,
    masse_volumique_kg_m3=7850.0,
)

MATERIAUX_DISPONIBLES: Final[tuple[Materiau, ...]] = (
    ALUMINIUM_2024_T3,
    ACIER_CONSTRUCTION,
)

_MATERIAUX_PAR_NOM: Final[dict[str, Materiau]] = {
    materiau.nom: materiau
    for materiau in MATERIAUX_DISPONIBLES
}


def obtenir_materiau(nom: str) -> Materiau:
    """Retourne un matériau enregistré à partir de son nom.

    Args:
        nom: Nom exact du matériau recherché.

    Returns:
        Matériau correspondant.

    Raises:
        ValueError: Si le matériau demandé n'existe pas.
    """
    try:
        return _MATERIAUX_PAR_NOM[nom]
    except KeyError as erreur:
        noms_disponibles = ", ".join(_MATERIAUX_PAR_NOM)
        raise ValueError(
            f"Matériau inconnu : {nom}. "
            f"Valeurs disponibles : {noms_disponibles}."
        ) from erreur