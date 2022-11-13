from pathlib import Path

from pygcode import Line, GCodeLinearMove


lines = list[Line]
str_lines = list[str]

def _str_to_path(str: str) -> Path:
    return Path(str)

def _read_line_by_line(filename: Path) -> lines:
    with open(filename) as file:
        return [Line(line.rstrip()) for line in file]

def read_gcode(filename: str) -> lines:
    return _read_line_by_line(_str_to_path(filename))
