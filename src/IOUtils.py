from pathlib import Path
from tomllib import load

from eltypes import config, gcode_line, lines, str_lines


def _lines_to_str_lines(lines: lines) -> str_lines:
    return [str(line) for line in lines]


def lines_to_text(lines: lines) -> str:
    return '\n'.join(str(g) for g in lines)


def _read_line_by_line(filename: Path) -> lines:
    with open(filename) as file:
        return [gcode_line(line.rstrip()) for line in file]


def read_gcode(filename: Path) -> lines:
    return _read_line_by_line(filename)


def _write_line_by_line(filename: Path, lines: lines):
    lines = _lines_to_str_lines(lines)
    with open(filename, 'w+') as file:
        for line in lines[:-1]:
            file.write(line + '\n')
        file.write(lines[-1])


def write_gcode(filename: Path, lines: lines):
    _write_line_by_line(filename, lines)


def _read_toml(filename: Path) -> config:
    with open(filename, mode='rb') as fp:
        config = load(fp)
    return config


def read_config(filename: Path) -> config:
    return _read_toml(filename)
