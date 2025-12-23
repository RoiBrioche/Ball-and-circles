from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class AudioEngine(Protocol):
    """
    Interface abstraite pour la gestion audio du simulateur.

    Cette interface définit le contrat que doivent implémenter tous les moteurs audio,
    qu'ils soient en temps réel ou en mode rendu offline.

    Les implémentations concrètes (comme RealtimeAudioEngine ou OfflineAudioEngine)
    devront fournir une implémentation spécifique de ces méthodes.
    """

    @abstractmethod
    def on_rebond(self, time_sec: float) -> None:
        """
        Méthode appelée à chaque rebond de la balle.

        Args:
            time_sec: Temps en secondes depuis le début de la simulation
                     où le rebond s'est produit.
        """
        ...

    @abstractmethod
    def finalize(self) -> None:
        """
        Méthode appelée à la fin de la simulation ou du rendu.

        Permet de libérer les ressources et de finaliser le rendu audio.
        """
        ...


# Classes d'implémentation futures (déclarées ici pour référence)
# class RealtimeAudioEngine(AudioEngine):
#     """Implémentation pour la lecture audio en temps réel."""
#     pass
#
#
# class OfflineAudioEngine(AudioEngine):
#     """Implémentation pour le rendu audio en mode offline (vidéo)."""
#     pass
