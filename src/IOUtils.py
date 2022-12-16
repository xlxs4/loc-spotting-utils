from pathlib import Path
from tomllib import load

from config_model import Config
from eltypes import config, config_model, gcode_line, lines, str_lines


def _lines_to_str_lines(lines: lines) -> str_lines:
    return [str(line) for line in lines]


def lines_to_text(lines: lines) -> str:
    return '\n'.join(str(g) for g in lines)


def text_to_lines(text: str) -> lines:
    return [gcode_line(line.rstrip()) for line in text.split('\n')]


def _read_line_by_line(filename: Path) -> lines:
    with open(filename) as file:
        return [gcode_line(line.rstrip()) for line in file]


def read_gcode(filename: Path) -> lines:
    return _read_line_by_line(filename)


def _write_line_by_line(filename: Path, lines: lines):
    lines = _lines_to_str_lines(lines)
    with open(filename, 'w+') as file:
        for line in lines:
            file.write(line + '\n')


def write_gcode(filename: Path, lines: lines):
    _write_line_by_line(filename, lines)


def _read_toml(filename: Path) -> config:
    with open(filename, mode='rb') as fp:
        config = load(fp)
    return config


def read_config(filename: Path) -> config_model:
    conf_from_file = _read_toml(filename)
    return Config.parse_obj(conf_from_file)
