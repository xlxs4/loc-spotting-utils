from pathlib import Path

from pyprojroot import here

_PATHS = {
    "assets": "assets/",
    "assets-minus": "assets/minus.png",
    "assets-multiply": "assets/multiply.png",
    "assets-plus": "assets/plus.png",
    "assets-replace": "assets/replace.png",
    "assets-undo": "assets/undo.png",
    "config": "src/config.toml"
}


def get_path(name: str, relative: bool) -> Path:
    return here(_PATHS[name]) if not relative else _PATHS[name]
