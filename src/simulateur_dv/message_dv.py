# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""message_dv.py - Contient la structure d'un paquet Distance-Vector.
Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from dataclasses import dataclass
from typing import Dict

TAILLE_ENTREE_BITS = 32  # (destination, cout) simplifie

@dataclass
class MessageDV:
    """Vecteur de distances echange entre deux routeurs voisins."""

    expediteur: int
    distances: Dict[int, float]

    # ------------------------------------------------------------------
    @property
    def taille_bits(self) -> int:
        """Nombre de bits transportes - impacte le delai de transmission."""
        return len(self.distances) * TAILLE_ENTREE_BITS
