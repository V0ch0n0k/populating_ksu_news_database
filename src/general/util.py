import json
import re
from typing import Dict

__all__ = ["load_data_from_json_by_path", "clean_newlines"]


def load_data_from_json_by_path(file_path: str) -> Dict:
    print(f"file_path={file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_newlines(text):
    return re.sub(r"\n+", " ", text).rstrip("\n ").strip()
