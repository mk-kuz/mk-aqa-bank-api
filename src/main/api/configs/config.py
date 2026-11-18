from pathlib import Path
from typing import Dict


class Config:
    _instance = None
    _properties: Dict[str, str] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_properties()
        return cls._instance

    @classmethod
    def _load_properties(cls):
        config_path = Path(__file__).resolve().parents[4] / "resources" / "urls.properties"
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    cls._properties[key.strip()] = value.strip()

    @classmethod
    def fetch(cls, key: str) -> str:
        if cls._instance is None:
            cls()
        return cls._properties.get(key, "")
