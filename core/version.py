from pathlib import Path

DEFAULT_VERSION = "1.0.7"


def _read_version():
    try:
        root = Path(__file__).resolve().parents[1]
        version_file = root / "VERSION.txt"
        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()
    except Exception:
        pass
    return DEFAULT_VERSION


APP_VERSION = _read_version()
CURRENT_VERSION = APP_VERSION
