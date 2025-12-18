import imageio
import pygame
import sys
import os
from progress import update_progress
from balle import Balle
from cercle import Cercle
from datetime import datetime

# Constantes
FPS = 65
DURATION_SECONDS = 61
TOTAL_FRAMES = DURATION_SECONDS * FPS

# Paramètres de la fenêtre
LARGEUR = 1088  # 1088 est le multiple de 16 le plus proche de 1080
HAUTEUR = 1920
TITRE = "bounce_and_panic"
COULEUR_FOND = (0, 0, 0)  # gris foncé

def init_pygame(mode="play"):
    """Initialise Pygame et retourne la fenêtre et l'horloge."""
    if mode == "video":
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    
    pygame.init()
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption(TITRE)
    clock = pygame.time.Clock()
    
    return fenetre, clock

def create_output_path():
    """Crée le chemin de sortie pour la vidéo."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = "videos"
    os.makedirs(output_folder, exist_ok=True)
    return os.path.join(output_folder, f"simulation_{now}.mp4")

def run_game(mode="play", duration_seconds=DURATION_SECONDS):
    """Fonction principale du jeu.
    
    Args:
        mode: "play" pour afficher la fenêtre, "video" pour générer uniquement la vidéo
        duration_seconds: durée de la simulation en secondes
    """
    # Initialisation
    fenetre, clock = init_pygame(mode)
    output_path = create_output_path()
    
    # Création des objets
    balle = Balle(
        x=LARGEUR // 2,
        y=HAUTEUR // 2 - 100,
        rayon=20,
        couleur_centre=(255, 0, 0),
        couleur_contour=(255, 255, 255),
    )
    cercle = Cercle(LARGEUR // 2, HAUTEUR // 2, 300, (255, 255, 255), 3)
    
    # Initialisation de l'enregistrement vidéo si nécessaire
    writer = None
    if mode == "video":
        writer = imageio.get_writer(output_path, fps=FPS)
    
    # Boucle principale
    total_frames = FPS * duration_seconds
    frame_counter = 0
    running = True
    
    while running and frame_counter < total_frames:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif mode == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # Mise à jour de la logique du jeu
        balle.update()
        balle.rebond_sur_cercle(cercle)
        
        # Rendu
        fenetre.fill(COULEUR_FOND)
        cercle.draw(fenetre)
        balle.draw(fenetre)
        pygame.display.flip()
        
        # Capture de la frame pour la vidéo
        if mode == "video":
            frame = pygame.surfarray.array3d(fenetre)
            frame = frame.swapaxes(0, 1)
            writer.append_data(frame)
        
        # Contrôle de la vitesse de la boucle
        clock.tick(FPS)
        frame_counter += 1
        update_progress(frame_counter, total_frames)
    
    # Nettoyage
    if writer is not None:
        writer.close()
    
    pygame.quit()
    
    if mode == "video":
        print(f"\nVidéo générée avec succès : {output_path}")

def parse_arguments():
    """Parse les arguments en ligne de commande."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Simulation de rebonds de balle')
    parser.add_argument('--mode', type=str, default='play',
                      choices=['play', 'video'],
                      help='Mode d\'exécution: play (affichage) ou video (génération vidéo)')
    parser.add_argument('--duration', type=int, default=DURATION_SECONDS,
                      help='Durée de la simulation en secondes')
    parser.add_argument('--test', action='store_true',
                      help='Mode test (réduit la durée automatiquement)')
    
    return parser.parse_args()

def main():
    """Point d'entrée principal du programme."""
    args = parse_arguments()
    
    # En mode test, on réduit la durée
    if args.test:
        duration = 5  # Durée courte pour les tests
    else:
        duration = args.duration
    
    try:
        run_game(mode=args.mode, duration_seconds=duration)
    except KeyboardInterrupt:
        print("\nArrêt du programme par l'utilisateur")
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()