import pygame
import sys

from balle import Balle
from cercle import Cercle

# Initialisation de Pygame
pygame.init()

FPS = 65
MOVIE_TIME = 61
TOTAL_FRAMES = MOVIE_TIME*FPS

# --- Paramètres de la fenêtre ---
LARGEUR = 1080
HAUTEUR = 1920
TITRE = "bounce_and_panic"
COULEUR_FOND = (0,0,0)  # gris foncé


# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption(TITRE)

# Position et taille de la balle
x, y = LARGEUR // 2, HAUTEUR // 2
rayon_exterieur = 21  # contour blanc
rayon_interieur = 20 # centre rouge

# Boucle principale du jeu

"""------------------------------------------------------------------------------------------"""
clock = pygame.time.Clock()

balle = Balle(
    x=LARGEUR // 2,
    y=HAUTEUR // 2,
    rayon=20,
    couleur_centre=(255, 0, 0),
    couleur_contour=(255, 255, 255),
)

cercle = Cercle(LARGEUR // 2, HAUTEUR // 2, 300, (255, 255, 255), 3)

running = True

while running:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # --- Logique du jeu (vide pour l'instant) ---
    balle.update()
    balle.rebond_sur_cercle(cercle)

    # --- Dessin ---
    fenetre.fill(COULEUR_FOND)
    cercle.draw(fenetre)
    balle.draw(fenetre)


    # --- Rafraîchissement ---
    pygame.display.flip()

    # --- Limite à 60 FPS ---
    clock.tick(FPS)

"""------------------------------------------------------------------------------------------"""

# Quitter proprement
pygame.quit()
sys.exit()