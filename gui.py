import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QCheckBox, QTextEdit, QScrollBar
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QProcess

# Default Base Directory
BASE_DIR = "Disneyland_Audio"

class AudioManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess(self)  # Create process instance
        self.is_dark_mode = True  # Theme State (Dark Mode by Default)
        self.initUI()

    def initUI(self):
        # Window Setup
        self.setWindowTitle("Disneyland Audio Manager")
        self.setGeometry(100, 100, 500, 550)
        self.setWindowIcon(QIcon("assets/icon.ico"))  # Optional: Set an icon

        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title Label
        self.title_label = QLabel("Disneyland Audio Manager", self)
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Divider Line
        self.divider = QFrame(self)
        self.divider.setFrameShape(QFrame.Shape.HLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.divider)

        # Add Spacing
        self.layout.addSpacing(10)

        # Output Console
        self.output_console = QTextEdit(self)
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 10))
        self.output_console.setMaximumHeight(250)  # Restrict console height
        self.output_console.setStyleSheet("""
            background-color: #181818;
            color: #E0E0E0;
            font-family: Consolas, Courier, monospace;
            padding: 8px;
            border-radius: 5px;
        """)
        self.layout.addWidget(self.output_console)

        # Add Spacing
        self.layout.addSpacing(15)

        # Button Style
        self.button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1F618D;
            }
        """

        # Scripts List
        scripts = [
            ("Download Songs", "download_songs.py"),
            ("Check Metadata", "check_metadata.py"),
            ("Fix Metadata", "fix_metadata.py"),
            ("Uniform Artist", "uniform_artist.py"),
            ("Add Album Art", "add_album_art.py"),
            ("Remove Holiday Tracks", "remove_holiday_tracks.py"),
        ]

        # Button Layout
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create Buttons
        self.buttons = []
        for text, script in scripts:
            btn = QPushButton(text, self)
            btn.setStyleSheet(self.button_style)
            btn.setFont(QFont("Arial", 12))
            btn.setFixedSize(320, 40)
            btn.clicked.connect(lambda checked, s=script: self.run_script(s))
            self.button_layout.addWidget(btn)
            self.buttons.append(btn)

        self.layout.addLayout(self.button_layout)  # Add buttons as a separate layout

        # Centered Theme Toggle Switch
        self.toggle_layout = QHBoxLayout()
        self.theme_toggle = QCheckBox("Dark Mode", self)
        self.theme_toggle.setFont(QFont("Arial", 11))
        self.theme_toggle.setChecked(True)  # Start in Dark Mode
        self.theme_toggle.setStyleSheet("padding: 10px;")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        self.toggle_layout.addWidget(self.theme_toggle, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.toggle_layout)

        # Apply Dark Mode by Default
        self.set_dark_mode()

        self.setLayout(self.layout)

    def run_script(self, script):
        """Runs the selected script within the application and captures output."""
        
        if getattr(sys, 'frozen', False):  # ✅ Now correctly indented inside the function
            base_path = os.path.join(sys._MEIPASS, "scripts")  # Extracted scripts directory
        else:
            base_path = os.path.join(os.getcwd(), "scripts")  # Running from source

        script_path = os.path.join(base_path, script)

        if not os.path.exists(script_path):
            self.output_console.append(f"Error: Script '{script}' not found!")
            return  # ✅ Now correctly inside the function

        self.process.setProgram("python")
        self.process.setArguments([script_path])
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)
        self.process.finished.connect(lambda: self.output_console.append("Task completed!\n"))
        self.process.start()

    def read_output(self):
        """Reads output from the running script and displays it in the console."""
        output = self.process.readAllStandardOutput().data().decode()
        error = self.process.readAllStandardError().data().decode()
        
        if output.strip():
            self.output_console.append(output.strip())
        if error.strip():
            self.output_console.append(f"<span style='color:red;'>{error.strip()}</span>")
        
        # Auto-scroll to the bottom
        self.output_console.verticalScrollBar().setValue(self.output_console.verticalScrollBar().maximum())

    def toggle_theme(self):
        """Switches between Dark and Light mode based on toggle state."""
        if self.theme_toggle.isChecked():
            self.set_dark_mode()
        else:
            self.set_light_mode()


    def set_dark_mode(self):
        """Applies Dark Mode Theme."""
        self.setStyleSheet("""
            background-color: #1E1E1E;
            color: #E0E0E0;
            font-size: 14px;
            border-radius: 10px;
        """)
        self.divider.setStyleSheet("background-color: #5A5A5A;")
        for btn in self.buttons:
            btn.setStyleSheet(self.button_style)
        self.theme_toggle.setText("Dark Mode")

    def set_light_mode(self):
        """Applies Light Mode Theme."""
        self.setStyleSheet("""
            background-color: #F0F0F0;
            color: #202020;
            font-size: 14px;
            border-radius: 10px;
        """)
        self.divider.setStyleSheet("background-color: #D0D0D0;")
        for btn in self.buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: black;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 14px;
                    min-width: 300px;
                }
                QPushButton:hover {
                    background-color: #5DADE2;
                }
                QPushButton:pressed {
                    background-color: #85C1E9;
                }
            """)
        self.theme_toggle.setText("Light Mode")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioManagerGUI()
    window.show()
    sys.exit(app.exec())
