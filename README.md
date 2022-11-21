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
  - [Miscellaneous](#miscellaneous)

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

<details>
<summary>Click to expand</summary>

All [CI magic](https://github.com/xlxs4/loc-spotting-utils/actions/workflows/ci.yml) happens using [GitHub Actions](https://docs.github.com/en/actions).
The related configuration is all located within `.github/workflows/ci.yml`:

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

#### Source

#### Rest

### Miscellaneous

Icons:

- <a target="_blank" href="https://icons8.com/icon/FMj27qvOMorG/replace">Replace</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/7jhtnMWdpEf1/plus-math">Plus Math</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/occUe06FpCMr/subtract">Subtract</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/2VYfDlfknSJE/multiply">Multiply</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a target="_blank" href="https://icons8.com/icon/e1AG2cMLWdUG/return">Return</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
