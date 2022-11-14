import sys

import PySide6.QtWidgets as QtWidgets

from IOUtils import lines_to_text, read_gcode, write_gcode


class GCodeUtils(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self._create_io_group_box()

        self.selected_gcode_path = QtWidgets.QLabel(self.tr("Selected G-Code: "))

        self.gcode_viewer = QtWidgets.QPlainTextEdit()
        self.gcode_viewer.setReadOnly(True)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self._io_group_box)

        main_layout.addWidget(self.selected_gcode_path)
        main_layout.addWidget(self.gcode_viewer)

        self.setLayout(main_layout)

        self.setWindowTitle(self.tr("Lab-On-a-Chip Spotting Utilties"))

        dummy_widget = QtWidgets.QWidget()
        dummy_widget.setLayout(main_layout)
        self.setCentralWidget(dummy_widget)

        self.gcode = None

    def _create_io_group_box(self):
        self._io_group_box = QtWidgets.QGroupBox(self.tr("IO"))
        layout = QtWidgets.QHBoxLayout()

        browse_button = QtWidgets.QPushButton(self.tr("Browse"))
        browse_button.clicked.connect(self._browse_gcode)

        save_button = QtWidgets.QPushButton(self.tr("Save"))
        save_button.clicked.connect(self._save_gcode)

        layout.addWidget(browse_button)
        layout.addWidget(save_button)

        self._io_group_box.setLayout(layout)

    def _browse_gcode(self) -> None:
        dialog = QtWidgets.QFileDialog(self)

        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]

            self.selected_gcode_path.setText(self.tr(f"Selected G-Code: {gcode_filename}"))
            self.gcode = read_gcode(gcode_filename)

            self._update_gcode_viewer()

    def _save_gcode(self) -> None:
        dialog = QtWidgets.QFileDialog(self)

        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setViewMode(QtWidgets.QFileDialog.List)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        dialog.setDefaultSuffix(self.tr("gcode"))
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            write_gcode(gcode_filename, self.gcode)
    
    def _update_gcode_viewer(self) -> None:
        self.gcode_viewer.setPlainText(lines_to_text(self.gcode))


if __name__ == "__main__":
    WIDTH, HEIGHT = (600, 700)
    app = QtWidgets.QApplication([])

    window = GCodeUtils()
    window.resize(WIDTH, HEIGHT)
    window.show()

    sys.exit(app.exec())