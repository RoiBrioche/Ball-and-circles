import pygame

# --- Classe Balle ---
class Balle:
    def __init__(self, x, y, rayon, couleur_centre, couleur_contour, vitesse=(0, 0)):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur_centre = couleur_centre
        self.couleur_contour = couleur_contour
        self.vx, self.vy = vitesse  # vitesse en x et y

    def draw(self, surface):
        """Dessine la balle à l'écran."""
        # contour
        pygame.draw.circle(surface, self.couleur_contour, (int(self.x), int(self.y)), self.rayon + 1)
        # centre
        pygame.draw.circle(surface, self.couleur_centre, (int(self.x), int(self.y)), self.rayon)

    def update(self):
        """Met à jour la position et applique la gravité simplifiée."""
        # Gravité simplifiée
        self.vy -= 0.3  # retire 0.3 à chaque frame

        # Mise à jour de la position
        self.x += self.vx
        self.y += self.vy