import math
import random
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
        self.en_contact = False  # État de contact avec le cercle

        # Paramètres de réinjection d'énergie
        self.vitesse_min = 3  # Seuil en dessous duquel on réinjecte de l'énergie
        self.vitesse_random_min = 3  # Vitesse minimale après réinjection
        self.vitesse_random_max = 6  # Vitesse maximale après réinjection

        # Historique des positions
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
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            self.en_contact = False
            return  # éviter la division par zéro

        # Rayon de contact
        rayon_contact = cercle.rayon - self.rayon

        # Détection de collision (sans forcément rebondir)
        collision = distance >= rayon_contact

        # Nouvel impact = collision détectée alors qu'on n'était pas en contact avant
        nouvel_impact = collision and not self.en_contact

        # Mise à jour de l'état de contact pour la prochaine frame
        self.en_contact = collision

        # Si c'est un nouvel impact, on applique la physique du rebond
        if nouvel_impact:
            # Normal au point d'impact
            nx = dx / distance
            ny = dy / distance

            # Correction de position pour éviter la pénétration
            penetration = distance - rayon_contact
            self.x -= nx * penetration
            self.y -= ny * penetration

            # Calcul de la vitesse actuelle avant rebond
            vitesse_avant_rebond = math.sqrt(self.vx**2 + self.vy**2)

            # Produit scalaire (V . n)
            dot = self.vx * nx + self.vy * ny

            # Réflexion du vecteur vitesse
            self.vx = self.vx - 2 * dot * nx
            self.vy = self.vy - 2 * dot * ny

            # Légère perte d'énergie pour stabilité
            self.vx *= 0.98
            self.vy *= 0.98

            # Vérification de la vitesse après rebond
            vitesse_apres_rebond = math.sqrt(self.vx**2 + self.vy**2)

            # Si la vitesse est en dessous du seuil, on réinjecte de l'énergie
            if vitesse_apres_rebond < self.vitesse_min:
                # On conserve la direction actuelle
                if vitesse_apres_rebond > 0:  # Éviter la division par zéro
                    direction_x = self.vx / vitesse_apres_rebond
                    direction_y = self.vy / vitesse_apres_rebond
                else:
                    # Si la vitesse est nulle (cas extrême), on utilise la normale
                    direction_x = -nx
                    direction_y = -ny
                    # Normalisation
                    norm = math.sqrt(direction_x**2 + direction_y**2)
                    if norm > 0:
                        direction_x /= norm
                        direction_y /= norm

                # Nouvelle vitesse aléatoire
                nouvelle_vitesse = random.uniform(self.vitesse_random_min, self.vitesse_random_max)
                self.vx = direction_x * nouvelle_vitesse
                self.vy = direction_y * nouvelle_vitesse
