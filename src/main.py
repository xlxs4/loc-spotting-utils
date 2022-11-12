import sys

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

from IOUtils import read_gcode


class GCodeUtils(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Browse")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.browse_gcode)

    def browse_gcode(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            print(read_gcode(gcode_filename))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = GCodeUtils()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())