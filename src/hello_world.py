import random
import sys

import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets

from IOUtils import read_gcode


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        self.hello = ["Hello Wêreld!", "Hej Verden!", "Γειά σου Κόσμε!", "こんにちは世界"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

        gcode_filename = None
        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            print(read_gcode(gcode_filename))

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())