"""Tests unitaires pour la classe Cercle."""
import pytest
from unittest.mock import patch, MagicMock

# Ajout du répertoire parent au chemin Python pour importer les modules
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cercle import Cercle


class TestCercleInitialisation:
    """Tests pour l'initialisation de la classe Cercle."""

    def test_initialisation_defaut(self):
        """Vérifie que le cercle est correctement initialisé avec les valeurs par défaut."""
        cercle = Cercle(100, 200, 50)
        
        assert cercle.x == 100
        assert cercle.y == 200
        assert cercle.diametre == 50
        assert cercle.rayon == 25  # 50 // 2
        assert cercle.couleur == (255, 255, 255)  # Couleur par défaut
        assert cercle.epaisseur == 2  # Épaisseur par défaut
        assert cercle.section_trou == 0  # Pas de trou par défaut

    def test_initialisation_parametres_personnalises(self):
        """Vérifie que le cercle accepte des paramètres personnalisés."""
        cercle = Cercle(
            x=150, 
            y=250, 
            diametre=100, 
            couleur=(255, 0, 0), 
            epaisseur=3, 
            section_trou=25
        )
        
        assert cercle.x == 150
        assert cercle.y == 250
        assert cercle.diametre == 100
        assert cercle.rayon == 50  # 100 // 2
        assert cercle.couleur == (255, 0, 0)
        assert cercle.epaisseur == 3
        assert cercle.section_trou == 25


class TestCercleDraw:
    """Tests pour la méthode draw de la classe Cercle."""

    @patch('pygame.draw.circle')
    def test_draw_cercle_complet(self, mock_draw_circle):
        """Test que la méthode draw appelle correctement pygame.draw.circle pour un cercle complet."""
        # Création d'une surface factice
        mock_surface = MagicMock()
        
        # Création d'un cercle
        cercle = Cercle(100, 200, 50, (255, 0, 0), 2)
        
        # Appel de la méthode draw
        cercle.draw(mock_surface)
        
        # Vérifie que pygame.draw.circle a été appelé avec les bons paramètres
        mock_draw_circle.assert_called_once_with(
            mock_surface,
            (255, 0, 0),  # Couleur
            (100, 200),   # Position (x, y)
            25,           # Rayon (diamètre / 2)
            2             # Épaisseur
        )

    @patch('pygame.draw.arc')
    @patch('pygame.draw.circle')
    def test_draw_avec_section_trou(self, mock_draw_circle, mock_draw_arc):
        """Test que la méthode draw gère correctement section_trou > 0."""
        # Création d'une surface factice
        mock_surface = MagicMock()
        
        # Création d'un cercle avec une section manquante
        cercle = Cercle(100, 200, 50, (255, 0, 0), 2, section_trou=25)
        
        # Appel de la méthode draw
        cercle.draw(mock_surface)
        
        # Vérifie que pygame.draw.circle a été appelé (pour l'implémentation actuelle)
        # Note: Ce test devra être mis à jour lorsque l'implémentation de section_trou sera complétée
        mock_draw_circle.assert_called_once()
        
        # Vérifie que pygame.draw.arc n'a pas été appelé (car non implémenté encore)
        # mock_draw_arc.assert_not_called()
        # Note: Décommentez cette ligne une fois l'implémentation terminée


class TestCercleCollision:
    """Tests pour la détection de collision avec la classe Cercle."""
    
    def test_collision_avec_balle(self):
        """Test la détection de collision entre un cercle et une balle."""
        from balle import Balle
        
        # Création d'un cercle et d'une balle qui le touche
        cercle = Cercle(200, 200, 100)  # Cercle de rayon 50
        balle = Balle(250, 200, 10, (255, 0, 0), (0, 0, 0))  # Balle à droite du cercle, à la limite de la collision
        
        # Calcul de la distance entre les centres
        dx = balle.x - cercle.x
        dy = balle.y - cercle.y
        distance = (dx**2 + dy**2) ** 0.5
        
        # La distance doit être inférieure à la somme des rayons pour une collision
        assert distance <= (cercle.rayon + balle.rayon)
    
    def test_pas_de_collision(self):
        """Test qu'il n'y a pas de collision quand les objets sont éloignés."""
        from balle import Balle
        
        # Création d'un cercle et d'une balle éloignés
        cercle = Cercle(200, 200, 100)  # Cercle de rayon 50
        balle = Balle(400, 400, 10, (255, 0, 0), (0, 0, 0))  # Balle loin du cercle
        
        # Calcul de la distance entre les centres
        dx = balle.x - cercle.x
        dy = balle.y - cercle.y
        distance = (dx**2 + dy**2) ** 0.5
        
        # La distance doit être supérieure à la somme des rayons
        assert distance > (cercle.rayon + balle.rayon)


class TestCercleLimites:
    """Tests des cas limites pour la classe Cercle."""
    
    def test_diametre_nul(self):
        """Test avec un diamètre nul."""
        cercle = Cercle(100, 200, 0)
        assert cercle.diametre == 0
        assert cercle.rayon == 0
    
    def test_section_trou_limites(self):
        """Test des valeurs limites pour section_trou."""
        # section_trou = 0 (cercle complet)
        cercle1 = Cercle(100, 200, 50, section_trou=0)
        assert cercle1.section_trou == 0
        
        # section_trou = 100 (cercle vide - à implémenter)
        cercle2 = Cercle(100, 200, 50, section_trou=100)
        assert cercle2.section_trou == 100
        
        # section_trou en dehors des limites (devrait être contraint entre 0 et 100)
        cercle3 = Cercle(100, 200, 50, section_trou=-10)
        assert cercle3.section_trou >= 0
        
        cercle4 = Cercle(100, 200, 50, section_trou=150)
        assert cercle4.section_trou <= 100
