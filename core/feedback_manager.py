import json
import os
import socket
import getpass
from datetime import datetime
from pathlib import Path

from core.version import APP_VERSION
from core.update_manager import REMOTE_ROOT


LOCAL_FEEDBACK_DIR = Path.home() / ".spreadsheet_compare" / "feedback"
LOCAL_FEEDBACK_FILE = LOCAL_FEEDBACK_DIR / "feedback.jsonl"

REMOTE_FEEDBACK_ROOT = os.environ.get(
    "SSC_FEEDBACK_ROOT",
    os.path.join(REMOTE_ROOT, "feedback"),
)


def _build_entry(message, kind="general", user=None):
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user or getpass.getuser(),
        "machine": socket.gethostname(),
        "version": APP_VERSION,
        "type": kind,
        "message": message,
    }


def _append_json_line(path, entry):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _append_remote(entry):
    if not REMOTE_FEEDBACK_ROOT:
        return False
    try:
        remote_dir = Path(REMOTE_FEEDBACK_ROOT)
        remote_dir.mkdir(parents=True, exist_ok=True)
        fname = f"feedback_{socket.gethostname()}_{getpass.getuser()}.jsonl"
        remote_path = remote_dir / fname
        _append_json_line(remote_path, entry)
        return True
    except Exception:
        return False


def submit_feedback(message, kind="general", user=None):
    entry = _build_entry(message, kind=kind, user=user)
    _append_json_line(LOCAL_FEEDBACK_FILE, entry)
    remote_ok = _append_remote(entry)
    return True, remote_ok
