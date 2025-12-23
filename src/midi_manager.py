"""
MIDI Manager Module

This module provides functionality to load MIDI files and extract notes in a sequential manner.
It's designed to be used as a standalone component without any sound generation.
"""

import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Import pretty_midi with a clear error message if not available
PRETTY_MIDI_AVAILABLE = False
pretty_midi = None

try:
    import pretty_midi

    PRETTY_MIDI_AVAILABLE = True
except ImportError:
    pass


@dataclass
class MidiNote:
    """Represents a single MIDI note with its properties."""

    pitch: int
    duration: float
    velocity: int = 64
    start_time: float = 0.0


class MidiManager:
    """
    A class to manage MIDI file loading and note sequence extraction.

    This class provides functionality to load MIDI files, extract notes,
    and provide them sequentially.
    """

    def __init__(self, midi_file_path: str, loop: bool = False):
        """
        Initialize the MidiManager with a MIDI file.

        Args:
            midi_file_path: Path to the MIDI file to load.
            loop: If True, the sequence will loop when reaching the end.

        Raises:
            ImportError: If pretty_midi is not installed.
            FileNotFoundError: If the MIDI file doesn't exist.
            Exception: If there's an error loading the MIDI file.
        """
        if not PRETTY_MIDI_AVAILABLE:
            raise ImportError("pretty_midi is required for MIDI support. " "Install it with: pip install pretty_midi")

        if not os.path.exists(midi_file_path):
            raise FileNotFoundError(f"MIDI file not found: {midi_file_path}")

        self.midi_file_path = midi_file_path
        self.loop = loop
        self.notes: List[MidiNote] = []
        self.current_note_index = 0

        try:
            self.midi_data = pretty_midi.PrettyMIDI(midi_file_path)
            self._extract_notes()
        except Exception as e:
            raise Exception(f"Error loading MIDI file {midi_file_path}: {str(e)}")

    def _extract_notes(self) -> None:
        """Extract notes from the loaded MIDI file and store them in order."""
        self.notes = []

        # Process each instrument in the MIDI file
        for instrument in self.midi_data.instruments:
            for note in instrument.notes:
                self.notes.append(
                    MidiNote(
                        pitch=note.pitch, duration=note.end - note.start, velocity=note.velocity, start_time=note.start
                    )
                )

        # Sort notes by their start time
        self.notes.sort(key=lambda x: x.start_time)

    def get_next_note(self) -> Optional[MidiNote]:
        """
        Get the next note in the sequence.

        Returns:
            The next MidiNote in the sequence, or None if the end is reached.
            If loop is True, it will start from the beginning when reaching the end.
        """
        if not self.notes:
            return None

        if self.current_note_index >= len(self.notes):
            if self.loop:
                self.current_note_index = 0
            else:
                return None

        note = self.notes[self.current_note_index]
        self.current_note_index += 1
        return note

    def reset(self) -> None:
        """Reset the note sequence to the beginning."""
        self.current_note_index = 0

    def get_total_duration(self) -> float:
        """
        Get the total duration of the MIDI sequence in seconds.

        Returns:
            Total duration in seconds.
        """
        if not self.notes:
            return 0.0
        return max(note.start_time + note.duration for note in self.notes)

    def get_note_count(self) -> int:
        """
        Get the total number of notes in the sequence.

        Returns:
            Number of notes.
        """
        return len(self.notes)
