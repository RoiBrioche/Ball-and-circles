import imageio
import os
import pygame
import sys

from abc import ABC
from datetime import datetime
from typing import Optional, Type

from src.audio_engine import AudioEngine
from src.balle import Balle
from src.cercle import Cercle
from src.progress import update_progress
from src.simulation_logger import SimulationLogger


# Constantes
FPS = 65
DURATION_SECONDS = 61
TOTAL_FRAMES = DURATION_SECONDS * FPS

# Paramètres de la fenêtre
LARGEUR = 1088
HAUTEUR = 1920
TITRE = "bounce_and_panic"
COULEUR_FOND = (0, 0, 0)  # gris foncé


def init_pygame(mode="play"):
    """Initialise Pygame et retourne la fenêtre et l'horloge."""
    print(f"Initialisation de Pygame en mode: {mode}")
    if mode == "video":
        print("Configuration du mode vidéo (dummy)")
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        try:
            pygame.display.init()
            surface = pygame.Surface((LARGEUR, HAUTEUR))
            return surface, pygame.time.Clock()
        except Exception as e:
            print(f"Erreur lors de l'initialisation du mode vidéo: {e}")
            raise
    else:
        try:
            pygame.init()
            fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
            pygame.display.set_caption(TITRE)
            return fenetre, pygame.time.Clock()
        except Exception as e:
            print(f"Erreur lors de l'initialisation du mode jeu: {e}")
            raise


def create_output_path():
    """Crée le chemin de sortie pour la vidéo."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = "videos"
    os.makedirs(output_folder, exist_ok=True)
    return os.path.join(output_folder, f"simulation_{now}.mp4")


def run_game(mode="play", duration_seconds=DURATION_SECONDS, audio_engine: Optional[AudioEngine] = None):
    """Fonction principale du jeu.

    Args:
        mode: Mode d'exécution ('play' ou 'video')
        duration_seconds: Durée de la simulation en secondes
        audio_engine: Moteur audio optionnel pour gérer les sons de rebond
    """
    print(f"\nDémarrage du jeu en mode: {mode} ({duration_seconds} secondes)")

    # Initialisation du moteur audio si fourni
    if audio_engine is not None:
        print("Moteur audio détecté - activation des sons de rebond")

    fenetre, clock = init_pygame(mode)
    output_path = create_output_path()
    print(f"Chemin de sortie de la vidéo: {output_path}")

    # Création des objets
    balle = Balle(LARGEUR // 2, HAUTEUR // 2 - 100, 20, (255, 0, 0), (255, 255, 255))
    cercle = Cercle(LARGEUR // 2, HAUTEUR // 2, 300, (255, 255, 255), 3)

    # Initialisation du logger de simulation
    logger = SimulationLogger("rebonds_log.json")
    logger.set_fps(FPS)

    writer = None
    if mode == "video":
        writer = imageio.get_writer(output_path, fps=FPS)

    total_frames = FPS * duration_seconds
    frame_counter = 0
    running = True

    while running and frame_counter < total_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif mode == "play" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Mise à jour
        balle.update()

        # Gestion des rebonds et enregistrement des événements
        rebond_event = balle.rebond_sur_cercle(cercle, frame_counter=frame_counter, FPS=FPS)
        if rebond_event is not None:
            logger.log_rebound(rebond_event)

            # Notification du rebond au moteur audio si disponible
            if audio_engine is not None:
                try:
                    audio_engine.on_rebond(rebond_event["time_sec"])
                except Exception as e:
                    print(f"Erreur lors de la notification audio du rebond: {e}")

        # Rendu
        fenetre.fill(COULEUR_FOND)
        cercle.draw(fenetre)
        balle.draw(fenetre)
        if mode == "play":
            pygame.display.flip()

        # Capture des frames pour la vidéo
        if mode == "video":
            if writer is None:
                raise RuntimeError("Writer should be initialized in video mode")
            try:
                frame = pygame.surfarray.array3d(fenetre).copy()
                frame = frame.transpose(1, 0, 2)
                writer.append_data(frame)
                update_progress(frame_counter, total_frames)
            except Exception as e:
                print(f"Erreur capture frame {frame_counter}: {e}")

        if mode == "play":
            clock.tick(FPS)
        frame_counter += 1
        update_progress(frame_counter, total_frames)

    # Nettoyage
    if writer is not None:
        writer.close()

    # Finalisation du moteur audio si disponible
    if audio_engine is not None:
        try:
            audio_engine.finalize()
        except Exception as e:
            print(f"Erreur lors de la finalisation du moteur audio: {e}")

    # Sauvegarde des logs de simulation
    try:
        logger.flush()
        print(f"\nLogs de simulation sauvegardés dans : rebonds_log.json")
    except Exception as e:
        print(f"\nErreur lors de la sauvegarde des logs : {e}")

    pygame.quit()

    if mode == "video":
        print(f"\nVidéo générée avec succès : {output_path}")


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(description="Simulation de rebonds de balle")
    parser.add_argument(
        "--mode",
        type=str,
        default="play",
        choices=["play", "video"],
        help="Mode d'exécution: 'play' pour l'affichage temps réel, 'video' pour générer une vidéo",
    )
    parser.add_argument("--duration", type=int, default=DURATION_SECONDS, help="Durée de la simulation en secondes")
    parser.add_argument("--test", action="store_true", help="Mode test (durée réduite à 5 secondes)")
    parser.add_argument("--no-audio", action="store_true", help="Désactive la sortie audio")
    return parser.parse_args()


def main():
    args = parse_arguments()
    duration = 5 if args.test else args.duration

    # Initialisation du moteur audio (None pour l'instant, sera implémenté plus tard)
    audio_engine = None
    no_audio = getattr(args, "no_audio", False)

    try:
        run_game(mode=args.mode, duration_seconds=duration, audio_engine=audio_engine if not no_audio else None)
    except KeyboardInterrupt:
        print("\nArrêt du programme par l'utilisateur")
    except Exception as e:
        print(f"\nErreur lors de l'exécution: {e}")
        raise
    finally:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
