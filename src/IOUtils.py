from pathlib import Path


file_lines = list[str]


def _str_to_path(str: str) -> Path:
    return Path(str)

def _read_line_by_line(filename: Path) -> file_lines:
    with open(filename) as file:
        return [line.rstrip() for line in file]

def read_gcode(filename: str) -> file_lines:
    return _read_line_by_line(_str_to_path(filename))


