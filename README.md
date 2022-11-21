<div align="center">
<p>
    <a href="https://benchling.com/organizations/acubesat/">Benchling 🎐🧬</a> &bull;
    <a href="https://gitlab.com/acubesat/documentation/cdr-public/-/blob/master/DDJF/DDJF_PL.pdf?expanded=true&viewer=rich">DDJF_PL 📚🧪</a> &bull;
    <a href="https://spacedot.gr/">SpaceDot 🌌🪐</a> &bull;
    <a href="https://acubesat.spacedot.gr/">AcubeSAT 🛰️🌎</a>
</p>
</div>

## Description

A repository to host code and a bunch of other stuff. These have to do with our efforts to repurpose a [Prusa i3 MKRS3+](https://www.prusa3d.com/category/original-prusa-i3-mk3s/) 3D printer to serve as a DIY DNA microarray spotter so that we can put *S. cerevisiae* cells inside a PDMS Lab-On-a-Chip (check [here](https://gitlab.com/acubesat/su/microfluidics) too!).

## Table of Contents

<details>
<summary>Click to expand</summary>

- [Description](#description)
- [Table of Contents](#table-of-contents)
- [GUI Spotting Utilities](#gui-spotting-utilities)
  - [Description](#description-1)
  - [File Structure](#file-structure)
    - [CI](#ci)
    - [Assets](#assets)
    - [Source](#source)
    - [Rest](#rest)

</details>

## GUI Spotting Utilities

### Description

TODO:

### File Structure

<details>
<summary>Click to expand</summary>

```graphql
./.github/workflows
└─ ci.yml
./assets/
├─ minus.png
├─ multiply.png
├─ plus.png
├─ replace.png
└─ undo.png
./src/
├─ config_model.py
├─ config.toml
├─ eltypes.py
├─ GCodeUtils.py
├─ GUI.py
├─ highlighter.py
├─ IOUtils.py
├─ main.py
├─ operators.py
└─ paths.py
.editorconfig
add-files-to-spec
poetry.lock
poetry.toml
pyproject.toml
```

</details>

#### CI

All [CI magic](https://github.com/xlxs4/loc-spotting-utils/actions/workflows/ci.yml) happens using [GitHub Actions](https://docs.github.com/en/actions).
The related configuration is all located within `.github/workflows/ci.yml`:

<details>
<summary>Click to expand</summary>

```yaml
name: CI
run-name: ${{ github.actor }} is running 🚀
on: [push] # Triggered by push.

jobs:
  ci:
    strategy:
      fail-fast: false # Don't fail all jobs if a single job fails.
      matrix:
        python-version: ["3.11"]
        poetry-version: ["1.2.2"] # Poetry is used for project/dependency management.
        os: [ubuntu-latest, macos-latest, windows-latest]
        include: # Where pip stores its cache is OS-dependent.
          - pip-cache-path: ~/.cache
            os: ubuntu-latest
          - pip-cache-path: ~/.cache
            os: macos-latest
          - pip-cache-path: ~\appdata\local\pip\cache
            os: windows-latest
    defaults:
      run:
        shell: bash # For sane consistent scripting throughout.
    runs-on: ${{ matrix.os }} # For each OS:
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
      - name: Setup Python
        id: setup-python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: ${{ matrix.poetry-version }}
          virtualenvs-create: true
          virtualenvs-in-project: true # Otherwise the venv will be the same across all OSes.
          installer-parallel: true
      - name: Load cached venv
        id: cached-pip-wheels
        uses: actions/cache@v3
        with:
          path: ${{ matrix.pip-cache-path }}
          key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}
      - name: Install dependencies
        run: poetry install --no-interaction --no-root -E build -E format # https://github.com/python-poetry/poetry/issues/1227
      - name: Check formatting
        run: |
          source $VENV
          yapf -drp --no-local-style --style "facebook" src/
      - name: Build for ${{ matrix.os }}
        run: | # https://stackoverflow.com/questions/19456518/error-when-using-sed-with-find-command-on-os-x-invalid-command-code
          source $VENV
          pyi-makespec src/main.py
          if [ "$RUNNER_OS" == "macOS" ]; then
            sed -i '' -e '2 r add-files-to-spec' main.spec
            sed -i '' -e 's/datas=\[]/datas=added_files/' main.spec
          else
            sed -i '2 r add-files-to-spec' main.spec
            sed -i 's/datas=\[]/datas=added_files/' main.spec
          fi
          pyinstaller main.spec
      - name: Archive binary artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.os }}-bundle
          path: dist
```

</details>

On each push, the application is bundled into a single folder containing an executable, for each OS.
This happens using [`pyinstaller`](https://www.pyinstaller.org/).
First there's a formatting check using [`yapf`](https://github.com/google/yapf).
Then, the application is built.
`pytest` is included as an extra optional dependency to add unit test support in the future.
Everything is cached when possible.
If the job terminates successfully, the bundle folder for each OS is uploaded as an [artifact](https://github.com/xlxs4/loc-spotting-utils/actions/runs/3518601483) that the user can download, instead of having to run `pyinstaller` locally, or having to install `python` and the project dependencies locally through `poetry`.

#### Assets

Icons:

- <a target="_blank" href="https://icons8.com/icon/FMj27qvOMorG/replace">Replace</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/7jhtnMWdpEf1/plus-math">Plus Math</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/occUe06FpCMr/subtract">Subtract</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/2VYfDlfknSJE/multiply">Multiply</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/e1AG2cMLWdUG/return">Return</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

#### Source

`main.py` is the entrypoint to be run:

<details>
<summary>Click to expand</summary>

```python
from sys import exit

from PySide6.QtWidgets import QApplication

from GUI import GCodeUtilsGUI
from IOUtils import read_config
from paths import get_path

if __name__ == "__main__":
    relative_paths = True
    CONFIG = read_config(get_path("config", relative_paths))
    if not CONFIG:
        exit(1)

    WINDOW_CONFIG = CONFIG.window

    app = QApplication([])

    window = GCodeUtilsGUI(CONFIG, relative_paths)
    window.resize(
        WINDOW_CONFIG["dimension"]["width"],
        WINDOW_CONFIG["dimension"]["height"]
    )
    window.show()

    exit(app.exec())
```

</details>

It creates the GUI (using [`PySide6`](https://pypi.org/project/PySide6/)) main application.
Configuration for the GUI is stored in a separate [TOML](https://github.com/toml-lang/toml) file, `config.toml`.
The config model is verified using [`pydantic`](https://pydantic-docs.helpmanual.io/).

---

The GUI is the backbone of the application, and it's described in `gui.py`:

<details>
<summary>Click to expand</summary>

```python
from collections import deque
from copy import deepcopy

from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPlainTextEdit, QVBoxLayout, QWidget, QToolBar,
    QPushButton, QStatusBar, QGroupBox, QHBoxLayout, QComboBox, QSpinBox,
    QFrame, QCheckBox, QFileDialog
)

from eltypes import config
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

        self.setStatusBar(QStatusBar(self))

        self.gcode = None
        self.previous_gcodes = deque()

    @Slot()
    def _handle_plus_button(self):
        self._save_last_gcode()
        if self._specific_val_checkbox.isChecked():
            self.gcode = [
                inc_coor(
                    line,
                    self._coor_dropdown.currentText(),
                    self._new_coor_val.value(),
                    only_for_val=self._specific_val_selector.value()
                ) for line in self.gcode
            ]
        else:
            self.gcode = [
                inc_coor(
                    line, self._coor_dropdown.currentText(),
                    self._new_coor_val.value()
                ) for line in self.gcode
            ]

        self._update_gcode_viewer()

    @Slot()
    def _handle_minus_button(self):
        self._save_last_gcode()
        if self._specific_val_checkbox.isChecked():
            self.gcode = [
                dec_coor(
                    line,
                    self._coor_dropdown.currentText(),
                    self._new_coor_val.value(),
                    only_for_val=self._specific_val_selector.value()
                ) for line in self.gcode
            ]
        else:
            self.gcode = [
                dec_coor(
                    line, self._coor_dropdown.currentText(),
                    self._new_coor_val.value()
                ) for line in self.gcode
            ]

        self._update_gcode_viewer()

    @Slot()
    def _handle_replace_button(self):
        self._save_last_gcode()
        if self._specific_val_checkbox.isChecked():
            self.gcode = [
                replace_coor(
                    line,
                    self._coor_dropdown.currentText(),
                    self._new_coor_val.value(),
                    only_for_val=self._specific_val_selector.value()
                ) for line in self.gcode
            ]
        else:
            self.gcode = [
                replace_coor(
                    line, self._coor_dropdown.currentText(),
                    self._new_coor_val.value()
                ) for line in self.gcode
            ]

        self._update_gcode_viewer()

    @Slot()
    def _handle_replicate_button(self):
        self._save_last_gcode()
        cursor = self.gcode_viewer.textCursor()
        sel_start = cursor.selectionStart()

        text = self.gcode_viewer.toPlainText()
        sel_text = cursor.selection().toPlainText().rstrip() + '\n'

        val = self._new_coor_val.value()
        times = val if val > 0 else 1

        new_text = text[:sel_start] + sel_text * times + text[sel_start:]

        self._update_gcode_from_text(new_text)
        self._update_gcode_viewer()

    @Slot()
    def _handle_undo_button(self) -> None:
        if self.previous_gcodes:
            self.gcode = self.previous_gcodes.pop()
            self._update_gcode_viewer()

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

        self._new_coor_val = QSpinBox()
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

        self._specific_val_selector = QSpinBox()
        self._specific_val_selector.setRange(
            selector_threshold["min"], selector_threshold["max"]
        )

        layout.addWidget(self._specific_val_checkbox)
        layout.addWidget(self._specific_val_selector)

        self._new_val_group_box.setLayout(layout)

    def _browse_gcode(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.List)
        dialog.setNameFilter(self.tr("G-Code (*.gcode)"))

        if dialog.exec():
            gcode_filename = dialog.selectedFiles()[0]

            self.selected_gcode_path.setText(
                self.tr(f"Selected G-Code: {gcode_filename}")
            )
            self.gcode = read_gcode(gcode_filename)

            self._update_gcode_viewer()

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

    def _update_gcode_viewer(self) -> None:
        self.gcode_viewer.setPlainText(lines_to_text(self.gcode))

    def _update_gcode_from_text(self, text: str) -> None:
        self.gcode = text_to_lines(text)

    def _save_last_gcode(self) -> None:
        self.previous_gcodes.append(deepcopy(self.gcode))
```

</details>

Essentially, there's:

- A toolbar
- Various buttons
- Selectors
- A reader
- A G-Code syntax highlighter

A G-Code can be loaded into the app through the `Browse` button, and saved through the `Save` button, respectively.
After a G-Code file is loaded, its absolute path is logged and its content is put in the reader for the user to browse.

The reader supports the following keybinds:

| Keybind | Description |
| ------- | ----------- |
| `UpArrow` | Moves one line up |
| `DownArrow` | Moves one line down |
| `LeftArrow` | Moves one character to the left |
| `RightArrow` | Moves one character to the right |
| `PageUp` | Moves one (viewport) page up |
| `PageDown` | Moves one (viewport) page down |
| `Home` | Moves to the beginning of the G-Code |
| `End` | Moves to the end of the G-Code |
| `Alt+Wheel` | Scrolls the page horizontally |
| `Ctrl+Wheel` | Zooms the G-Code |
| `Ctrl+A` | Selects all text |

The application supports proper G-Code *parsing*, through [`pygcode`](https://github.com/fragmuffin/pygcode).
There are four G-Code operations supported:

1. **Add**: Increase coordinate(s) by specified amount (plus button)
2. **Sub**: Decrease coordinate(s) by specified amount (minus button)
3. **Replace**: Set coordinate(s) to new value (replace button)
4. **Replicate**: Replicated selected text X times (multiply button)

The user can select whether to apply the operations to the `X`, `Y` or `Z` coordinates.
Additionally, instead of applying an operations to *every* `X|Y|Z` coordinate value, the user can instead only apply it to the `X|Y|Z` coordinate that are of a specified value.

Applying each of these operations can be reversed through the **Undo** button.

#### Rest
