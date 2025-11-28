# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""simulateur.py - Orchestrateur de la simulation Distance-Vector.
Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations
import heapq
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List

from .evenement import Evenement
from .lien import Lien
from .routeur import Routeur


class Simulateur:
    """Gere l'agenda, le temps simule et la construction du reseau."""

    # ------------------------------------------------------------------ #
    # Initialisation & logger

    def __init__(self, mode_verbeux: bool = False):
        self.mode_verbeux = mode_verbeux
        self.temps_ms = 0.0
        self._seq_evt = 0
        self._agenda: List[Evenement] = []
        self.routeurs: Dict[int, Routeur] = {}
        self.liens: List[Lien] = []

        self._configurer_logs()

    def _configurer_logs(self) -> None:
        fmt = "@%(temps).3f s %(message)s"

        class Adapt(logging.LoggerAdapter):
            """Ajoute le temps simule courant dans chaque entree de log."""

            def __init__(self, logger: logging.Logger, simulateur: "Simulateur"):
                super().__init__(logger, {})
                self.simulateur = simulateur

            def process(self, msg, kwargs):
                kwargs.setdefault("extra", {})["temps"] = self.simulateur.temps_ms / 1000
                return msg, kwargs

        base_logger = logging.getLogger("dv")
        base_logger.handlers.clear()
        base_logger.setLevel(logging.INFO if self.mode_verbeux else logging.WARNING)

        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(fmt))
        base_logger.addHandler(h)

        self.log = Adapt(base_logger, self)

    # ------------------------------------------------------------------ #
    # Agenda

    def planifier(self, dans_ms: float, action):
        """Place une action dans l’agenda à exécuter après `dans_ms` millisecondes simulées."""
        evt = Evenement(self.temps_ms + dans_ms, self._seq_evt, action)
        self._seq_evt += 1
        heapq.heappush(self._agenda, evt)

    def _prochain_evt(self) -> Evenement | None:
        return heapq.heappop(self._agenda) if self._agenda else None

    # ------------------------------------------------------------------ #
    # Construction du reseau

    def _routeur(self, rid: int) -> Routeur:
        if rid not in self.routeurs:
            self.routeurs[rid] = Routeur(rid, self)
        return self.routeurs[rid]

    def ajouter_lien(self, spec: dict) -> None:
        lien = Lien(
            spec["endpoints"][0],
            spec["endpoints"][1],
            spec["distance"],
            spec["propagation_speed"],
            spec["transmission_speed"],
            spec["cost"],
        )
        self.liens.append(lien)
        self._routeur(lien.a).ajouter_lien(lien)
        self._routeur(lien.b).ajouter_lien(lien)

    # ----- evenements dynamiques -------------------------------------- #

    def _planifier_changement_cout(self, ev: dict) -> None:
        temps = ev["time"]
        a, b = ev["link"]

        for lien in self.liens:
            if {lien.a, lien.b} == {a, b}:

                def action(l=lien, ev=ev):
                    ancien = l.cout_admin
                    if ev.get("down"):
                        l.mettre_hors_service()
                    else:
                        l.changer_cout(ev["new_cost"])
                    self.log.info(
                        "Lien %d-%d cout %.0f -> %.0f", l.a, l.b, ancien, l.cout_admin
                    )
                    # les deux extremites renvoient un DV
                    for rid in (l.a, l.b):
                        self.routeurs[rid].envoyer_dv()

                self.planifier(temps, action)
                break

    # ------------------------------------------------------------------ #
    # Boucle de la simulation

    def executer(self) -> None:
        """Déroule l’agenda jusqu’à stabilisation en appliquant les actions planifiées."""
        # DV initiaux
        for r in self.routeurs.values():
            r.envoyer_dv()

        while self._agenda:
            evt = self._prochain_evt()
            self.temps_ms = evt.instant_ms
            evt.action()

    # ------------------------------------------------------------------ #
    # Affichage final

    def afficher_tables(self) -> None:
        """Affiche les tables de routage finales de chaque routeur (stdout)."""
        for rid in sorted(self.routeurs):
            print(f"-- Routeur {rid} --")
            print("dest\tcost\tnext-hop")
            t = self.routeurs[rid].table
            for dest, e in sorted(t._table.items()):
                print(f"{dest}\t{e.cout}\t{e.prochain_saut}")

    # ------------------------------------------------------------------ #
    # Chargement JSON

    @classmethod
    def charger_depuis_json(cls, chemin: Path, mode_verbeux=False) -> "Simulateur":
        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)

        sim = cls(mode_verbeux)
        for lien in data["links"]:
            sim.ajouter_lien(lien)
        for ev in data.get("events", []):
            if ev["type"] == "cost_change":
                sim._planifier_changement_cout(ev)
        return sim
