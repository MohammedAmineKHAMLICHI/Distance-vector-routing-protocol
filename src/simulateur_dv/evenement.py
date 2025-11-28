# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""evenement.py - Definition d'un evenement planifie dans la timeline du simulateur.
Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from dataclasses import dataclass
from typing import Callable, Any

@dataclass(order=True)
class Evenement:
    """Objet stocke dans le tas de priorite.
    Les deux premiers champs servent de cle pour heapq :
     - instant_ms  - date d'execution
     - compteur    - brise-egalite stable
    Le champ action est une fonction sans argument a executer.
    """

    instant_ms: float
    compteur: int
    action: Callable[[], Any]
