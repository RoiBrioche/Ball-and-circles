"""Tests unitaires pour la classe Balle."""

import math
import pytest
from unittest.mock import patch, MagicMock

# Ajout du répertoire parent au chemin Python pour importer les modules
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from balle import Balle


class TestBalleInitialisation:
    """Tests pour l'initialisation de la classe Balle."""

    def test_initialisation_defaut(self):
        """Vérifie que la balle est correctement initialisée avec les valeurs par défaut."""
        balle = Balle(100, 200, 10, (255, 0, 0), (0, 0, 0))

        assert balle.x == 100
        assert balle.y == 200
        assert balle.rayon == 10
        assert balle.couleur_centre == (255, 0, 0)
        assert balle.couleur_contour == (0, 0, 0)
        assert balle.vx == 5  # Valeur par défaut
        assert balle.vy == 0  # Valeur par défaut
        assert balle.vitesse_min == 3
        assert balle.max_positions == 80

    def test_initialisation_vitesse_personnalisee(self):
        """Vérifie que la balle accepte une vitesse personnalisée."""
        balle = Balle(100, 200, 10, (255, 0, 0), (0, 0, 0), vitesse=(10, -5))

        assert balle.vx == 10
        assert balle.vy == -5


class TestBalleUpdate:
    """Tests pour la méthode update de la classe Balle."""

    def test_update_application_gravite(self):
        """Vérifie que la gravité est correctement appliquée."""
        balle = Balle(100, 200, 10, (255, 0, 0), (0, 0, 0), vitesse=(5, 0))

        # Avant update
        vy_avant = balle.vy

        # Après update
        balle.update()

        # La vitesse verticale devrait avoir augmenté à cause de la gravité
        assert balle.vy > vy_avant
        assert abs(balle.vy - 0.3) < 0.001  # 0.3 est la valeur de la gravité

    def test_update_position(self):
        """Vérifie que la position est correctement mise à jour."""
        balle = Balle(100, 200, 10, (255, 0, 0), (0, 0, 0), vitesse=(2, 3))

        x_avant, y_avant = balle.x, balle.y

        balle.update()

        assert balle.x == x_avant + 2  # x += vx
        assert balle.y == y_avant + 3 + 0.3  # y += vy + gravité

    def test_historique_positions(self):
        """Vérifie que l'historique des positions est correctement géré."""
        balle = Balle(100, 200, 10, (255, 0, 0), (0, 0, 0))

        # Ajout d'une position
        balle.update()
        assert len(balle.positions) == 1

        # Ajout de plus de positions que le maximum autorisé
        for _ in range(balle.max_positions + 10):
            balle.update()

        # Vérifie que le nombre de positions ne dépasse pas max_positions
        assert len(balle.positions) == balle.max_positions


class TestBalleRebondCercle:
    """Tests pour la méthode rebond_sur_cercle de la classe Balle."""

    def test_collision_frontale(self):
        """Test une collision frontale avec un cercle."""
        from cercle import Cercle

        # Création d'une balle se déplaçant vers la droite
        balle = Balle(100, 201, 10, (255, 0, 0), (0, 0, 0), vitesse=(10, 0))
        cercle = Cercle(200, 200, 100)  # Cercle à droite de la balle

        # Avant collision
        vx_avant = balle.vx

        # Collision
        balle.rebond_sur_cercle(cercle)

        # Après collision
        assert balle.vx < 0  # La balle rebondit vers la gauche
        assert abs(balle.vx) < abs(vx_avant)  # Perte d'énergie
        # Ne pas vérifier vy car dans une collision frontale parfaite, il peut rester à 0

    def test_collision_tangentielle(self):
        """Test une collision tangentielle avec un cercle."""
        from cercle import Cercle

        # Balle se déplaçant horizontalement, juste au-dessus du cercle
        balle = Balle(100, 100, 10, (255, 0, 0), (0, 0, 0), vitesse=(10, 0))
        cercle = Cercle(200, 200, 100)  # Cercle en dessous

        # Avant collision
        vx_avant, vy_avant = balle.vx, balle.vy

        # Collision
        balle.rebond_sur_cercle(cercle)

        # Après collision, la vitesse devrait avoir changé de direction
        assert balle.vx != vx_avant or balle.vy != vy_avant

    def test_reinjection_energie_vitesse_basse(self):
        """Vérifie la réinjection d'énergie quand la vitesse est trop basse."""
        from cercle import Cercle

        # Balle avec une vitesse très basse
        balle = Balle(100, 100, 10, (255, 0, 0), (0, 0, 0), vitesse=(0.1, 0.1))
        cercle = Cercle(200, 200, 100)

        # Avant collision
        vitesse_avant = math.sqrt(balle.vx**2 + balle.vy**2)

        # Collision
        balle.rebond_sur_cercle(cercle)

        # Après collision, la vitesse devrait être dans l'intervalle [vitesse_random_min, vitesse_random_max]
        vitesse_apres = math.sqrt(balle.vx**2 + balle.vy**2)
        assert balle.vitesse_random_min <= vitesse_apres <= balle.vitesse_random_max

    def test_collision_vitesse_nulle(self):
        """Test le comportement avec une vitesse nulle."""
        from cercle import Cercle

        # Balle sans vitesse initiale
        balle = Balle(100, 100, 10, (255, 0, 0), (0, 0, 0), vitesse=(0, 0))
        cercle = Cercle(200, 200, 100)

        # La collision avec vitesse nulle devrait quand même fonctionner
        try:
            balle.rebond_sur_cercle(cercle)
            # Si on arrive ici, c'est que la méthode n'a pas levé d'exception
            # Vérifions que la vitesse a été réinitialisée
            vitesse_apres = math.sqrt(balle.vx**2 + balle.vy**2)
            assert balle.vitesse_random_min <= vitesse_apres <= balle.vitesse_random_max
        except Exception as e:
            pytest.fail(f"La méthode a échoué avec une vitesse nulle: {e}")


class TestBalleDraw:
    """Tests pour la méthode draw de la classe Balle."""

    @patch("pygame.draw.circle")
    @patch("pygame.Surface")
    def test_draw(self, mock_surface, mock_draw_circle):
        """Test que la méthode draw appelle correctement les fonctions de dessin."""
        # Création d'une surface factice
        mock_surface_instance = MagicMock()
        mock_surface.return_value = mock_surface_instance

        # Création d'une balle
        balle = Balle(100, 200, 15, (255, 0, 0), (0, 0, 255))

        # Appel de la méthode draw
        balle.draw(mock_surface_instance)

        # Vérifie que pygame.draw.circle a été appelé pour le contour
        mock_draw_circle.assert_any_call(
            mock_surface_instance, (0, 0, 255), (100, 200), 16  # Couleur du contour  # Position  # Rayon + 1
        )

        # Vérifie que pygame.draw.circle a été appelé pour le centre
        mock_draw_circle.assert_any_call(
            mock_surface_instance, (255, 0, 0), (100, 200), 15  # Couleur du centre  # Position  # Rayon
        )

    @patch("pygame.draw.line")
    @patch("pygame.draw.circle")
    @patch("pygame.Surface")
    def test_draw_avec_trainee(self, mock_surface, mock_draw_circle, mock_draw_line):
        """Test que la traînée est correctement dessinée."""
        # Configuration des mocks
        mock_surface_instance = MagicMock()
        mock_surface.return_value = mock_surface_instance

        # Création d'une balle avec quelques positions dans l'historique
        balle = Balle(100, 200, 10, (255, 0, 0), (0, 0, 255))

        # Ajout de positions à l'historique
        balle.positions = [(90, 190), (95, 195), (100, 200)]

        # Appel de la méthode draw
        balle.draw(mock_surface_instance)

        # Vérifie que pygame.draw.line a été appelé pour la traînée
        assert mock_draw_line.called
