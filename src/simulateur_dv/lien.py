# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""lien.py - Modelise un lien bidirectionnel entre deux routeurs.
Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from math import inf

class Lien:
    """Lien physique : distance, vitesses, cout administratif et etat."""

    def __init__(self,
                 a: int,
                 b: int,
                 distance: float,
                 vitesse_propagation: float,
                 debit: float,
                 cout_admin: float):
        self.a = a
        self.b = b
        self.distance = distance
        self.v_prop = vitesse_propagation
        self.debit = debit
        self.cout_admin = cout_admin
        self.actif = True  # si False -> lien tombe (cout = +inf)

    # ------------------------------------------------------------------
    def autre_extremite(self, rid: int) -> int:
        if rid == self.a:
            return self.b
        if rid == self.b:
            return self.a
        raise ValueError("Le routeur {} n'est pas relie a ce lien".format(rid))

    # ------------------------------------------------------------------
    def delai_transmission(self, taille_bits: int) -> float:
        """Temps total (en secondes) pour envoyer un paquet de taille_bits."""
        t_prop = self.distance / self.v_prop
        t_trans = taille_bits / self.debit
        return t_prop + t_trans

    # ------------------------------------------------------------------
    # Gestion des couts / pannes
    def changer_cout(self, nouveau: float):
        self.cout_admin = nouveau

    def mettre_hors_service(self):
        self.actif = False
        self.cout_admin = inf
