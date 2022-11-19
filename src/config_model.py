from pydantic import BaseModel


class Config(BaseModel):
    icon: dict[str, dict[str, int]]
    window: dict[str, dict[str, int]]
    coordinate: dict[str, dict[str, int]]
