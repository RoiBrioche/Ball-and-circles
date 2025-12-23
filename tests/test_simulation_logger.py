"""Tests unitaires pour le module simulation_logger."""

import json
import os
import pytest
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

# Import des classes à tester
from src.simulation_logger import SimulationLogger
from src.balle import RebondEvent, Balle


class TestSimulationLogger:
    """Tests pour la classe SimulationLogger."""

    def test_initialization(self):
        """Teste l'initialisation du logger."""
        # GIVEN - WHEN: Création d'une instance de SimulationLogger
        logger = SimulationLogger()

        # THEN: Vérification des valeurs par défaut
        assert logger.fps is None
        assert logger.rebounds == []
        assert logger.output_file == "rebonds_log.json"

    def test_set_fps(self):
        """Teste la définition du FPS."""
        # GIVEN: Un logger initialisé
        logger = SimulationLogger()

        # WHEN: On définit le FPS
        test_fps = 60
        logger.set_fps(test_fps)

        # THEN: Le FPS est correctement défini
        assert logger.fps == test_fps

    def test_log_rebound(self):
        """Teste l'ajout d'un événement de rebond."""
        # GIVEN: Un logger initialisé et un événement de rebond
        logger = SimulationLogger()
        test_event = RebondEvent(index=1, time_sec=1.5, vitesse=10.5, position=(100.0, 200.0))

        # WHEN: On enregistre l'événement
        logger.log_rebound(test_event)

        # THEN: L'événement est correctement enregistré
        assert len(logger.rebounds) == 1
        assert logger.rebounds[0]["index"] == test_event.index
        assert logger.rebounds[0]["time_sec"] == test_event.time_sec
        assert logger.rebounds[0]["vitesse"] == test_event.vitesse
        assert logger.rebounds[0]["position"] == list(test_event.position)

    def test_log_rebound_invalid_type(self):
        """Teste qu'une erreur est levée si l'événement n'est pas un RebondEvent."""
        # GIVEN: Un logger initialisé et un événement invalide
        logger = SimulationLogger()
        invalid_event = {"not": "a ReboundEvent"}

        # WHEN/THEN: On vérifie que l'erreur est levée
        with pytest.raises(ValueError, match="L'événement doit être une instance de RebondEvent"):
            logger.log_rebound(invalid_event)

    def test_flush_creates_file(self, tmp_path):
        """Teste que flush() crée bien un fichier JSON."""
        # GIVEN: Un logger avec un fichier de sortie temporaire
        output_file = tmp_path / "test_rebonds.json"
        logger = SimulationLogger(output_file=str(output_file))

        # Ajout d'un événement de test
        test_event = RebondEvent(index=1, time_sec=1.5, vitesse=10.5, position=(100.0, 200.0))
        logger.log_rebound(test_event)
        logger.set_fps(60)

        # WHEN: On écrit dans le fichier
        logger.flush()

        # THEN: Le fichier est créé avec le bon contenu
        assert output_file.exists()

        # Vérification du contenu JSON
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "simulation" in data
        assert "rebonds" in data
        assert data["simulation"]["fps"] == 60
        assert len(data["rebonds"]) == 1
        assert data["rebonds"][0]["index"] == test_event.index

    def test_integration_with_balle(self, tmp_path):
        """Test d'intégration avec la classe Balle."""
        # GIVEN: Une instance de Balle et un logger
        output_file = tmp_path / "integration_test.json"
        logger = SimulationLogger(output_file=str(output_file))
        logger.set_fps(60)

        # Création d'un événement de rebond simulé
        test_event = RebondEvent(index=0, time_sec=2.5, vitesse=8.2, position=(150.0, 250.0))

        # Création d'une balle et ajout de l'événement
        balle = Balle(x=150, y=250, rayon=10, couleur_centre=(255, 0, 0), couleur_contour=(200, 0, 0))
        balle.rebond_events.append(test_event)

        # WHEN: On enregistre l'événement et on écrit dans le fichier
        logger.log_rebound(test_event)
        logger.flush()

        # THEN: Vérification du contenu du fichier
        assert output_file.exists()

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["simulation"]["fps"] == 60
        assert len(data["rebonds"]) == 1
        assert data["rebonds"][0]["index"] == test_event.index
        assert data["rebonds"][0]["time_sec"] == test_event.time_sec
        assert data["rebonds"][0]["vitesse"] == test_event.vitesse
        assert data["rebonds"][0]["position"] == list(test_event.position)

    def test_multiple_rebounds(self, tmp_path):
        """Teste l'enregistrement de plusieurs rebonds."""
        # GIVEN: Un logger avec un fichier de sortie temporaire
        output_file = tmp_path / "multiple_rebounds.json"
        logger = SimulationLogger(output_file=str(output_file))
        logger.set_fps(60)

        # Création de plusieurs événements de rebond
        events = [
            RebondEvent(index=i, time_sec=i * 0.5, vitesse=5.0 + i, position=(100 + i * 10, 200 + i * 5))
            for i in range(5)
        ]

        # WHEN: On enregistre les événements et on écrit dans le fichier
        for event in events:
            logger.log_rebound(event)
        logger.flush()

        # THEN: Vérification du contenu du fichier
        assert output_file.exists()

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data["rebonds"]) == len(events)
        for i, event in enumerate(events):
            assert data["rebonds"][i]["index"] == event.index
            assert data["rebonds"][i]["time_sec"] == event.time_sec
            assert data["rebonds"][i]["vitesse"] == event.vitesse
            assert data["rebonds"][i]["position"] == list(event.position)

    def test_flush_without_events(self, tmp_path):
        """Teste que flush() fonctionne même sans événements."""
        # GIVEN: Un logger sans événements
        output_file = tmp_path / "empty_events.json"
        logger = SimulationLogger(output_file=str(output_file))
        logger.set_fps(60)

        # WHEN: On écrit dans le fichier sans avoir ajouté d'événements
        logger.flush()

        # THEN: Le fichier est créé avec une liste d'événements vide
        assert output_file.exists()

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["simulation"]["fps"] == 60
        assert data["rebonds"] == []


if __name__ == "__main__":
    pytest.main(["-v", "tests/test_simulation_logger.py"])
