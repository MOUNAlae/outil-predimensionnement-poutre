"""Export des résultats de dimensionnement vers des fichiers externes."""

import csv
from pathlib import Path

from .modeles import ResultatDimensionnement

CHAMPS_CSV = [
    "section",
    "hauteur_mm",
    "masse_kg",
    "contrainte_mpa",
    "fleche_mm",
    "fleche_admissible_mm",
    "facteur_securite",
    "facteur_securite_minimal",
    "admissible",
    "critere_dimensionnant",
    "difference_masse_kg",
    "reduction_masse_pourcentage",
]


def _formater_nombre(valeur: float) -> str:
    """Formate un nombre avec une précision adaptée à l'export."""

    return f"{valeur:.8g}"


def exporter_dimensionnement_csv(
    resultat: ResultatDimensionnement,
    destination: str | Path,
) -> Path:
    """Exporte les sections initiale et optimisée dans un fichier CSV.

    Le séparateur point-virgule facilite l'ouverture du fichier dans
    les versions françaises d'Excel. L'encodage UTF-8 avec signature
    préserve correctement les caractères accentués.

    Args:
        resultat: Résultat complet produit par ``dimensionner_poutre``.
        destination: Chemin du fichier CSV à créer.

    Returns:
        Chemin du fichier réellement créé.

    Raises:
        TypeError: Si ``resultat`` n'est pas un ResultatDimensionnement.
        ValueError: Si la destination est vide.
    """

    if not isinstance(resultat, ResultatDimensionnement):
        raise TypeError("resultat doit être une instance de ResultatDimensionnement.")

    if not str(destination).strip():
        raise ValueError("La destination de l'export ne peut pas être vide.")

    chemin = Path(destination)

    if chemin.suffix.lower() != ".csv":
        chemin = chemin.with_suffix(".csv")

    chemin.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    initiale = resultat.section_initiale

    lignes = [
        {
            "section": "initiale",
            "hauteur_mm": _formater_nombre(initiale.hauteur_mm),
            "masse_kg": _formater_nombre(initiale.masse_kg),
            "contrainte_mpa": _formater_nombre(initiale.contrainte_maximale_mpa),
            "fleche_mm": _formater_nombre(initiale.fleche_maximale_mm),
            "fleche_admissible_mm": _formater_nombre(initiale.fleche_admissible_mm),
            "facteur_securite": _formater_nombre(initiale.facteur_securite),
            "facteur_securite_minimal": _formater_nombre(
                initiale.facteur_securite_minimal
            ),
            "admissible": "oui" if initiale.est_admissible else "non",
            "critere_dimensionnant": "",
            "difference_masse_kg": "",
            "reduction_masse_pourcentage": "",
        }
    ]

    if resultat.optimisation is not None:
        optimisee = resultat.optimisation

        lignes.append(
            {
                "section": "optimisee",
                "hauteur_mm": str(optimisee.hauteur_mm),
                "masse_kg": _formater_nombre(optimisee.masse_kg),
                "contrainte_mpa": _formater_nombre(optimisee.contrainte_maximale_mpa),
                "fleche_mm": _formater_nombre(optimisee.fleche_maximale_mm),
                "fleche_admissible_mm": _formater_nombre(
                    optimisee.fleche_admissible_m * 1000.0
                ),
                "facteur_securite": _formater_nombre(optimisee.facteur_securite),
                "facteur_securite_minimal": _formater_nombre(
                    initiale.facteur_securite_minimal
                ),
                "admissible": "oui",
                "critere_dimensionnant": (optimisee.critere_dimensionnant.value),
                "difference_masse_kg": _formater_nombre(resultat.difference_masse_kg),
                "reduction_masse_pourcentage": _formater_nombre(
                    resultat.difference_masse_pourcentage
                ),
            }
        )

    with chemin.open(
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as fichier:
        redacteur = csv.DictWriter(
            fichier,
            fieldnames=CHAMPS_CSV,
            delimiter=";",
        )
        redacteur.writeheader()
        redacteur.writerows(lignes)

    return chemin
