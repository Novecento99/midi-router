import mido
import sys
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MidiForwarder(QThread):
    # Signal to send MIDI messages back to the main thread
    message_signal = pyqtSignal(str)

    def __init__(self, input_port, output_ports):
        super().__init__()
        self.input_port = input_port
        self.output_ports = output_ports
        self.running = True

    def run(self):
        """Run the message forwarding in a separate thread."""
        with mido.open_input(self.input_port) as inport:
            outports = [mido.open_output(port) for port in self.output_ports]
            try:
                while self.running:
                    for msg in inport.iter_pending():
                        for outport in outports:
                            outport.send(msg)
                        self.message_signal.emit(
                            str(msg)
                        )  # Emit message to update label
            finally:
                for outport in outports:
                    outport.close()

    def stop(self):
        """Stop the message forwarding."""
        self.running = False
        self.quit()
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MIDI Router")
        self.setGeometry(100, 100, 400, 300)

        self.input_label = QLabel("Select input port:", self)
        self.input_label.move(20, 20)

        self.input_combo = QComboBox(self)
        self.input_combo.move(150, 20)

        self.output_label = QLabel("Select output ports:", self)
        self.output_label.move(20, 60)

        self.output_combo1 = QComboBox(self)
        self.output_combo1.move(150, 60)

        self.output_combo2 = QComboBox(self)
        self.output_combo2.move(150, 100)

        self.start_button = QPushButton("Start", self)
        self.start_button.move(150, 140)
        self.start_button.clicked.connect(self.start_forwarding)

        # Stop button to stop forwarding
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.move(150, 180)
        self.stop_button.clicked.connect(self.stop_forwarding)
        self.stop_button.setEnabled(False)  # Initially disabled

        # Refresh button to refresh devices
        self.refresh_button = QPushButton("Refresh Devices", self)
        self.refresh_button.move(150, 220)
        self.refresh_button.clicked.connect(self.refresh_devices)

        # QLabel to show MIDI message
        self.message_label = QLabel("MIDI Message: None", self)
        self.message_label.move(20, 260)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_combo)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_combo1)
        layout.addWidget(self.output_combo2)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)  # Add stop button to the layout
        layout.addWidget(self.refresh_button)  # Add refresh button to the layout
        layout.addWidget(self.message_label)  # Add message label to the layout

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.populate_input_ports()
        self.populate_output_ports()

        self.midi_forwarder = None

    def populate_input_ports(self):
        self.input_combo.clear()
        input_ports = mido.get_input_names()
        self.input_combo.addItems(input_ports)

    def populate_output_ports(self):
        self.output_combo1.clear()
        self.output_combo2.clear()
        output_ports = mido.get_output_names()
        self.output_combo1.addItems(output_ports)
        self.output_combo2.addItems(output_ports)

    def refresh_devices(self):
        """Refresh the list of MIDI devices."""
        self.populate_input_ports()
        self.populate_output_ports()

    def update_message_label(self, msg):
        """Update the message label with the current MIDI message."""
        self.message_label.setText(f"MIDI Message: {msg}")

    def start_forwarding(self):
        input_port = self.input_combo.currentText()
        output_ports = [
            self.output_combo1.currentText(),
            self.output_combo2.currentText(),
        ]

        print("Input port:", input_port)
        print("Output ports:", output_ports)

        if self.midi_forwarder:
            self.midi_forwarder.stop()

        self.midi_forwarder = MidiForwarder(input_port, output_ports)
        self.midi_forwarder.message_signal.connect(self.update_message_label)
        self.midi_forwarder.start()

        # Disable Start button and enable Stop button
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_forwarding(self):
        """Stop the message forwarding."""
        if self.midi_forwarder:
            self.midi_forwarder.stop()

        # Disable Stop button and enable Start button
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
