# MIDI Router

## Overview

MIDI Router is a PyQt6-based application that allows you to route MIDI messages from an input port to multiple output ports. It provides a graphical user interface to select MIDI input and output ports, start and stop the message forwarding, and display the forwarded MIDI messages.

## Features

- Select MIDI input port
- Select multiple MIDI output ports
- Start and stop MIDI message forwarding
- Refresh the list of available MIDI devices
- Display the forwarded MIDI messages

## Requirements

- Python 3.x
- `mido` library
- `python-rtmidi` library
- `PyQt6` library

## Installation

1. Install Python 3.x from the official [Python website](https://www.python.org/).
2. Install the required libraries using pip:

```sh
pip install mido python-rtmidi PyQt6
```

## Usage

1. Clone the repository or download the `midi_router.py` file.
2. Run the `midi_router.py` script:

```sh
python midi_router.py
```
3. The application window will open. Use the dropdown menus to select the MIDI input and output ports.
4. Click the "Start" button to begin forwarding MIDI messages.
5. Click the "Stop" button to stop forwarding MIDI messages.
6. Click the "Refresh Devices" button to refresh the list of available MIDI devices.
7. The forwarded MIDI messages will be displayed in the application window.

## Code Structure

- `MidiForwarder` class: Handles the MIDI message forwarding in a separate thread.
- `MainWindow` class: Manages the graphical user interface and user interactions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [mido](https://github.com/mido/mido) - MIDI Objects for Python
- [PyQt6](https://riverbankcomputing.com/software/pyqt/intro) - Python bindings for Qt libraries

