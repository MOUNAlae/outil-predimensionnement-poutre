# Outil de pré-dimensionnement d'une poutre encastrée
# Auteur : Mohamed Alae Mountassir
import csv
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
import numpy as np


def calculer_moment_quadratique(b, h):
    moment_quadratique = b * h**3 / 12
    return moment_quadratique


def calculer_moment_maximal(F, L):
    M_max = F * L
    return M_max


def calculer_contrainte_maximale(M_max, h, moment_quadratique):
    sigma_max = (M_max * h / 2) / moment_quadratique
    return sigma_max


def calculer_fleche_maximale(F, L, E, moment_quadratique):
    fleche_max = (F * L**3) / (3 * E * moment_quadratique)
    return fleche_max


def calculer_volume(L, b, h):
    volume = L * b * h
    return volume


def calculer_masse(densite, volume):
    masse = densite * volume
    return masse


def calculer_facteur_securite(Re, sigma_max):
    facteur_securite = Re / sigma_max
    return facteur_securite


def calculer_fleche_admissible(L):
    fleche_admissible = L / 250
    return fleche_admissible


def verifier_resistance(facteur_securite, facteur_securite_minimal):
    tolerance = 1e-9

    if facteur_securite + tolerance >= facteur_securite_minimal:
        return True
    else:
        return False


def verifier_rigidite(fleche_max, fleche_admissible):
    if fleche_max <= fleche_admissible:
        return True
    else:
        return False


def rechercher_hauteur_minimale(L, b, F, E, Re, densite, facteur_securite_minimal):
    fleche_admissible = calculer_fleche_admissible(L)

    hauteurs = np.arange(0.01, 0.201, 0.001)

    for hauteur_testee in hauteurs:
        I_test = calculer_moment_quadratique(b, hauteur_testee)

        M_max_test = calculer_moment_maximal(F, L)

        sigma_test = calculer_contrainte_maximale(M_max_test, hauteur_testee, I_test)

        fleche_test = calculer_fleche_maximale(F, L, E, I_test)

        facteur_securite_test = calculer_facteur_securite(Re, sigma_test)

        resistance_test = verifier_resistance(
            facteur_securite_test, facteur_securite_minimal
        )

        rigidite_test = verifier_rigidite(fleche_test, fleche_admissible)

        if resistance_test and rigidite_test:
            volume_test = calculer_volume(L, b, hauteur_testee)

            masse_test = calculer_masse(densite, volume_test)

            return (
                hauteur_testee,
                sigma_test,
                fleche_test,
                facteur_securite_test,
                masse_test,
            )

    return None


def selectionner_materiau(choix_materiau):
    E_aluminium = 73.1e9
    Re_aluminium = 320e6
    densite_aluminium = 2780

    E_acier = 210e9
    Re_acier = 235e6
    densite_acier = 7850

    if choix_materiau == 1:
        nom_materiau = "Aluminium 2024-T3"
        E = E_aluminium
        Re = Re_aluminium
        densite = densite_aluminium

    elif choix_materiau == 2:
        nom_materiau = "Acier de construction"
        E = E_acier
        Re = Re_acier
        densite = densite_acier

    else:
        nom_materiau = "Choix invalide"
        E = 0
        Re = 0
        densite = 0

    return nom_materiau, E, Re, densite


def creer_positions(L):
    x = np.linspace(0, L, 100)
    return x


def calculer_effort_tranchant(x, F):
    effort_tranchant = np.full_like(x, -F)
    return effort_tranchant


def calculer_deformee(x, F, L, E, moment_quadratique):
    deformee = -(F * x**2 * (3 * L - x)) / (6 * E * moment_quadratique)
    return deformee


def tracer_moment_flechissant(x, moment_flechissant):
    plt.figure()

    plt.plot(x, moment_flechissant)

    plt.title("Diagramme du moment fléchissant")
    plt.xlabel("Position x le long de la poutre (m)")
    plt.ylabel("Moment fléchissant M(x) (N.m)")

    plt.grid()
    plt.show()


def tracer_effort_tranchant(x, effort_tranchant):
    plt.figure()

    plt.plot(x, effort_tranchant)

    plt.title("Diagramme de l'effort tranchant")
    plt.xlabel("Position x le long de la poutre (m)")
    plt.ylabel("Effort tranchant T(x) (N)")

    plt.grid()
    plt.show()


def tracer_deformee(x, deformee):
    deformee_mm = deformee * 1000

    plt.figure()

    plt.plot(x, deformee_mm)

    plt.title("Déformée de la poutre")
    plt.xlabel("Position x le long de la poutre (m)")
    plt.ylabel("Déplacement vertical v(x) (mm)")

    plt.grid()
    plt.show()


def tracer_resultats_combines(
    x, effort_tranchant, moment_flechissant, deformee, nom_materiau
):
    deformee_mm = deformee * 1000

    figure, axes = plt.subplots(3, 1, figsize=(10, 12), constrained_layout=True)

    figure.suptitle(f"Pré-dimensionnement d'une poutre — {nom_materiau}", fontsize=16)

    axes[0].plot(x, effort_tranchant)
    axes[0].set_title("Diagramme de l'effort tranchant")
    # axes[0].set_xlabel("Position x (m)")
    axes[0].set_ylabel("T(x) (N)")
    axes[0].grid()

    axes[1].plot(x, moment_flechissant)
    axes[1].set_title("Diagramme du moment fléchissant")
    # axes[1].set_xlabel("Position x (m)")
    axes[1].set_ylabel("M(x) (N.m)")
    axes[1].grid()

    axes[2].plot(x, deformee_mm)
    axes[2].set_title("Déformée de la poutre")
    axes[2].set_xlabel("Position x (m)")
    axes[2].set_ylabel("v(x) (mm)")
    axes[2].grid()
    if nom_materiau == "Aluminium 2024-T3":
        nom_fichier = "resultats_poutre_aluminium.png"
    else:
        nom_fichier = "resultats_poutre_acier.png"
    figure.savefig(nom_fichier, dpi=300)
    print(f"\nFigure enregistrée dans : {nom_fichier}")
    plt.show()


def exporter_resultats_csv(
    L,
    b,
    h,
    F,
    nom_materiau,
    E,
    Re,
    densite,
    volume,
    masse,
    moment_quadratique,
    M_max,
    sigma_max_MPa,
    fleche_max_mm,
    fleche_admissible_mm,
    facteur_securite,
    facteur_securite_minimal,
    resistance_respectee,
    rigidite_respectee,
    hauteur_optimisee,
    sigma_optimisee,
    fleche_optimisee,
    facteur_securite_optimise,
    masse_optimisee,
    reduction_masse,
    pourcentage_reduction,
):
    if resistance_respectee and rigidite_respectee:
        conclusion = "Dimensionnement validé"
    else:
        conclusion = "Dimensionnement non validé"
    if nom_materiau == "Aluminium 2024-T3":
        nom_fichier = "resultats_poutre_aluminium.csv"
    else:
        nom_fichier = "resultats_poutre_acier.csv"
    with open(nom_fichier, "w", newline="", encoding="utf-8-sig") as fichier:
        ecrivain = csv.writer(fichier, delimiter=";")

        ecrivain.writerow(["Paramètre", "Valeur", "Unité"])

        ecrivain.writerow(["Longueur", L, "m"])
        ecrivain.writerow(["Largeur", b, "m"])
        ecrivain.writerow(["Hauteur", h, "m"])
        ecrivain.writerow(["Force", F, "N"])

        ecrivain.writerow(["Matériau", nom_materiau, ""])
        ecrivain.writerow(["Module d'Young", E / 1e9, "GPa"])
        ecrivain.writerow(["Limite élastique", Re / 1e6, "MPa"])
        ecrivain.writerow(["Masse volumique", densite, "kg/m³"])

        ecrivain.writerow(["Volume", volume, "m³"])
        ecrivain.writerow(["Masse", masse, "kg"])
        ecrivain.writerow(["Moment quadratique", moment_quadratique, "m⁴"])
        ecrivain.writerow(["Moment maximal", M_max, "N·m"])
        ecrivain.writerow(["Contrainte maximale", sigma_max_MPa, "MPa"])
        ecrivain.writerow(["Flèche maximale", fleche_max_mm, "mm"])
        ecrivain.writerow(["Flèche admissible", fleche_admissible_mm, "mm"])
        ecrivain.writerow(["Facteur de sécurité", facteur_securite, ""])
        ecrivain.writerow(
            [
                "Facteur de sécurité minimal demandé",
                round(facteur_securite_minimal, 2),
                "",
            ]
        )

        ecrivain.writerow(
            ["Résistance respectée", "Oui" if resistance_respectee else "Non", ""]
        )

        ecrivain.writerow(
            ["Rigidité respectée", "Oui" if rigidite_respectee else "Non", ""]
        )

        ecrivain.writerow(["Conclusion", conclusion, ""])
        ecrivain.writerow([])
        ecrivain.writerow(["RÉSULTATS DE L'OPTIMISATION", "", ""])

        ecrivain.writerow(["Hauteur initiale", round(h * 1000, 1), "mm"])

        ecrivain.writerow(
            ["Hauteur optimisée", round(hauteur_optimisee * 1000, 1), "mm"]
        )

        ecrivain.writerow(["Masse initiale", round(masse, 2), "kg"])

        ecrivain.writerow(["Masse optimisée", round(masse_optimisee, 2), "kg"])

        ecrivain.writerow(
            ["Contrainte optimisée", round(sigma_optimisee / 1e6, 2), "MPa"]
        )

        ecrivain.writerow(["Flèche optimisée", round(fleche_optimisee * 1000, 3), "mm"])

        ecrivain.writerow(
            ["Facteur de sécurité optimisé", round(facteur_securite_optimise, 2), ""]
        )

        ecrivain.writerow(["Réduction de masse", round(reduction_masse, 2), "kg"])

        ecrivain.writerow(["Réduction relative", round(pourcentage_reduction, 1), "%"])
    print(f"Résultats enregistrés dans : {nom_fichier}")


def main():
    print("\n--- RÉSULTATS DU PRÉ-DIMENSIONNEMENT ---\n")
    print("Choisissez un matériau :")
    print("1 - Aluminium 2024-T3")
    print("2 - Acier de construction")
    try:
        L = float(input("Entrez la longueur de la poutre en m : "))
        b = float(input("Entrez la largeur de la poutre en m : "))
        h = float(input("Entrez la hauteur de la poutre en m : "))
        F = float(input("Entrez la force appliquée sur la poutre en N : "))
        facteur_securite_minimal = float(
            input("Entrez le facteur de sécurité minimal souhaité : ")
        )
        choix_materiau = int(input("Votre choix de matériau : "))
        E_aluminium = 73.1e9
        Re_aluminium = 320e6
        densite_aluminium = 2780

        E_acier = 210e9
        Re_acier = 235e6
        densite_acier = 7850
        nom_materiau, E, Re, densite = selectionner_materiau(choix_materiau)
        if choix_materiau != 1 and choix_materiau != 2:
            print("Erreur : choix de matériau invalide.")

        elif L <= 0 or b <= 0 or h <= 0 or F <= 0 or facteur_securite_minimal <= 0:
            print("Erreur : toutes les valeurs doivent être strictement positives.")

        else:
            print("\n--- MATÉRIAU SÉLECTIONNÉ ---")
            print(f"\nMatériau sélectionné : {nom_materiau}")
            print(f"Module d'Young : {E / 1e9:.1f} GPa")
            print(f"Limite élastique : {Re / 1e6:.1f} MPa")
            print(f"Masse volumique : {densite:.0f} kg/m^3")
            volume = calculer_volume(L, b, h)
            masse = calculer_masse(densite, volume)
            masse_aluminium = calculer_masse(densite_aluminium, volume)
            masse_acier = calculer_masse(densite_acier, volume)
            difference_masse = masse_acier - masse_aluminium
            rapport_masse = masse_acier / masse_aluminium
            print(f"Volume de la poutre : {volume:.6f} m^3")
            print(f"Masse de la poutre : {masse:.2f} kg")
            print("\n--- COMPARAISON DES MASSES ---")
            print(f"Masse en aluminium : {masse_aluminium:.2f} kg")
            print(f"Masse en acier : {masse_acier:.2f} kg")
            print(f"Différence de masse : {difference_masse:.2f} kg")
            print(f"Rapport acier/aluminium : {rapport_masse:.2f}")
            print("\n--- RÉSULTATS MÉCANIQUES ---")
            moment_quadratique = calculer_moment_quadratique(b, h)
            print(f"Moment quadratique : {moment_quadratique:.6e} m^4")
            M_max = calculer_moment_maximal(F, L)
            print(f"Moment maximal : {M_max:.2f} N.m")
            x = creer_positions(L)
            moment_flechissant = -F * (L - x)
            effort_tranchant = calculer_effort_tranchant(x, F)
            deformee = calculer_deformee(x, F, L, E, moment_quadratique)
            sigma_max = calculer_contrainte_maximale(M_max, h, moment_quadratique)
            sigma_max_MPa = sigma_max / 1e6
            fleche_aluminium = calculer_fleche_maximale(
                F, L, E_aluminium, moment_quadratique
            )
            fleche_acier = calculer_fleche_maximale(F, L, E_acier, moment_quadratique)

            fleche_aluminium_mm = fleche_aluminium * 1000
            fleche_acier_mm = fleche_acier * 1000
            facteur_securite_aluminium = calculer_facteur_securite(
                Re_aluminium, sigma_max
            )
            facteur_securite_acier = calculer_facteur_securite(Re_acier, sigma_max)

            print(f"Contrainte maximale : {sigma_max_MPa:.2f} MPa")
            fleche_max = calculer_fleche_maximale(F, L, E, moment_quadratique)
            fleche_max_mm = fleche_max * 1000
            fleche_admissible = calculer_fleche_admissible(L)
            fleche_admissible_mm = fleche_admissible * 1000
            print(f"Flèche maximale : {fleche_max_mm:.3f} mm")
            print(f"Flèche admissible : {fleche_admissible_mm:.3f} mm")
            facteur_securite = calculer_facteur_securite(Re, sigma_max)
            print(f"Facteur de sécurité : {facteur_securite:.2f}")
            print(
                f"Facteur de sécurité minimal demandé : {facteur_securite_minimal:.2f}"
            )
            print("\n--- COMPARAISON MÉCANIQUE DES MATÉRIAUX ---")
            print(f"Contrainte commune : {sigma_max_MPa:.2f} MPa")
            print(f"Flèche aluminium : {fleche_aluminium_mm:.3f} mm")
            print(f"Flèche acier : {fleche_acier_mm:.3f} mm")
            print(f"Facteur de sécurité aluminium : {facteur_securite_aluminium:.2f}")
            print(f"Facteur de sécurité acier : {facteur_securite_acier:.2f}")
            resistance_respectee = verifier_resistance(
                facteur_securite, facteur_securite_minimal
            )

            if resistance_respectee:
                print(
                    "Le critère de résistance statique est respecté : "
                    f"FS = {facteur_securite:.2f} >= "
                    f"{facteur_securite_minimal:.2f}."
                )
            else:
                print(
                    "Le critère de résistance statique n'est pas respecté : "
                    f"FS = {facteur_securite:.2f} < "
                    f"{facteur_securite_minimal:.2f}."
                )
            rigidite_respectee = verifier_rigidite(fleche_max, fleche_admissible)

            if rigidite_respectee:
                print("Le critère de rigidité est respecté.")
            else:
                print("Le critère de rigidité n'est pas respecté.")
            print("\n--- CONCLUSION GLOBALE ---")

            if resistance_respectee and rigidite_respectee:
                print(
                    "Dimensionnement validé : les critères de résistance et de rigidité sont respectés."
                )
            else:
                print(
                    "Dimensionnement non validé : au moins un critère n'est pas respecté."
                )

            solution_optimisee = rechercher_hauteur_minimale(
                L, b, F, E, Re, densite, facteur_securite_minimal
            )

            print("\n--- RECHERCHE D'UNE HAUTEUR MINIMALE ---")

            if solution_optimisee is not None:
                (
                    hauteur_optimisee,
                    sigma_optimisee,
                    fleche_optimisee,
                    facteur_securite_optimise,
                    masse_optimisee,
                ) = solution_optimisee
                reduction_masse = masse - masse_optimisee

                pourcentage_reduction = (reduction_masse / masse) * 100

                print(f"Hauteur minimale : {hauteur_optimisee * 1000:.1f} mm")

                print(f"Contrainte correspondante : {sigma_optimisee / 1e6:.2f} MPa")

                print(f"Flèche correspondante : {fleche_optimisee * 1000:.3f} mm")

                print(f"Facteur de sécurité : {facteur_securite_optimise:.2f}")

                print(f"Masse correspondante : {masse_optimisee:.2f} kg")
                print("\n--- COMPARAISON INITIAL / OPTIMISÉ ---")

                print(f"Hauteur initiale : {h * 1000:.1f} mm")

                print(f"Hauteur optimisée : {hauteur_optimisee * 1000:.1f} mm")

                print(f"Masse initiale : {masse:.2f} kg")

                print(f"Masse optimisée : {masse_optimisee:.2f} kg")

                print(f"Réduction de masse : {reduction_masse:.2f} kg")

                print(f"Réduction relative : {pourcentage_reduction:.1f} %")
                exporter_resultats_csv(
                    L,
                    b,
                    h,
                    F,
                    nom_materiau,
                    E,
                    Re,
                    densite,
                    volume,
                    masse,
                    moment_quadratique,
                    M_max,
                    sigma_max_MPa,
                    fleche_max_mm,
                    fleche_admissible_mm,
                    facteur_securite,
                    facteur_securite_minimal,
                    resistance_respectee,
                    rigidite_respectee,
                    hauteur_optimisee,
                    sigma_optimisee,
                    fleche_optimisee,
                    facteur_securite_optimise,
                    masse_optimisee,
                    reduction_masse,
                    pourcentage_reduction,
                )

            else:
                print(
                    "Aucune hauteur comprise entre 10 mm et 200 mm "
                    "ne respecte les deux critères."
                )
            solution_aluminium = rechercher_hauteur_minimale(
                L,
                b,
                F,
                E_aluminium,
                Re_aluminium,
                densite_aluminium,
                facteur_securite_minimal,
            )
            solution_acier = rechercher_hauteur_minimale(
                L, b, F, E_acier, Re_acier, densite_acier, facteur_securite_minimal
            )
        print("\n--- COMPARAISON DES SOLUTIONS OPTIMISÉES ---")

        if solution_aluminium is not None and solution_acier is not None:
            (
                hauteur_optimisee_aluminium,
                sigma_optimisee_aluminium,
                fleche_optimisee_aluminium,
                facteur_securite_optimise_aluminium,
                masse_optimisee_aluminium,
            ) = solution_aluminium
            (
                hauteur_optimisee_acier,
                sigma_optimisee_acier,
                fleche_optimisee_acier,
                facteur_securite_optimise_acier,
                masse_optimisee_acier,
            ) = solution_acier
            print("\nAluminium 2024-T3 :")
            print(f"Hauteur minimale : {hauteur_optimisee_aluminium * 1000:.1f} mm")
            print(f"Masse optimisée : {masse_optimisee_aluminium:.2f} kg")
            print(f"Contrainte : {sigma_optimisee_aluminium / 1e6:.2f} MPa")
            print(f"Flèche : {fleche_optimisee_aluminium * 1000:.3f} mm")
            print(f"Facteur de sécurité : {facteur_securite_optimise_aluminium:.2f}")

            print("\nAcier de construction :")
            print(f"Hauteur minimale : {hauteur_optimisee_acier * 1000:.1f} mm")
            print(f"Masse optimisée : {masse_optimisee_acier:.2f} kg")
            print(f"Contrainte : {sigma_optimisee_acier / 1e6:.2f} MPa")
            print(f"Flèche : {fleche_optimisee_acier * 1000:.3f} mm")
            print(f"Facteur de sécurité : {facteur_securite_optimise_acier:.2f}")
            print("\n--- AIDE AU CHOIX ---")

            if masse_optimisee_aluminium < masse_optimisee_acier:
                print(
                    "Solution la plus légère parmi les matériaux "
                    "étudiés : Aluminium 2024-T3."
                )
            elif masse_optimisee_acier < masse_optimisee_aluminium:
                print(
                    "Solution la plus légère parmi les matériaux "
                    "étudiés : Acier de construction."
                )
            else:
                print("Les deux solutions optimisées ont la même masse.")
            if hauteur_optimisee_aluminium < hauteur_optimisee_acier:
                print("Section de plus faible hauteur : Aluminium 2024-T3.")

            elif hauteur_optimisee_acier < hauteur_optimisee_aluminium:
                print("Section de plus faible hauteur : Acier de construction.")

            else:
                print("Les deux solutions ont la même hauteur.")
        else:
            print(
                "La comparaison est impossible : au moins un matériau "
                "ne possède aucune solution entre 10 mm et 200 mm."
            )

        # tracer_moment_flechissant(x, moment_flechissant)
        # tracer_effort_tranchant(x, effort_tranchant)
        # tracer_deformee(x, deformee)

        tracer_resultats_combines(
            x, effort_tranchant, moment_flechissant, deformee, nom_materiau
        )

    except ValueError:
        print("Erreur : veuillez entrer uniquement des valeurs numériques.")


def lancer_interface():
    fenetre = tk.Tk()

    fenetre.title("Outil de pré-dimensionnement d'une poutre encastrée")

    fenetre.geometry("850x800")
    fenetre.resizable(True, True)
    longueur_var = tk.StringVar(value="1.0")
    largeur_var = tk.StringVar(value="0.05")
    hauteur_var = tk.StringVar(value="0.10")
    force_var = tk.StringVar(value="1000")
    facteur_minimal_var = tk.StringVar(value="2.0")
    materiau_var = tk.StringVar(value="Aluminium 2024-T3")

    titre = ttk.Label(
        fenetre,
        text="Pré-dimensionnement d'une poutre encastrée",
        font=("Arial", 18, "bold"),
    )

    titre.pack(pady=20)

    sous_titre = ttk.Label(
        fenetre,
        text=(
            "Calcul de résistance, rigidité, masse et recherche d'une hauteur minimale"
        ),
        font=("Arial", 10),
    )

    sous_titre.pack(pady=(0, 15))

    cadre_saisie = ttk.LabelFrame(fenetre, text="Données d'entrée", padding=20)

    cadre_saisie.pack(fill="x", padx=30, pady=10)
    ttk.Label(cadre_saisie, text="Longueur L (m) :").grid(
        row=0, column=0, sticky="w", padx=10, pady=8
    )

    ttk.Entry(cadre_saisie, textvariable=longueur_var, width=20).grid(
        row=0, column=1, padx=10, pady=8
    )
    ttk.Label(cadre_saisie, text="Largeur b (m) :").grid(
        row=1, column=0, sticky="w", padx=10, pady=8
    )

    ttk.Entry(cadre_saisie, textvariable=largeur_var, width=20).grid(
        row=1, column=1, padx=10, pady=8
    )
    ttk.Label(cadre_saisie, text="Hauteur initiale h (m) :").grid(
        row=2, column=0, sticky="w", padx=10, pady=8
    )

    ttk.Entry(cadre_saisie, textvariable=hauteur_var, width=20).grid(
        row=2, column=1, padx=10, pady=8
    )
    ttk.Label(cadre_saisie, text="Force appliquée F (N) :").grid(
        row=3, column=0, sticky="w", padx=10, pady=8
    )

    ttk.Entry(cadre_saisie, textvariable=force_var, width=20).grid(
        row=3, column=1, padx=10, pady=8
    )
    ttk.Label(cadre_saisie, text="Facteur de sécurité minimal :").grid(
        row=4, column=0, sticky="w", padx=10, pady=8
    )

    ttk.Entry(cadre_saisie, textvariable=facteur_minimal_var, width=20).grid(
        row=4, column=1, padx=10, pady=8
    )
    ttk.Label(cadre_saisie, text="Matériau :").grid(
        row=5, column=0, sticky="w", padx=10, pady=8
    )
    liste_materiaux = ttk.Combobox(
        cadre_saisie,
        textvariable=materiau_var,
        values=["Aluminium 2024-T3", "Acier de construction"],
        state="readonly",
        width=25,
    )
    liste_materiaux.grid(row=5, column=1, padx=10, pady=8)
    cadre_resultats = ttk.LabelFrame(fenetre, text="Résultats du calcul", padding=15)

    cadre_resultats.pack(fill="both", expand=True, padx=30, pady=(0, 20))
    barre_defilement = ttk.Scrollbar(cadre_resultats, orient="vertical")
    texte_resultats = tk.Text(
        cadre_resultats,
        height=12,
        width=80,
        wrap="word",
        font=("Consolas", 10),
        yscrollcommand=barre_defilement.set,
    )
    barre_defilement.config(command=texte_resultats.yview)
    barre_defilement.pack(side="right", fill="y")

    texte_resultats.pack(side="left", fill="both", expand=True)
    texte_resultats.insert(
        "1.0", "Renseignez les données puis cliquez sur « Calculer et optimiser »."
    )

    def calculer_interface():
        try:
            L = float(longueur_var.get())
            b = float(largeur_var.get())
            h = float(hauteur_var.get())
            F = float(force_var.get())

            facteur_securite_minimal = float(facteur_minimal_var.get())

            nom_materiau = materiau_var.get()

            if L <= 0 or b <= 0 or h <= 0 or F <= 0 or facteur_securite_minimal <= 0:
                messagebox.showerror(
                    "Données invalides",
                    "Toutes les valeurs doivent être strictement positives.",
                )
                return

            if nom_materiau == "Aluminium 2024-T3":
                choix_materiau = 1
            else:
                choix_materiau = 2

            (nom_materiau, E, Re, densite) = selectionner_materiau(choix_materiau)

            volume = calculer_volume(L, b, h)
            masse = calculer_masse(densite, volume)

            moment_quadratique = calculer_moment_quadratique(b, h)
            M_max = calculer_moment_maximal(F, L)

            sigma_max = calculer_contrainte_maximale(M_max, h, moment_quadratique)

            sigma_max_MPa = sigma_max / 1e6

            fleche_max = calculer_fleche_maximale(F, L, E, moment_quadratique)

            fleche_max_mm = fleche_max * 1000

            fleche_admissible = calculer_fleche_admissible(L)
            fleche_admissible_mm = fleche_admissible * 1000

            facteur_securite = calculer_facteur_securite(Re, sigma_max)

            resistance_respectee = verifier_resistance(
                facteur_securite, facteur_securite_minimal
            )

            rigidite_respectee = verifier_rigidite(fleche_max, fleche_admissible)

            solution_optimisee = rechercher_hauteur_minimale(
                L, b, F, E, Re, densite, facteur_securite_minimal
            )
            resultat = (
                "--- SECTION INITIALE ---\n\n"
                f"Matériau : {nom_materiau}\n"
                f"Volume : {volume:.6f} m³\n"
                f"Masse : {masse:.2f} kg\n"
                f"Moment quadratique : {moment_quadratique:.6e} m⁴\n"
                f"Moment maximal : {M_max:.2f} N·m\n"
                f"Contrainte maximale : {sigma_max_MPa:.2f} MPa\n"
                f"Flèche maximale : {fleche_max_mm:.3f} mm\n"
                f"Flèche admissible : {fleche_admissible_mm:.3f} mm\n"
                f"Facteur de sécurité : {facteur_securite:.2f}\n"
                f"Facteur minimal demandé : "
                f"{facteur_securite_minimal:.2f}\n\n"
            )
            if resistance_respectee and rigidite_respectee:
                resultat += "Conclusion : dimensionnement initial validé.\n"
            else:
                resultat += "Conclusion : dimensionnement initial non validé.\n"
            if solution_optimisee is not None:
                (
                    hauteur_optimisee,
                    sigma_optimisee,
                    fleche_optimisee,
                    facteur_securite_optimise,
                    masse_optimisee,
                ) = solution_optimisee

                difference_masse = masse - masse_optimisee

                pourcentage_difference = (difference_masse / masse) * 100

                resultat += (
                    "\n--- SECTION OPTIMISÉE ---\n\n"
                    f"Hauteur minimale : "
                    f"{hauteur_optimisee * 1000:.1f} mm\n"
                    f"Masse optimisée : {masse_optimisee:.2f} kg\n"
                    f"Contrainte optimisée : "
                    f"{sigma_optimisee / 1e6:.2f} MPa\n"
                    f"Flèche optimisée : "
                    f"{fleche_optimisee * 1000:.3f} mm\n"
                    f"Facteur de sécurité optimisé : "
                    f"{facteur_securite_optimise:.2f}\n"
                    f"Différence de masse : "
                    f"{difference_masse:.2f} kg\n"
                    f"Différence relative : "
                    f"{pourcentage_difference:.1f} %\n"
                )

            else:
                resultat += "\nAucune solution trouvée entre 10 mm et 200 mm.\n"
            texte_resultats.delete("1.0", tk.END)
            texte_resultats.insert("1.0", resultat)
        except ValueError:
            messagebox.showerror(
                "Erreur de saisie", "Veuillez entrer uniquement des valeurs numériques."
            )

    bouton_calculer = ttk.Button(
        fenetre, text="Calculer et optimiser", command=calculer_interface
    )

    bouton_calculer.pack(before=cadre_resultats, pady=20)

    fenetre.mainloop()


if __name__ == "__main__":
    # main()
    lancer_interface()
