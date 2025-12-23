"""Unit tests for the midi_manager module."""

import os
import sys
import unittest
import tempfile
import pretty_midi

from unittest.mock import patch

# Add the src directory to the path to import the module
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from midi_manager import MidiManager, MidiNote  # noqa: E402


def create_temp_midi():
    """Create a temporary MIDI file for testing purposes."""
    tmp_file = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"))

    # Add some test notes
    notes = [
        pretty_midi.Note(velocity=100, pitch=60, start=0.0, end=0.5),
        pretty_midi.Note(velocity=100, pitch=62, start=0.5, end=1.0),
        pretty_midi.Note(velocity=100, pitch=64, start=1.0, end=1.5),
    ]

    piano.notes.extend(notes)
    midi.instruments.append(piano)

    # Save to temporary file
    midi.write(tmp_file.name)
    return tmp_file.name


class TestMidiManager(unittest.TestCase):
    """Test cases for the MidiManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary MIDI file
        self.test_midi_path = create_temp_midi()

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary MIDI file
        if os.path.exists(self.test_midi_path):
            os.remove(self.test_midi_path)

    def test_extract_notes(self):
        """Test that notes are extracted correctly from the MIDI file."""
        manager = MidiManager(self.test_midi_path)
        self.assertEqual(len(manager.notes), 3)
        self.assertEqual(manager.notes[0].pitch, 60)
        self.assertEqual(manager.notes[1].pitch, 62)
        self.assertEqual(manager.notes[2].pitch, 64)

    def test_get_next_note_sequential(self):
        """Test that get_next_note returns notes in sequence."""
        manager = MidiManager(self.test_midi_path)
        note1 = manager.get_next_note()
        note2 = manager.get_next_note()
        note3 = manager.get_next_note()
        self.assertEqual(note1.pitch, 60)
        self.assertEqual(note2.pitch, 62)
        self.assertEqual(note3.pitch, 64)

    def test_get_next_note_end_of_sequence(self):
        """Test that get_next_note returns None at the end of the sequence."""
        manager = MidiManager(self.test_midi_path, loop=False)
        for _ in range(3):
            manager.get_next_note()
        self.assertIsNone(manager.get_next_note())

    def test_get_next_note_loop(self):
        """Test that get_next_note loops when loop=True."""
        manager = MidiManager(self.test_midi_path, loop=True)
        notes = [manager.get_next_note() for _ in range(4)]
        self.assertEqual(notes[0].pitch, 60)
        self.assertEqual(notes[3].pitch, 60)

    def test_reset(self):
        """Test that reset restarts the sequence."""
        manager = MidiManager(self.test_midi_path)
        note1 = manager.get_next_note()
        manager.reset()
        note1_again = manager.get_next_note()
        self.assertEqual(note1.pitch, note1_again.pitch)

    def test_get_total_duration(self):
        """Test that get_total_duration returns the correct duration."""
        manager = MidiManager(self.test_midi_path)
        self.assertAlmostEqual(manager.get_total_duration(), 1.5)

    def test_get_note_count(self):
        """Test that get_note_count returns the correct number of notes."""
        manager = MidiManager(self.test_midi_path)
        self.assertEqual(manager.get_note_count(), 3)

    def test_init_raises_file_not_found(self):
        """Test that FileNotFoundError is raised if MIDI file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            MidiManager("nonexistent.mid")


class TestMidiNote(unittest.TestCase):
    """Test cases for the MidiNote dataclass."""

    def test_midi_note_creation(self):
        note = MidiNote(pitch=60, duration=1.0)
        self.assertEqual(note.pitch, 60)
        self.assertEqual(note.duration, 1.0)
        self.assertEqual(note.velocity, 64)
        note = MidiNote(pitch=72, duration=0.5, velocity=100, start_time=1.0)
        self.assertEqual(note.pitch, 72)
        self.assertEqual(note.duration, 0.5)
        self.assertEqual(note.velocity, 100)
        self.assertEqual(note.start_time, 1.0)


if __name__ == "__main__":
    unittest.main()
