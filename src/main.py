import sys

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

from IOUtils import read_gcode


class GCodeUtils(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        self.selected_gcode_path = QtWidgets.QLabel("Selected G-Code: ")

        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_gcode)

        self.gcode_viewer = QtWidgets.QPlainTextEdit()
        self.gcode_viewer.setReadOnly(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.selected_gcode_path)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.gcode_viewer)

        self.gcode = None

    def browse_gcode(self) -> None:
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            self.selected_gcode_path.setText(f"Selected G-Code: {gcode_filename}")
            self.gcode = read_gcode(gcode_filename)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = GCodeUtils()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())