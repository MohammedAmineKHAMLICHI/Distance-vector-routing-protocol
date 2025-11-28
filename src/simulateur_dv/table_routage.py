# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""table_routage.py - Maintient les meilleures routes d'un routeur.
Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from dataclasses import dataclass
from math import inf
from typing import Dict, Optional

@dataclass
class EntreeTable:
    destination: int
    cout: float
    prochain_saut: Optional[int]

class TableRoutage:
    """Implemente l'algorithme Distance-Vector pour un routeur donne."""

    def __init__(self, identifiant: int):
        self.id = identifiant
        self._table: Dict[int, EntreeTable] = {
            identifiant: EntreeTable(identifiant, 0, identifiant)
        }

    # ------------------------------------------------------------
    @property
    def vecteur(self) -> Dict[int, float]:
        """Retourne le vecteur des coûts actuels vers chaque destination connue."""
        return {dest: e.cout for dest, e in self._table.items()}

    def vecteur_poison(self, voisin: int) -> Dict[int, float]:
        """Retourne le DV en appliquant le poison reverse pour un voisin donné."""
        v = {}
        for dest, e in self._table.items():
            if dest != voisin and e.prochain_saut == voisin:
                v[dest] = inf
            else:
                v[dest] = e.cout
        return v

    # ------------------------------------------------------------
    def _entree(self, dest: int) -> EntreeTable:
        return self._table.get(dest, EntreeTable(dest, inf, None))

    # ------------------------------------------------------------
    def mise_a_jour(self,
                    dv_voisins: Dict[int, Dict[int, float]],
                    couts_voisins: Dict[int, float]) -> bool:
        """Recalcule la table de routage. Renvoie True si une modification est détectée."""
        import copy
        ancienne_table = copy.deepcopy(self._table)
        destinations = set(ancienne_table)
        for dv in dv_voisins.values():
            destinations.update(dv)

        nouvelle: Dict[int, EntreeTable] = {
            self.id: EntreeTable(self.id, 0, self.id)
        }

        for dest in destinations:
            if dest == self.id:
                continue
            meilleur = (inf, None)
            for voisin, cout_lien in couts_voisins.items():
                cout_voisin = dv_voisins.get(voisin, {}).get(dest, inf)
                tot = cout_lien + cout_voisin
                if tot < meilleur[0]:
                    meilleur = (tot, voisin)
            if meilleur[1] is not None:
                nouvelle[dest] = EntreeTable(dest, meilleur[0], meilleur[1])

        self._table = nouvelle
        return nouvelle != ancienne_table

    # ------------------------------------------------------------
    def diff(self, autre: 'TableRoutage') -> Dict[int, tuple]:
        """Retourne {dest: (ancien_cout, nouveau_cout, nouveau_next)} pour les entrées modifiées."""
        changements = {}
        for dest, new_e in self._table.items():
            old_e = autre._table.get(dest)
            if old_e is None or old_e.cout != new_e.cout or old_e.prochain_saut != new_e.prochain_saut:
                changements[dest] = (old_e.cout if old_e else float('inf'),
                                     new_e.cout,
                                     new_e.prochain_saut)
        # destinations supprimees
        for dest in autre._table:
            if dest not in self._table:
                changements[dest] = (autre._table[dest].cout, float('inf'), None)
        return changements
