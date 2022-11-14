from pathlib import Path

_PATHS = {
    "assets": Path("assets/"),
    "assets-minus": Path("assets/minus.png"),
    "assets-plus": Path("assets/plus.png"),
    "assets-replace": Path("assets/replace.png")
}

def get_path(name: str) -> Path:
    return _PATHS[name]
