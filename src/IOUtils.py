from pathlib import Path
import tomllib

from eltypes import config, gcode_line, lines, str_lines


def _str_to_path(str: str) -> Path:
    return Path(str)

def _lines_to_str_lines(lines: lines) -> str_lines:
    return [str(line) for line in lines]

def lines_to_text(lines: lines) -> str:
    return '\n'.join(str(g) for g in lines)

def _read_line_by_line(filename: Path) -> lines:
    with open(filename) as file:
        return [gcode_line(line.rstrip()) for line in file]

def read_gcode(filename: str) -> lines:
    return _read_line_by_line(_str_to_path(filename))

def _write_line_by_line(filename: Path, lines: lines):
    lines = _lines_to_str_lines(lines)
    with open(filename, 'w+') as file:
        for line in lines[:-1]:
            file.write(line + '\n')
        file.write(lines[-1])

def write_gcode(filename: str, lines: lines):
    _write_line_by_line(_str_to_path(filename), lines)

def read_config(filename: str) -> config:
    return _read_config(_str_to_path(filename))

def _read_config(filename: Path) -> config:
    with open(filename, mode='rb') as fp:
        config = tomllib.load(fp)
    return config
