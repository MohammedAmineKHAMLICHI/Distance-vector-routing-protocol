# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""routeur.py - Logique d'un routeur Distance-Vector.
Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations
from typing import Dict, TYPE_CHECKING
import copy

from .message_dv import MessageDV
from .table_routage import TableRoutage

if TYPE_CHECKING:
    from .simulateur import Simulateur
    from .lien import Lien

class Routeur:
    """Noeud du reseau : conserve une table et echange des DV."""

    def __init__(self, identifiant: int, sim: 'Simulateur'):
        self.id = identifiant
        self.sim = sim
        self.liens: Dict[int, 'Lien'] = {}  # voisin -> Lien
        self.table = TableRoutage(identifiant)
        self.dv_voisins: Dict[int, Dict[int, float]] = {}

    # ------------------------------------------------------------
    def ajouter_lien(self, lien: 'Lien'):
        """Associe un lien bidirectionnel à ce routeur (indexé par l’identifiant voisin)."""
        self.liens[lien.autre_extremite(self.id)] = lien

    # ------------------------------------------------------------
    def envoyer_dv(self):
        """Diffuse le vecteur de distances aux voisins actifs (poison reverse inclus)."""
        for voisin, lien in self.liens.items():
            if not lien.actif:
                continue
            distances = self.table.vecteur_poison(voisin)
            message = MessageDV(self.id, distances)
            delai_ms = lien.delai_transmission(message.taille_bits) * 1000  # secondes -> ms
            # planifie la reception chez le voisin
            self.sim.planifier(delai_ms,
                               lambda v=voisin, m=message: self.sim.routeurs[v].recevoir_dv(m))
            # log
            self.sim.log.info("Routeur %d envoie DV a %d: %s %% lien %d-%d %g bps",
                              self.id, voisin, message.distances, lien.a, lien.b, lien.debit)

    # ------------------------------------------------------------
    def recevoir_dv(self, message: MessageDV):
        """Met à jour la table locale à la réception d’un DV, puis relance la diffusion si nécessaire."""
        self.sim.log.info("Routeur %d recoit DV de %d: %s",
                          self.id, message.expediteur, message.distances)
        self.dv_voisins[message.expediteur] = message.distances

        ancienne = copy.deepcopy(self.table)
        if self.table.mise_a_jour(self.dv_voisins,
                                  {v: l.cout_admin for v, l in self.liens.items()}):
            # log les changements
            for dest, (old_cost, new_cost, new_nh) in self.table.diff(ancienne).items():
                raison = "nouvelle destination" if old_cost == float('inf') else "cout modifie"
                if new_cost == float('inf'):
                    raison = "destination retiree"
                self.sim.log.info(
                    "Routeur %d : %s pour %d (%.0f -> %.0f) via %s",
                    self.id, raison, dest, old_cost, new_cost,
                    'N/A' if new_nh is None else new_nh)
            # retransmet
            self.envoyer_dv()
