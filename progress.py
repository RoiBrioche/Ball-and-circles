"""Module pour gérer l'affichage de la progression."""
import sys

def update_progress(current_frame, total_frames):
    """
    Affiche la progression de la génération de la vidéo.
    
    Args:
        current_frame (int): Numéro de la frame actuelle
        total_frames (int): Nombre total de frames à générer
    """

    progress = (current_frame / total_frames) * 100 if total_frames > 0 else 0
    sys.stdout.write(f"\rGenerating video: {current_frame}/{total_frames} frames ({progress:.1f}%)")
    sys.stdout.flush()
