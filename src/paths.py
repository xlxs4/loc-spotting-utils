from pathlib import Path

from pyprojroot import here

_PATHS = {
    "assets": here("assets/"),
    "assets-minus": here("assets/minus.png"),
    "assets-plus": here("assets/plus.png"),
    "assets-replace": here("assets/replace.png"),
    "config": here("src/config.toml")
}

def get_path(name: str) -> Path:
    return _PATHS[name]
