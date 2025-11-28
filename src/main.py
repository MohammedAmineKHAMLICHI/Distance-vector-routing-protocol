# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Point d'entrée CLI du simulateur Distance-Vector.
Charge un scénario JSON, exécute la simulation puis affiche les tables finales.

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""
# Auteurs : Mohammed KHAMLICHI et Gedeon DASSI KOUAM
#!/usr/bin/env python3
import argparse
from pathlib import Path
from simulateur_dv import Simulateur

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulateur Distance-Vector (mode verbeux active par defaut)")
    parser.add_argument("scenario", type=Path, help="Fichier JSON du scenario")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Desactive les logs verbeux",
    )
    args = parser.parse_args()

    sim = Simulateur.charger_depuis_json(args.scenario, mode_verbeux=not args.quiet)
    sim.executer()
    sim.afficher_tables()

if __name__ == "__main__":
    main()
