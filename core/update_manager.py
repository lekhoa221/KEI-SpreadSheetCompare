import json
import os
import re

REMOTE_ROOT = os.environ.get(
    "SSC_UPDATE_ROOT",
    r"\\10.1.3.2\KEIToolsData\SpreadSheetCompare",
)

LATEST_FILE = os.path.join(REMOTE_ROOT, "LATEST.txt")


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
    if not os.path.exists(LATEST_FILE):
        return None, f"LATEST.txt not found at {LATEST_FILE}"
    try:
        with open(LATEST_FILE, "r", encoding="utf-8-sig") as f:
            latest = (f.read() or "").strip()
        if not latest:
            return None, "LATEST.txt is empty"
        return latest, None
    except Exception as exc:
        return None, f"Failed to read LATEST.txt: {exc}"


def read_manifest(version):
    manifest_path = os.path.join(REMOTE_ROOT, "releases", version, "version.json")
    if not os.path.exists(manifest_path):
        return None, f"version.json not found at {manifest_path}"
    try:
        with open(manifest_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data, None
    except Exception as exc:
        return None, f"Failed to read version.json: {exc}"


def find_updater(release_dir):
    candidates = [
        os.path.join(release_dir, "updater", "Updater.exe"),
        os.path.join(release_dir, "Updater.exe"),
        os.path.join(REMOTE_ROOT, "Updater.exe"),
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

    release_dir = os.path.join(REMOTE_ROOT, "releases", latest)
    return {
        "latest": latest,
        "version": manifest_version,
        "manifest": manifest,
        "release_dir": release_dir,
        "updater_path": find_updater(release_dir),
    }, None
