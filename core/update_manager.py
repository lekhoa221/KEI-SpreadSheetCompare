import json
import os
import re
from pathlib import Path

DEFAULT_REMOTE_ROOT = r"\\10.1.3.2\KEIToolsData\SpreadSheetCompare"
REMOTE_ROOT = DEFAULT_REMOTE_ROOT


def resolve_update_root():
    override = os.environ.get("SSC_UPDATE_ROOT")
    if override:
        return override
    if os.path.exists(DEFAULT_REMOTE_ROOT):
        return DEFAULT_REMOTE_ROOT
    local_root = Path(__file__).resolve().parents[1]
    if (local_root / "LATEST.txt").exists():
        return str(local_root)
    return DEFAULT_REMOTE_ROOT


def _parse_version(value):
    parts = re.findall(r"\d+", str(value or ""))
    if not parts:
        return (0,)
    return tuple(int(p) for p in parts)


def is_newer_version(latest, current):
    latest_parts = list(_parse_version(latest))
    current_parts = list(_parse_version(current))
    max_len = max(len(latest_parts), len(current_parts))
    latest_parts += [0] * (max_len - len(latest_parts))
    current_parts += [0] * (max_len - len(current_parts))
    return tuple(latest_parts) > tuple(current_parts)


def read_latest_version():
    update_root = resolve_update_root()
    latest_file = os.path.join(update_root, "LATEST.txt")
    if not os.path.exists(latest_file):
        return None, f"LATEST.txt not found at {latest_file}"
    try:
        with open(latest_file, "r", encoding="utf-8-sig") as f:
            latest = (f.read() or "").strip()
        if not latest:
            return None, "LATEST.txt is empty"
        return latest, None
    except Exception as exc:
        return None, f"Failed to read LATEST.txt: {exc}"


def read_manifest(version):
    update_root = resolve_update_root()
    manifest_path = os.path.join(update_root, "releases", version, "version.json")
    if not os.path.exists(manifest_path):
        return None, f"version.json not found at {manifest_path}"
    try:
        with open(manifest_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data, None
    except Exception as exc:
        return None, f"Failed to read version.json: {exc}"


def find_updater(release_dir):
    update_root = resolve_update_root()
    candidates = [
        os.path.join(release_dir, "updater", "Updater.exe"),
        os.path.join(release_dir, "Updater.exe"),
        os.path.join(update_root, "Updater.exe"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def check_for_update(current_version):
    latest, err = read_latest_version()
    if err:
        return None, err

    manifest, err = read_manifest(latest)
    if err:
        return None, err

    manifest_version = manifest.get("version") or latest
    if not is_newer_version(manifest_version, current_version):
        return None, None

    update_root = resolve_update_root()
    release_dir = os.path.join(update_root, "releases", latest)
    return {
        "latest": latest,
        "version": manifest_version,
        "manifest": manifest,
        "release_dir": release_dir,
        "updater_path": find_updater(release_dir),
    }, None
