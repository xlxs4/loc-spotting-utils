from pathlib import Path

from pygcode import GCodeLinearMove

from eltypes import gcode_line, lines, str_lines


def _str_to_path(str: str) -> Path:
    return Path(str)

def _read_line_by_line(filename: Path) -> lines:
    with open(filename) as file:
        return [gcode_line(line.rstrip()) for line in file]

def read_gcode(filename: str) -> lines:
    return _read_line_by_line(_str_to_path(filename))

def _write_line_by_line(filename: Path, lines: str_lines):
    with open(filename, 'w+') as file:
        for line in lines[:-1]:
            file.write(line + '\n')
        file.write(lines[-1])

def write_gcode(filename: str, lines: str_lines):
    _write_line_by_line(_str_to_path(filename), lines)
