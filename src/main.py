import sys

import PySide6.QtWidgets as QtWidgets

from IOUtils import lines_to_text, read_gcode, write_gcode


class GCodeUtils(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        self.create_io_group_box()

        self.selected_gcode_path = QtWidgets.QLabel("Selected G-Code: ")

        self.gcode_viewer = QtWidgets.QPlainTextEdit()
        self.gcode_viewer.setReadOnly(True)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self._io_group_box)

        main_layout.addWidget(self.selected_gcode_path)
        main_layout.addWidget(self.gcode_viewer)

        self.setLayout(main_layout)

        self.setWindowTitle("Lab-On-a-Chip Spotting Utilties")

        self.gcode = None

    def create_io_group_box(self):
        self._io_group_box = QtWidgets.QGroupBox("IO")
        layout = QtWidgets.QHBoxLayout()

        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_gcode)

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(self.save_gcode)

        layout.addWidget(browse_button)
        layout.addWidget(save_button)

        self._io_group_box.setLayout(layout)

    def browse_gcode(self) -> None:
        dialog = QtWidgets.QFileDialog(self)

        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]

            self.selected_gcode_path.setText(f"Selected G-Code: {gcode_filename}")
            self.gcode = read_gcode(gcode_filename)

            self.update_gcode_viewer()

    def save_gcode(self) -> None:
        dialog = QtWidgets.QFileDialog(self)

        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setViewMode(QtWidgets.QFileDialog.List)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        dialog.setDefaultSuffix("gcode")
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            write_gcode(gcode_filename, self.gcode)
    
    def update_gcode_viewer(self) -> None:
        self.gcode_viewer.setPlainText(lines_to_text(self.gcode))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = GCodeUtils()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())