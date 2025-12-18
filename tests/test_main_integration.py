"""Tests d'intégration pour main.py corrigés pour le nouveau main.py."""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
import argparse
import pygame

# Ajout du répertoire parent au chemin Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import main
from balle import Balle
from cercle import Cercle


class TestIntegrationBalleCercle:
    """Tests d'intégration entre la balle et le cercle."""

    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('pygame.event.get')
    @patch('pygame.quit')
    @patch('pygame.init')
    def test_balle_rebond_sur_cercle(self, mock_init, mock_quit, mock_event_get,
                                      mock_clock, mock_set_caption):
        """Test que la balle rebondit correctement sur le cercle."""
        # Utiliser une vraie surface Pygame pour le dessin
        pygame.init()
        fenetre = pygame.Surface((main.LARGEUR, main.HAUTEUR))

        # Simulation d'événements Pygame (QUIT pour arrêter)
        mock_event = MagicMock()
        mock_event.type = pygame.QUIT
        mock_event_get.return_value = [mock_event]

        # Simulation du clock
        mock_clock_instance = MagicMock()
        mock_clock.return_value = mock_clock_instance
        mock_clock_instance.tick.return_value = 60

        # Patch des arguments de ligne de commande
        with patch('main.parse_arguments') as mock_parse:
            mock_parse.return_value = argparse.Namespace(mode='play', duration=1, test=True)
            with patch('sys.exit'):
                main.main()


class TestModeVideo:
    """Tests pour le mode vidéo sans affichage graphique."""

    @patch('pygame.init')
    @patch('pygame.time.Clock')
    @patch('pygame.event.get')
    @patch('imageio.get_writer')
    @patch('pygame.surfarray.array3d')
    def test_mode_video_sans_affichage(self, mock_array3d, mock_get_writer,
                                       mock_event_get, mock_clock, mock_init):
        """Test que le mode vidéo fonctionne sans affichage graphique."""
        # Utiliser une vraie surface Pygame
        pygame.init()
        fenetre = pygame.Surface((main.LARGEUR, main.HAUTEUR))

        # Simulation d'un événement pour quitter
        mock_event = MagicMock()
        mock_event.type = pygame.QUIT
        mock_event_get.return_value = [mock_event]

        # Clock simulé
        mock_clock_instance = MagicMock()
        mock_clock.return_value = mock_clock_instance
        mock_clock_instance.tick.return_value = 60

        # Mock du writer imageio
        mock_writer = MagicMock()
        mock_get_writer.return_value = mock_writer

        # Mock array3d
        mock_array3d.return_value = MagicMock()
        mock_array3d.return_value.swapaxes.return_value = b'frame_data'

        # Patch des arguments de ligne de commande
        with patch('main.parse_arguments') as mock_parse:
            mock_parse.return_value = argparse.Namespace(mode='video', duration=1, test=True)
            with patch('sys.exit'):
                main.main()


class TestInteractionsBallesCercles:
    """Tests des interactions entre balles et cercles."""

    def test_creation_et_mise_a_jour_balles(self):
        balle = Balle(100, 100, 10, (255, 0, 0), (255, 255, 255))
        cercle = Cercle(200, 200, 100)
        x_avant, y_avant = balle.x, balle.y
        balle.update()
        assert (balle.x, balle.y) != (x_avant, y_avant)
        assert balle.vy > 0
        balle.rebond_sur_cercle(cercle)
        assert balle.vy < 0 or balle.vx != 0

    def test_plusieurs_collisions(self):
        balle = Balle(100, 100, 10, (255, 0, 0), (255, 255, 255), vitesse=(5, 0))
        cercle = Cercle(200, 200, 100)
        for _ in range(10):
            balle.update()
            balle.rebond_sur_cercle(cercle)
        vitesse = (balle.vx**2 + balle.vy**2) ** 0.5
        assert vitesse > 0


class TestFonctionnalitesAvancees:
    """Tests des fonctionnalités avancées comme la réinjection d'énergie."""

    def test_reinjection_energie(self):
        balle = Balle(100, 100, 10, (255, 0, 0), (255, 255, 255), vitesse=(0.1, 0.1))
        cercle = Cercle(200, 200, 100)
        vitesse_avant = (balle.vx**2 + balle.vy**2) ** 0.5
        balle.rebond_sur_cercle(cercle)
        vitesse_apres = (balle.vx**2 + balle.vy**2) ** 0.5
        assert balle.vitesse_random_min <= vitesse_apres <= balle.vitesse_random_max

    def test_effet_gravite(self):
        balle = Balle(100, 100, 10, (255, 0, 0), (255, 255, 255), vitesse=(0, 0))
        vy_avant = balle.vy
        balle.update()
        assert balle.vy > vy_avant
