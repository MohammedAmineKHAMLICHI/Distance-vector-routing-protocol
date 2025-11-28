from math import inf

from simulateur_dv.table_routage import EntreeTable, TableRoutage


def test_vecteur_poison_masks_routes_via_voisin():
    table = TableRoutage(1)
    table._table[2] = EntreeTable(2, 5, 2)
    table._table[3] = EntreeTable(3, 7, 2)
    table._table[4] = EntreeTable(4, 4, 3)

    vecteur = table.vecteur_poison(2)

    assert vecteur[2] == 5  # destination = voisin reste connue
    assert vecteur[3] is inf  # route via voisin 2 est masquee
    assert vecteur[4] == 4  # route via un autre voisin reste intacte


def test_mise_a_jour_selectionne_le_meilleur_voisin():
    table = TableRoutage(1)
    dv_voisins = {2: {3: 5}, 3: {3: 2}}
    couts_voisins = {2: 1, 3: 3}

    changed = table.mise_a_jour(dv_voisins, couts_voisins)

    assert changed is True
    entree_3 = table._table[3]
    assert entree_3.cout == 5  # 3 (voisin) + 2 (DV voisin 3)
    assert entree_3.prochain_saut == 3
