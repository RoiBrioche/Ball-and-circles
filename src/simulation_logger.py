import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from src.balle import RebondEvent


class SimulationLogger:
    def __init__(self, output_file: str = "rebonds_log.json"):
        """
        Initialise le logger de simulation.

        Args:
            output_file: Chemin vers le fichier de sortie JSON
        """
        self.output_file = output_file
        self.start_time = datetime.now().isoformat()
        self.fps: Optional[int] = None
        self.rebounds: List[Dict[str, Any]] = []

    def set_fps(self, fps: int) -> None:
        """Définit le FPS de la simulation"""
        self.fps = fps

    def log_rebound(self, event: RebondEvent) -> None:
        """
        Enregistre un événement de rebond.

        Args:
            event: L'événement de rebond à enregistrer
        """
        if not isinstance(event, RebondEvent):
            raise ValueError("L'événement doit être une instance de RebondEvent")

        self.rebounds.append(
            {
                "index": event.index,
                "time_sec": event.time_sec,
                "vitesse": event.vitesse,
                "position": list(event.position),  # Convertit le tuple en liste pour la sérialisation
            }
        )

    def flush(self) -> None:
        """Écrit les logs dans le fichier de sortie au format JSON"""
        log_data = {"simulation": {"fps": self.fps, "start_time": self.start_time}, "rebonds": self.rebounds}

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
