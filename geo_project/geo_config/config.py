import json
from typing import Dict

class Config:
    lang: Dict[str, str] = {}

    @classmethod
    def load_language (cls, code: str) -> None:
        with open(f"locales/{code}.json", "r", encoding="utf-8") as f:
            cls.lang = json.load(f)