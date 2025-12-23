# MIDI Manager Module

A Python module for loading and processing MIDI files in a simple, efficient manner. This module is designed to be used in applications that need to process MIDI note events sequentially, such as music visualizers, games, or interactive music applications.

## Features

- Load and parse MIDI files
- Extract notes with pitch, duration, velocity, and timing information
- Sequential note access with optional looping
- Lightweight and focused on performance
- No external dependencies except `pretty_midi`
- Fully tested with unit tests

## Installation

1. First, install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Install the `pretty_midi` package:

```bash
pip install pretty_midi
```

## Usage

```python
from midi_manager import MidiManager

# Create a MidiManager instance
midi_file = "path/to/your/file.mid"
midi_manager = MidiManager(midi_file, loop=True)  # loop=True to loop the sequence

# Get the next note in the sequence
note = midi_manager.get_next_note()
if note:
    print(f"Pitch: {note.pitch}, Duration: {note.duration}, Velocity: {note.velocity}")

# Reset to the beginning of the sequence
midi_manager.reset()

# Get the total number of notes
note_count = midi_manager.get_note_count()

# Get the total duration of the MIDI sequence
total_duration = midi_manager.get_total_duration()
```

## Example

See the [examples/midi_example.py](examples/midi_example.py) file for a complete example of how to use the MidiManager class.

## API Reference

### MidiManager

#### `__init__(self, midi_file_path: str, loop: bool = False)`
Initialize the MidiManager with a MIDI file.

- `midi_file_path`: Path to the MIDI file to load
- `loop`: If True, the sequence will loop when reaching the end

#### `get_next_note() -> Optional[MidiNote]`
Get the next note in the sequence.

- Returns: The next MidiNote in the sequence, or None if the end is reached (unless loop=True)

#### `reset() -> None`
Reset the sequence to the beginning.

#### `get_note_count() -> int`
Get the total number of notes in the sequence.

- Returns: Number of notes

#### `get_total_duration() -> float`
Get the total duration of the MIDI sequence in seconds.

- Returns: Total duration in seconds

### MidiNote

A dataclass representing a single MIDI note with the following attributes:

- `pitch`: MIDI note number (0-127)
- `duration`: Note duration in seconds
- `velocity`: Note velocity (0-127, default=64)
- `start_time`: Note start time in seconds (default=0.0)

## Running Tests

To run the unit tests:

```bash
python -m pytest tests/test_midi_manager.py -v
```

## Dependencies

- Python 3.6+
- pretty_midi (for MIDI file parsing)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
