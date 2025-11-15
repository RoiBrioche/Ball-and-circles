import math
import pygame
# --- Classe Balle ---
class Balle:
    def __init__(self, x, y, rayon, couleur_centre, couleur_contour, vitesse=(5, 0)):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur_centre = couleur_centre
        self.couleur_contour = couleur_contour
        self.vx, self.vy = vitesse

        # --- Nouveau : historique des positions ---
        self.positions = []  # liste [(x1, y1), (x2, y2), ...]
        self.max_positions = 80  # environ 1 seconde de traînée à 80 FPS

    def draw(self, surface):

       # Surface temporaire pour gérer la transparence
        trail_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        trail_surface.fill((0, 0, 0, 0))

        if len(self.positions) > 1:
            for i in range(1, len(self.positions)):
                alpha = int(180 * (i / len(self.positions)))
                r, g, b = self.couleur_centre
                color = (int(r * 0.7), int(g * 0.7), int(b * 0.7), alpha)

                start = self.positions[i - 1]
                end = self.positions[i]
                width = int(self.rayon * (i / len(self.positions)) + 1)

                # Ligne principale
                pygame.draw.line(trail_surface, color, start, end, width)

                # Petits cercles de finition pour éviter les "trous"
                pygame.draw.circle(trail_surface, color, (int(start[0]), int(start[1])), width // 2)
                pygame.draw.circle(trail_surface, color, (int(end[0]), int(end[1])), width // 2)

        surface.blit(trail_surface, (0, 0))

        """Dessine la balle (contour + centre)."""
        pygame.draw.circle(surface, self.couleur_contour, (int(self.x), int(self.y)), self.rayon + 1)
        pygame.draw.circle(surface, self.couleur_centre, (int(self.x), int(self.y)), self.rayon)

    def update(self):
        """Ajoute la gravité et déplace la balle."""
        self.vy += 0.3  # effet gravité
        self.x += self.vx
        self.y += self.vy

        self.positions.append((self.x, self.y))

        # Garde seulement les dernières positions
        if len(self.positions) > self.max_positions:
            self.positions.pop(0)

    def rebond_sur_cercle(self, cercle):
        """Détecte et applique le rebond sur le cercle donné."""
        dx = self.x - cercle.x
        dy = self.y - cercle.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            return  # éviter la division par zéro

        # Rayon de contact
        rayon_contact = cercle.rayon - self.rayon

        # Si la balle touche ou pénètre le cercle
        if distance >= rayon_contact:
            # Normal au point d'impact
            nx = dx / distance
            ny = dy / distance

            # Correction de position pour éviter la pénétration
            penetration = distance - rayon_contact
            self.x -= nx * penetration
            self.y -= ny * penetration

            # Produit scalaire (V . n)
            dot = self.vx * nx + self.vy * ny

            # Réflexion du vecteur vitesse
            self.vx = self.vx - 2 * dot * nx
            self.vy = self.vy - 2 * dot * ny

            # Légère perte d'énergie pour stabilité
            self.vx *= 0.98
            self.vy *= 0.98