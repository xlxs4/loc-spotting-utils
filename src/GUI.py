from collections import deque
from copy import deepcopy
import logging
from pathlib import Path

from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPlainTextEdit, QVBoxLayout, QWidget, QToolBar,
    QPushButton, QStatusBar, QGroupBox, QHBoxLayout, QComboBox, QDoubleSpinBox,
    QFrame, QCheckBox, QFileDialog
)

from eltypes import config, gcode_line, operator
from GCodeUtils import dec_coor, inc_coor, replace_coor
from highlighter import Highlighter
from IOUtils import lines_to_text, read_gcode, text_to_lines, write_gcode
from paths import get_path


class GCodeUtilsGUI(QMainWindow):
    def __init__(self, config: config, relative_paths: bool):
        super().__init__()

        ICON_CONFIG = config.icon
        COOR_CONFIG = config.coordinate

        self._init_ui(COOR_CONFIG, ICON_CONFIG, relative_paths)

    def _init_ui(
        self, coor_config: config, icon_config: config, relative_paths: bool
    ) -> None:
        selector_threshold = coor_config["threshold"]

        self._create_io_group_box()
        self._create_coor_group_box(selector_threshold)
        self._create_coor_frame_separator()
        self._create_new_val_group_box(selector_threshold)
        self._create_additive_group_box()

        self.selected_gcode_path = QLabel(self.tr("Selected G-Code: "))

        self.gcode_viewer = QPlainTextEdit()
        self.gcode_viewer.setReadOnly(True)

        self.highlighter = Highlighter(self.gcode_viewer.document())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._io_group_box)
        main_layout.addWidget(self.selected_gcode_path)
        main_layout.addWidget(self.gcode_viewer)
        main_layout.addWidget(self._coor_group_box)
        main_layout.addWidget(self._frame_separator)
        main_layout.addWidget(self._new_val_group_box)
        main_layout.addWidget(self._additive_group_box)
        self.setLayout(main_layout)

        self.setWindowTitle(self.tr("Lab-On-a-Chip Spotting Utilties"))

        # To have widgets appear.
        dummy_widget = QWidget()
        dummy_widget.setLayout(main_layout)
        self.setCentralWidget(dummy_widget)

        toolbar = QToolBar("Edit")
        toolbar.setIconSize(
            QSize(
                icon_config["dimension"]["width"],
                icon_config["dimension"]["height"]
            )
        )
        self.addToolBar(toolbar)

        plus_button = QPushButton(
            QIcon(str(get_path("assets-plus", relative_paths))), "", self
        )
        plus_button.setStatusTip(
            self.tr("Increase X/Y/Z G-Code coordinates by value")
        )
        plus_button.clicked.connect(self._handle_plus_button)

        toolbar.addWidget(plus_button)

        minus_button = QPushButton(
            QIcon(str(get_path("assets-minus", relative_paths))), "", self
        )
        minus_button.setStatusTip(
            self.tr("Decrease X/Y/Z G-Code coordinates by value")
        )
        minus_button.clicked.connect(self._handle_minus_button)

        toolbar.addWidget(minus_button)
        toolbar.addSeparator()

        replace_button = QPushButton(
            QIcon(str(get_path("assets-replace", relative_paths))), "", self
        )
        replace_button.setStatusTip(
            self.tr("Replace X/Y/Z G-Code coordinates with value")
        )
        replace_button.clicked.connect(self._handle_replace_button)

        toolbar.addWidget(replace_button)
        toolbar.addSeparator()

        delete_button = QPushButton(
            QIcon(str(get_path("assets-delete", relative_paths))), "", self
        )
        delete_button.setStatusTip(self.tr("Delete selected lines"))
        delete_button.clicked.connect(self._handle_delete_button)

        toolbar.addWidget(delete_button)

        replicate_button = QPushButton(
            QIcon(str(get_path("assets-multiply", relative_paths))), "", self
        )
        replicate_button.setStatusTip(self.tr("Replicate selection"))
        replicate_button.clicked.connect(self._handle_replicate_button)

        toolbar.addWidget(replicate_button)
        toolbar.addSeparator()

        undo_button = QPushButton(
            QIcon(str(get_path("assets-undo", relative_paths))), "", self
        )
        undo_button.setStatusTip(self.tr("Undo last G-Code operation"))
        undo_button.clicked.connect(self._handle_undo_button)

        toolbar.addWidget(undo_button)
        toolbar.addSeparator()

        header_button = QPushButton(
            QIcon(str(get_path("assets-header", relative_paths))), "", self
        )
        header_button.setStatusTip(self.tr("Add/Remove header"))
        header_button.clicked.connect(self._handle_header_button)

        toolbar.addWidget(header_button)

        self.setStatusBar(QStatusBar(self))

        self.gcode = None
        self.previous_gcodes = deque()

    def _apply_coor_operator(self, op: operator) -> None:
        if self.gcode is not None:
            coor = self._coor_dropdown.currentText()
            new_val = self._new_coor_val.value()
            additive = self._additive_checkbox.isChecked()
            specific_val = self._specific_val_selector.value(
            ) if self._specific_val_checkbox.isChecked() else None

            new = []
            times = 1
            for line in self.gcode:
                new_line, found = op(
                    line, coor, new_val * times, additive, specific_val
                )
                if found:
                    times += 1
                new.append(new_line)

            self.gcode = new

    @Slot()
    def _handle_plus_button(self):
        self._save_last_gcode()
        self._apply_coor_operator(inc_coor)
        self._update_gcode_viewer()

    @Slot()
    def _handle_minus_button(self):
        self._save_last_gcode()
        self._apply_coor_operator(dec_coor)
        self._update_gcode_viewer()

    @Slot()
    def _handle_replace_button(self):
        self._save_last_gcode()
        self._apply_coor_operator(replace_coor)
        self._update_gcode_viewer()

    @Slot()
    def _handle_delete_button(self):
        cursor = self.gcode_viewer.textCursor()

        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()

        if sel_end == 0:
            return

        text = self.gcode_viewer.toPlainText().rstrip()
        if sel_start != 0:
            if text[sel_start - 1] != '\n':
                last_newline = text.rfind('\n', 0, sel_start - 1)
                sel_start = last_newline + 1 if last_newline != -1 else 0

        text_length = len(text)
        if sel_end >= text_length:
            sel_end = text_length - 1

        if text[sel_end] != '\n':
            if text[sel_end - 1] != '\n':
                next_newline = text.find('\n', sel_end)
                sel_end = next_newline + 1 if next_newline != -1 else text_length
        else:
            sel_end += 1

        new_text = text[:sel_start] + text[sel_end:]

        self._save_last_gcode()
        self._update_gcode_from_text(new_text)
        self._update_gcode_viewer()

    @Slot()
    def _handle_replicate_button(self):
        cursor = self.gcode_viewer.textCursor()
        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()

        if sel_end == 0:
            return

        text = self.gcode_viewer.toPlainText()
        sel_text = cursor.selection().toPlainText().rstrip() + '\n'

        val = self._new_coor_val.value()
        times = int(val) if val > 0 else 1

        new_text = text[:sel_start] + sel_text * times + text[sel_start:]

        self._save_last_gcode()
        self._update_gcode_from_text(new_text)
        self._update_gcode_viewer()

    @Slot()
    def _handle_undo_button(self) -> None:
        if self.previous_gcodes:
            self.gcode = self.previous_gcodes.pop()
            self._update_gcode_viewer()

    @Slot()
    def _handle_header_button(self) -> None:
        check_args = (
            (0, 0, 'G', '21'),
            (1, 0, 'G', '91'),
            (-1, 0, 'M', '84')
        )
        for args in check_args:
            if not self._check_gcode_equals(*args):
                self._add_header()
                return

        self._remove_header()

    def _create_io_group_box(self) -> None:
        self._io_group_box = QGroupBox(self.tr("IO"))
        layout = QHBoxLayout()

        browse_button = QPushButton(self.tr("Browse"))
        browse_button.clicked.connect(self._browse_gcode)

        save_button = QPushButton(self.tr("Save"))
        save_button.clicked.connect(self._save_gcode)

        layout.addWidget(browse_button)
        layout.addWidget(save_button)

        self._io_group_box.setLayout(layout)

    def _create_coor_group_box(self, selector_threshold: config) -> None:
        self._coor_group_box = QGroupBox(
            self.tr("Select coordinate/operator value")
        )
        layout = QHBoxLayout()

        self._coor_dropdown = QComboBox()
        self._coor_dropdown.addItems(['X', 'Y', 'Z'])

        self._new_coor_val = QDoubleSpinBox()
        self._new_coor_val.setRange(
            selector_threshold["min"], selector_threshold["max"]
        )

        layout.addWidget(self._coor_dropdown)
        layout.addWidget(self._new_coor_val)

        self._coor_group_box.setLayout(layout)

    def _create_coor_frame_separator(self) -> None:
        frame = QFrame()
        self._frame_separator = frame

    def _create_new_val_group_box(self, selector_threshold: config) -> None:
        self._new_val_group_box = QGroupBox(
            self.tr("Only change specific value")
        )
        layout = QHBoxLayout()

        self._specific_val_checkbox = QCheckBox(self.tr("Specific value only"))

        self._specific_val_selector = QDoubleSpinBox()
        self._specific_val_selector.setRange(
            selector_threshold["min"], selector_threshold["max"]
        )

        layout.addWidget(self._specific_val_checkbox)
        layout.addWidget(self._specific_val_selector)

        self._new_val_group_box.setLayout(layout)

    def _create_additive_group_box(self) -> None:
        self._additive_group_box = QGroupBox(
            self.tr("Apply coordinate operations in additive manner")
        )
        layout = QHBoxLayout()

        self._additive_checkbox = QCheckBox(
            self.tr("Additive operation application")
        )

        layout.addWidget(self._additive_checkbox)

        self._additive_group_box.setLayout(layout)

    def _browse_gcode(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.List)
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            gcode_filename = Path(gcode_filename)

            self.selected_gcode_path.setText(
                self.tr(f"Selected G-Code: {gcode_filename.name}")
            )
            self.gcode = read_gcode(gcode_filename)

            self._update_gcode_viewer()

            logging.info(f"Loaded file {gcode_filename.name} successfully.")

    def _save_gcode(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.List)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix(self.tr("gcode"))
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]
            write_gcode(gcode_filename, self.gcode)

            logging.info(f"Saved file {gcode_filename.name} successfully.")

    def _update_gcode_viewer(self) -> None:
        if self.gcode is not None:
            self.gcode_viewer.setPlainText(lines_to_text(self.gcode))

    def _update_gcode_from_text(self, text: str) -> None:
        self.gcode = text_to_lines(text)

    def _save_last_gcode(self) -> None:
        if self.gcode is not None:
            self.previous_gcodes.append(deepcopy(self.gcode))

    def _check_gcode_equals(self, line_index, gcode_index, letter, value):
        try:
            gcode = self.gcode[line_index].block.gcodes[gcode_index]
            return gcode.word.letter == letter and gcode.word.value_str == value
        except IndexError:
            return False
        
    def _add_header(self):
        self._save_last_gcode()

        self.gcode.insert(0, gcode_line("G21"))
        self.gcode.insert(1, gcode_line("G91"))
        self.gcode.append(gcode_line("M84"))

        self._update_gcode_viewer()

    def _remove_header(self):
        self._save_last_gcode()
        self.gcode = self.gcode[2:-1]
        self._update_gcode_viewer()
