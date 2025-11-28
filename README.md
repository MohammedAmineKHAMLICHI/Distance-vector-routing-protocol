# Simulateur de routage Distance-Vector
[![CI](https://github.com/MohammedAmineKHAMLICHI/Distance-vector-routing-protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/MohammedAmineKHAMLICHI/Distance-vector-routing-protocol/actions/workflows/ci.yml)

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/

## 🎯 Résumé du projet
Simulateur pédagogique en Python de l’algorithme Distance-Vector (type RIP). Le programme charge un scénario JSON, simule la diffusion des vecteurs de distance avec poison reverse, journalise les événements et affiche les tables finales.

## 🧭 Contexte et objectif
Contexte réseau et protocoles de routage. Objectif principal : illustrer le comportement Distance-Vector (propagation, count-to-infinity, changements de coût) sur des topologies simples.

## 🔑 Fonctionnalités principales
- Lecture de scénarios JSON (liens, événements de changement de coût ou mise hors service).
- Gestion d’un agenda d’événements et simulation du temps de propagation/transmission.
- Poison reverse pour limiter le count-to-infinity.
- Logs horodatés et affichage final des tables.
- Suite de tests pytest couvrant les scénarios fournis.

## 🛠️ Stack technique
- Python 3.10+
- Standard library uniquement
- Pytest pour les tests

## ⚙️ Installation
1. Cloner le dépôt.
2. (Optionnel) Créer un environnement virtuel : `python -m venv .venv`.
3. Activer l’environnement si créé.
4. Installer pytest pour les tests : `pip install pytest`.

## 🚀 Utilisation
```bash
python src/main.py src/scenarios/scenario_validation.json         # mode verbeux par défaut
python src/main.py src/scenarios/scenario_validation.json --quiet # sortie tables uniquement
```
Scénarios disponibles : `scenario_validation.json`, `scenario_count_to_infinity.json`, `scenario_delays.json`.

## 🗂️ Structure du dépôt
- `src/main.py` : point d’entrée CLI
- `src/simulateur_dv/` : simulateur, routeurs, liens, messages, tables
- `src/scenarios/` : topologies et événements JSON
- `tests/` : tests pytest (tables et scénarios)
- `.github/workflows/ci.yml` : CI GitHub Actions (pytest)

## ✅ Tests
- Commande : `pytest`
- CI : workflow GitHub Actions `ci.yml` (Python 3.11)

## 🌟 Compétences mises en avant
- Modélisation de protocoles de routage (Distance-Vector, poison reverse)
- Simulation d’événements et gestion du temps
- Tests automatisés et CI GitHub Actions
- Manipulation de fichiers de configuration JSON
