import imageio
import pygame
import sys
import os

from balle import Balle
from cercle import Cercle
from datetime import datetime


FPS = 65
DURATION_SECONDS = 61 
TOTAL_FRAMES = DURATION_SECONDS*FPS

# --- Paramètres de la fenêtre ---
LARGEUR = 1080
HAUTEUR = 1920
TITRE = "bounce_and_panic"
COULEUR_FOND = (0,0,0)  # gris foncé

# MODE = "video"  → génère uniquement le MP4, aucune fenêtre visible
# MODE = "play"   → affiche la fenêtre + génère le MP4
MODE = "video"     # CHANGE ICI selon ton besoin


# -------------------------------------
# CRÉATION D’UN NOM DE VIDÉO AVEC DATE/HEURE
# -------------------------------------
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_FOLDER = "videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

output_path = os.path.join(OUTPUT_FOLDER, f"simulation_{now}.mp4")


# -------------------------------------
# INITIALISATION PYGAME
# -------------------------------------
if MODE == "play":
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption(TITRE)
else:
    # mode "video only" → fenêtre cachée
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))


# Position et taille de la balle
x, y = LARGEUR // 2, HAUTEUR // 2
rayon_exterieur = 21  # contour blanc
rayon_interieur = 20 # centre rouge

# Boucle principale du jeu

"""------------------------------------------------------------------------------------------"""
clock = pygame.time.Clock()


# -------------------------------------
# OBJETS
# -------------------------------------
balle = Balle(
    x=LARGEUR // 2,
    y=HAUTEUR // 2 - 100,
    rayon=20,
    couleur_centre=(255, 0, 0),
    couleur_contour=(255, 255, 255),
)

cercle = Cercle(LARGEUR // 2, HAUTEUR // 2, 300, (255, 255, 255), 3)

# -------------------------------------
# WRITER MP4
# -------------------------------------
if MODE == "video" :
    writer = imageio.get_writer(output_path, fps=FPS)

total_frames = FPS * DURATION_SECONDS

# -------------------------------------
# BOUCLE PRINCIPALE
# -------------------------------------
running = True
frame_counter = 0

while running and frame_counter < total_frames:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif MODE == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

        # --- Enregistrement vidéo ---
    if MODE == "video":
        frame = pygame.surfarray.array3d(fenetre)
        frame = frame.swapaxes(0, 1)
        writer.append_data(frame)

    # --- Limite à 60 FPS ---
    clock.tick(FPS)
    frame_counter += 1
    print(".")
    # print(f"Frame {frame_counter}/{total_frames}", end="\r")

"""------------------------------------------------------------------------------------------"""

# -------------------------------------
# FIN
# -------------------------------------
if MODE == "video":
    writer.close()
    
# Quitter proprement
pygame.quit()
sys.exit()

print(f"Vidéo générée : {output_path}")