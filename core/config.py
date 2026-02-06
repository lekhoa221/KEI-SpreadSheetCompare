import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".spreadsheet_compare"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    if not CONFIG_FILE.exists():
        return {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_last_open_dir():
    data = load_config()
    last_dir = data.get("last_open_dir")
    if last_dir and Path(last_dir).exists():
        return str(last_dir)
    return str(Path.home())


def update_last_open_dir(path):
    if not path:
        return
    data = load_config()
    data["last_open_dir"] = str(path)
    save_config(data)
