import pygame
import math


# --- Classe Cercle ---
class Cercle:
    def __init__(self, x, y, diametre, couleur=(255, 255, 255), epaisseur=2, section_trou=0):
        """
        x, y : position du centre
        diametre : diamètre du cercle
        couleur : couleur du contour (défaut = blanc)
        epaisseur : épaisseur du trait
        section_trou : pourcentage de la portion manquante (0 à 100)
        """

        self.x = x
        self.y = y
        self.diametre = diametre
        self.rayon = diametre // 2
        self.couleur = couleur
        self.epaisseur = epaisseur
        # Contrainte pour section_trou entre 0 et 100
        self.section_trou = max(0, min(100, section_trou))

    def draw(self, surface):
        """Dessine le cercle complet (ou partiel plus tard)."""
        # Pour l’instant : cercle complet
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), self.rayon, self.epaisseur)

        # TODO : si section_trou > 0, on dessinera seulement une portion (ex : arc de cercle)
        # On pourra utiliser pygame.draw.arc() avec un angle calculé à partir du pourcentage
