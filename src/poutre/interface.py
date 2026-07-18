"""Interface graphique du pré-dimensionnement d'une poutre encastrée."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .dimensionnement import dimensionner_poutre
from .export import exporter_dimensionnement_csv
from .materiaux import (
    ALUMINIUM_2024_T3,
    MATERIAUX_DISPONIBLES,
    obtenir_materiau,
)
from .modeles import DonneesPoutre, ResultatDimensionnement

VALEURS_PAR_DEFAUT = {
    "longueur_m": "1.0",
    "largeur_m": "0.05",
    "hauteur_initiale_m": "0.10",
    "force_n": "1000",
    "facteur_securite_minimal": "2.0",
    "rapport_fleche": "250",
    "hauteur_min_mm": "10",
    "hauteur_max_mm": "200",
    "pas_mm": "1",
}


class ApplicationPoutre(ttk.Frame):
    """Fenêtre principale de l'outil de pré-dimensionnement."""

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent, padding=20)

        self.parent = parent
        self.resultat: ResultatDimensionnement | None = None

        self.variables = {
            nom: tk.StringVar(value=valeur)
            for nom, valeur in VALEURS_PAR_DEFAUT.items()
        }

        self.materiau_var = tk.StringVar(value=ALUMINIUM_2024_T3.nom)
        self.resume_var = tk.StringVar(
            value="Renseignez les données puis lancez le dimensionnement."
        )

        self._construire_interface()

    def _construire_interface(self) -> None:
        """Construit et positionne tous les composants graphiques."""

        self.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        titre = ttk.Label(
            self,
            text="Pré-dimensionnement d'une poutre encastrée",
            style="Titre.TLabel",
        )
        titre.grid(
            row=0,
            column=0,
            pady=(0, 15),
        )

        cadre_entrees = ttk.LabelFrame(
            self,
            text="Données d'entrée",
            padding=15,
        )
        cadre_entrees.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        for colonne in range(4):
            cadre_entrees.columnconfigure(
                colonne,
                weight=1 if colonne in (1, 3) else 0,
            )

        self._ajouter_champ(
            cadre_entrees,
            "Longueur L (m)",
            "longueur_m",
            ligne=0,
            colonne=0,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Largeur b (m)",
            "largeur_m",
            ligne=0,
            colonne=2,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Hauteur initiale h (m)",
            "hauteur_initiale_m",
            ligne=1,
            colonne=0,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Force F (N)",
            "force_n",
            ligne=1,
            colonne=2,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Facteur de sécurité minimal",
            "facteur_securite_minimal",
            ligne=2,
            colonne=0,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Critère de flèche L/",
            "rapport_fleche",
            ligne=2,
            colonne=2,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Hauteur minimale (mm)",
            "hauteur_min_mm",
            ligne=3,
            colonne=0,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Hauteur maximale (mm)",
            "hauteur_max_mm",
            ligne=3,
            colonne=2,
        )
        self._ajouter_champ(
            cadre_entrees,
            "Pas de recherche (mm)",
            "pas_mm",
            ligne=4,
            colonne=0,
        )

        ttk.Label(
            cadre_entrees,
            text="Matériau",
        ).grid(
            row=4,
            column=2,
            sticky="w",
            padx=(10, 5),
            pady=5,
        )

        self.liste_materiaux = ttk.Combobox(
            cadre_entrees,
            textvariable=self.materiau_var,
            values=[materiau.nom for materiau in MATERIAUX_DISPONIBLES],
            state="readonly",
        )
        self.liste_materiaux.grid(
            row=4,
            column=3,
            sticky="ew",
            padx=(5, 10),
            pady=5,
        )

        cadre_actions = ttk.Frame(
            self,
            padding=(0, 15),
        )
        cadre_actions.grid(
            row=2,
            column=0,
        )

        ttk.Button(
            cadre_actions,
            text="Calculer et optimiser",
            command=self._calculer,
        ).grid(
            row=0,
            column=0,
            padx=5,
        )

        self.bouton_exporter = ttk.Button(
            cadre_actions,
            text="Exporter en CSV",
            command=self._exporter,
            state="disabled",
        )
        self.bouton_exporter.grid(
            row=0,
            column=1,
            padx=5,
        )

        ttk.Button(
            cadre_actions,
            text="Réinitialiser",
            command=self._reinitialiser,
        ).grid(
            row=0,
            column=2,
            padx=5,
        )

        cadre_resultats = ttk.LabelFrame(
            self,
            text="Résultats du dimensionnement",
            padding=10,
        )
        cadre_resultats.grid(
            row=3,
            column=0,
            sticky="nsew",
        )
        cadre_resultats.rowconfigure(0, weight=1)
        cadre_resultats.columnconfigure(0, weight=1)

        self.tableau = ttk.Treeview(
            cadre_resultats,
            columns=("propriete", "initiale", "optimisee"),
            show="headings",
            height=12,
        )

        self.tableau.heading(
            "propriete",
            text="Propriété",
        )
        self.tableau.heading(
            "initiale",
            text="Section initiale",
        )
        self.tableau.heading(
            "optimisee",
            text="Section optimisée",
        )

        self.tableau.column(
            "propriete",
            width=260,
            anchor="w",
        )
        self.tableau.column(
            "initiale",
            width=220,
            anchor="center",
        )
        self.tableau.column(
            "optimisee",
            width=220,
            anchor="center",
        )

        barre = ttk.Scrollbar(
            cadre_resultats,
            orient="vertical",
            command=self.tableau.yview,
        )
        self.tableau.configure(
            yscrollcommand=barre.set,
        )

        self.tableau.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        barre.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        ttk.Label(
            self,
            textvariable=self.resume_var,
            style="Resume.TLabel",
            anchor="center",
        ).grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(15, 0),
        )

    def _ajouter_champ(
        self,
        parent: ttk.LabelFrame,
        texte: str,
        nom_variable: str,
        ligne: int,
        colonne: int,
    ) -> None:
        """Ajoute un libellé et un champ de saisie."""

        ttk.Label(
            parent,
            text=texte,
        ).grid(
            row=ligne,
            column=colonne,
            sticky="w",
            padx=(10, 5),
            pady=5,
        )

        ttk.Entry(
            parent,
            textvariable=self.variables[nom_variable],
        ).grid(
            row=ligne,
            column=colonne + 1,
            sticky="ew",
            padx=(5, 10),
            pady=5,
        )

    def _lire_float(
        self,
        nom_variable: str,
        libelle: str,
    ) -> float:
        """Lit un nombre décimal en acceptant le point ou la virgule."""

        texte = self.variables[nom_variable].get().strip()
        texte = texte.replace(",", ".")

        try:
            return float(texte)
        except ValueError as erreur:
            raise ValueError(f"{libelle} doit être une valeur numérique.") from erreur

    def _lire_entier(
        self,
        nom_variable: str,
        libelle: str,
    ) -> int:
        """Lit un entier utilisé pour la grille de recherche."""

        texte = self.variables[nom_variable].get().strip()

        try:
            return int(texte)
        except ValueError as erreur:
            raise ValueError(f"{libelle} doit être un nombre entier.") from erreur

    def _construire_donnees(self) -> DonneesPoutre:
        """Construit les données métier depuis les champs de saisie."""

        return DonneesPoutre(
            longueur_m=self._lire_float(
                "longueur_m",
                "La longueur",
            ),
            largeur_m=self._lire_float(
                "largeur_m",
                "La largeur",
            ),
            hauteur_initiale_m=self._lire_float(
                "hauteur_initiale_m",
                "La hauteur initiale",
            ),
            force_n=self._lire_float(
                "force_n",
                "La force",
            ),
            facteur_securite_minimal=self._lire_float(
                "facteur_securite_minimal",
                "Le facteur de sécurité minimal",
            ),
            materiau=obtenir_materiau(self.materiau_var.get()),
            rapport_fleche=self._lire_float(
                "rapport_fleche",
                "Le rapport de flèche",
            ),
        )

    def _calculer(self) -> None:
        """Lance le dimensionnement à partir des données saisies."""

        try:
            donnees = self._construire_donnees()

            resultat = dimensionner_poutre(
                donnees,
                hauteur_min_mm=self._lire_entier(
                    "hauteur_min_mm",
                    "La hauteur minimale",
                ),
                hauteur_max_mm=self._lire_entier(
                    "hauteur_max_mm",
                    "La hauteur maximale",
                ),
                pas_mm=self._lire_entier(
                    "pas_mm",
                    "Le pas de recherche",
                ),
            )
        except (TypeError, ValueError) as erreur:
            messagebox.showerror(
                "Données invalides",
                str(erreur),
                parent=self.parent,
            )
            return

        self.resultat = resultat
        self._afficher_resultat(resultat)
        self.bouton_exporter.configure(state="normal")

    def _afficher_resultat(
        self,
        resultat: ResultatDimensionnement,
    ) -> None:
        """Affiche les résultats initiaux et optimisés dans le tableau."""

        for element in self.tableau.get_children():
            self.tableau.delete(element)

        initiale = resultat.section_initiale
        optimisee = resultat.optimisation

        if optimisee is None:
            valeur_optimisee = "Aucune solution"
            hauteur_optimisee = valeur_optimisee
            inertie_optimisee = valeur_optimisee
            volume_optimise = valeur_optimisee
            masse_optimisee = valeur_optimisee
            contrainte_optimisee = valeur_optimisee
            fleche_optimisee = valeur_optimisee
            securite_optimisee = valeur_optimisee
            conformite_optimisee = "Non"
            critere_optimise = "—"
            reduction = "—"
        else:
            hauteur_optimisee = f"{optimisee.hauteur_mm}"
            inertie_optimisee = f"{optimisee.moment_quadratique_m4:.6e}"
            volume_optimise = f"{optimisee.volume_m3:.6f}"
            masse_optimisee = f"{optimisee.masse_kg:.3f}"
            contrainte_optimisee = f"{optimisee.contrainte_maximale_mpa:.2f}"
            fleche_optimisee = f"{optimisee.fleche_maximale_mm:.3f}"
            securite_optimisee = f"{optimisee.facteur_securite:.2f}"
            conformite_optimisee = "Oui"
            critere_optimise = optimisee.critere_dimensionnant.value

            pourcentage = resultat.difference_masse_pourcentage
            reduction = f"{pourcentage:.1f} %" if pourcentage is not None else "—"

        lignes = [
            (
                "Hauteur (mm)",
                f"{initiale.hauteur_mm:.1f}",
                hauteur_optimisee,
            ),
            (
                "Moment quadratique (m⁴)",
                f"{initiale.moment_quadratique_m4:.6e}",
                inertie_optimisee,
            ),
            (
                "Volume (m³)",
                f"{initiale.volume_m3:.6f}",
                volume_optimise,
            ),
            (
                "Masse (kg)",
                f"{initiale.masse_kg:.3f}",
                masse_optimisee,
            ),
            (
                "Contrainte maximale (MPa)",
                f"{initiale.contrainte_maximale_mpa:.2f}",
                contrainte_optimisee,
            ),
            (
                "Flèche maximale (mm)",
                f"{initiale.fleche_maximale_mm:.3f}",
                fleche_optimisee,
            ),
            (
                "Flèche admissible (mm)",
                f"{initiale.fleche_admissible_mm:.3f}",
                f"{initiale.fleche_admissible_mm:.3f}",
            ),
            (
                "Facteur de sécurité",
                f"{initiale.facteur_securite:.2f}",
                securite_optimisee,
            ),
            (
                "Dimensionnement conforme",
                "Oui" if initiale.est_admissible else "Non",
                conformite_optimisee,
            ),
            (
                "Critère dimensionnant",
                "—",
                critere_optimise,
            ),
            (
                "Réduction de masse",
                "—",
                reduction,
            ),
        ]

        for ligne in lignes:
            self.tableau.insert(
                "",
                "end",
                values=ligne,
            )

        if optimisee is None:
            self.resume_var.set("Aucune solution admissible dans la plage demandée.")
            return

        difference = resultat.difference_masse_kg
        pourcentage = resultat.difference_masse_pourcentage

        self.resume_var.set(
            "Hauteur optimale : "
            f"{optimisee.hauteur_mm} mm | "
            f"Gain de masse : {difference:.3f} kg | "
            f"Réduction : {pourcentage:.1f} % | "
            "Critère : "
            f"{optimisee.critere_dimensionnant.value}"
        )

    def _exporter(self) -> None:
        """Demande une destination puis exporte le dernier résultat."""

        if self.resultat is None:
            messagebox.showwarning(
                "Aucun résultat",
                "Lancez d'abord un dimensionnement.",
                parent=self.parent,
            )
            return

        destination = filedialog.asksaveasfilename(
            parent=self.parent,
            title="Exporter les résultats",
            defaultextension=".csv",
            filetypes=[
                ("Fichier CSV", "*.csv"),
                ("Tous les fichiers", "*.*"),
            ],
            initialfile="resultats_dimensionnement.csv",
        )

        if not destination:
            return

        try:
            chemin = exporter_dimensionnement_csv(
                self.resultat,
                destination,
            )
        except (OSError, TypeError, ValueError) as erreur:
            messagebox.showerror(
                "Erreur d'export",
                str(erreur),
                parent=self.parent,
            )
            return

        messagebox.showinfo(
            "Export terminé",
            f"Fichier créé :\n{chemin}",
            parent=self.parent,
        )

    def _reinitialiser(self) -> None:
        """Restaure les valeurs du cas de référence."""

        for nom, valeur in VALEURS_PAR_DEFAUT.items():
            self.variables[nom].set(valeur)

        self.materiau_var.set(ALUMINIUM_2024_T3.nom)
        self.resultat = None
        self.bouton_exporter.configure(state="disabled")

        for element in self.tableau.get_children():
            self.tableau.delete(element)

        self.resume_var.set("Renseignez les données puis lancez le dimensionnement.")


def lancer_interface() -> None:
    """Crée la fenêtre principale et démarre la boucle graphique."""

    fenetre = tk.Tk()
    fenetre.title("Pré-dimensionnement d'une poutre encastrée")
    fenetre.geometry("1000x720")
    fenetre.minsize(850, 650)

    style = ttk.Style(fenetre)

    if "vista" in style.theme_names():
        style.theme_use("vista")

    style.configure(
        "Titre.TLabel",
        font=("Segoe UI", 20, "bold"),
    )
    style.configure(
        "Resume.TLabel",
        font=("Segoe UI", 11, "bold"),
    )

    ApplicationPoutre(fenetre)
    fenetre.mainloop()


if __name__ == "__main__":
    lancer_interface()
