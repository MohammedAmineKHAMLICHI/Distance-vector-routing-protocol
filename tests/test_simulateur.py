from pathlib import Path

from simulateur_dv import Simulateur


def test_scenario_validation_tables_stables():
    sim = Simulateur.charger_depuis_json(
        Path("src/scenarios/scenario_validation.json"), mode_verbeux=False
    )
    sim.executer()

    attendu = {
        1: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4},
        2: {2: 0, 1: 1, 3: 3, 4: 2, 5: 3},
        3: {3: 0, 1: 2, 2: 3, 4: 5, 5: 5},
        4: {4: 0, 1: 3, 2: 2, 3: 5, 5: 1},
        5: {5: 0, 1: 4, 2: 3, 3: 5, 4: 1},
    }

    for rid, vecteur in attendu.items():
        assert sim.routeurs[rid].table.vecteur == vecteur


def test_scenario_count_to_infinity_limite_par_poison_reverse():
    sim = Simulateur.charger_depuis_json(
        Path("src/scenarios/scenario_count_to_infinity.json"), mode_verbeux=False
    )
    sim.executer()

    # Les couts se stabilisent malgre la suppression d'un lien grace au poison reverse.
    assert sim.routeurs[1].table.vecteur == {1: 0, 2: 51, 3: 50}
    assert sim.routeurs[2].table.vecteur == {2: 0, 1: 51, 3: 1}
    assert sim.routeurs[3].table.vecteur == {3: 0, 1: 50, 2: 1}
