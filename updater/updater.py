import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    import ctypes
except Exception:
    ctypes = None


APP_NAME = "DocCompareAI"
LOG_PATH = Path(tempfile.gettempdir()) / f"{APP_NAME}_Updater.log"


def log(message):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    try:
        print(line)
    except Exception:
        pass


def show_message(title, text, kind="info"):
    if ctypes is None:
        log(f"{title}: {text}")
        return
    flags = 0x0
    if kind == "error":
        flags |= 0x10  # MB_ICONERROR
    elif kind == "warn":
        flags |= 0x30  # MB_ICONWARNING
    else:
        flags |= 0x40  # MB_ICONINFORMATION
    try:
        ctypes.windll.user32.MessageBoxW(None, text, title, flags)
    except Exception:
        log(f"{title}: {text}")


def read_manifest(release_dir):
    manifest_path = release_dir / "version.json"
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        log(f"Failed to read version.json: {exc}")
        return {}


def pick_package(release_dir, manifest):
    pkg = (manifest.get("package") or {}).get("path")
    if pkg:
        pkg_path = release_dir / pkg
        if pkg_path.exists():
            return pkg_path
    default = release_dir / "package.zip"
    return default if default.exists() else None


def pick_app_exe(install_dir, manifest):
    app_exe = manifest.get("app_exe") or f"{APP_NAME}.exe"
    exe_path = install_dir / app_exe
    if exe_path.exists():
        return exe_path
    fallback = install_dir / f"{APP_NAME}.exe"
    return fallback if fallback.exists() else None


def find_extracted_root(temp_dir):
    entries = [p for p in temp_dir.iterdir() if p.name not in (".", "..")]
    if len(entries) == 1 and entries[0].is_dir():
        return entries[0]
    doc_root = temp_dir / APP_NAME
    if doc_root.exists() and doc_root.is_dir():
        return doc_root
    return temp_dir


def copy_with_retry(src, dst, attempts=12, delay=0.5):
    last_exc = None
    for i in range(attempts):
        try:
            if dst.exists():
                try:
                    os.chmod(dst, 0o666)
                except Exception:
                    pass
                try:
                    dst.unlink()
                except Exception:
                    pass
            shutil.copy2(src, dst)
            return True
        except Exception as exc:
            last_exc = exc
            time.sleep(delay + (i * 0.2))
    if last_exc:
        raise last_exc
    return False


def copy_tree(src_root, dest_root):
    for root, _dirs, files in os.walk(src_root):
        rel = os.path.relpath(root, src_root)
        dest_dir = dest_root if rel == "." else dest_root / rel
        dest_dir.mkdir(parents=True, exist_ok=True)
        for fname in files:
            s = Path(root) / fname
            d = dest_dir / fname
            copy_with_retry(s, d)


def is_admin():
    if ctypes is None:
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _quote(arg):
    if not arg:
        return '""'
    if " " in arg or "\t" in arg or '"' in arg:
        return '"' + arg.replace('"', '\\"') + '"'
    return arg


def relaunch_as_admin(args):
    if ctypes is None:
        return False
    try:
        if getattr(sys, "frozen", False):
            exe = sys.executable
            params = " ".join(_quote(a) for a in args)
        else:
            exe = sys.executable
            script = str(Path(__file__).resolve())
            params = " ".join(_quote(a) for a in [script] + args)
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, params, None, 1)
        return result > 32
    except Exception as exc:
        log(f"Failed to elevate: {exc}")
        return False


def is_dir_writable(path):
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / f".__write_test_{os.getpid()}"
        with test_file.open("w", encoding="utf-8") as f:
            f.write("ok")
        test_file.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def main():
    if len(sys.argv) < 3:
        show_message("Updater", "Usage: Updater.exe <release_dir> <install_dir>", kind="error")
        return 2

    args = sys.argv[1:]
    elevated_flag = "--elevated"
    elevated = False
    if elevated_flag in args:
        args = [a for a in args if a != elevated_flag]
        elevated = True

    if len(args) < 2:
        show_message("Updater", "Usage: Updater.exe <release_dir> <install_dir>", kind="error")
        return 2

    release_dir = Path(args[0]).resolve()
    install_dir = Path(args[1]).resolve()

    log(f"Release dir: {release_dir}")
    log(f"Install dir: {install_dir}")

    if not release_dir.exists():
        show_message("Updater", f"Release folder not found:\n{release_dir}", kind="error")
        return 1

    if not is_dir_writable(install_dir):
        if not is_admin():
            if relaunch_as_admin([str(release_dir), str(install_dir), elevated_flag]):
                return 0
            show_message(
                "Updater",
                "Administrator permission is required to update this installation.\n"
                "Please run the updater as Administrator.",
                kind="warn",
            )
            return 1
        if elevated and not is_admin():
            show_message(
                "Updater",
                "Updater was launched without Administrator privileges.",
                kind="error",
            )
            return 1

    manifest = read_manifest(release_dir)
    package_path = pick_package(release_dir, manifest)
    if not package_path:
        show_message("Updater", "package.zip not found in release folder.", kind="error")
        return 1

    temp_dir = Path(tempfile.mkdtemp(prefix=f"{APP_NAME}_update_"))
    log(f"Temp dir: {temp_dir}")

    try:
        log(f"Extracting {package_path}...")
        shutil.unpack_archive(str(package_path), str(temp_dir))
        src_root = find_extracted_root(temp_dir)
        log(f"Extracted root: {src_root}")

        install_dir.mkdir(parents=True, exist_ok=True)
        log("Copying files...")
        copy_tree(src_root, install_dir)

        exe_path = pick_app_exe(install_dir, manifest)
        if exe_path:
            try:
                subprocess.Popen([str(exe_path)], cwd=str(install_dir))
            except Exception as exc:
                log(f"Failed to relaunch app: {exc}")
        show_message("Update Complete", "Application updated successfully.", kind="info")
        return 0
    except Exception as exc:
        log(f"Update failed: {exc}")
        show_message("Update Failed", f"Could not apply update.\n\n{exc}\n\nLog: {LOG_PATH}", kind="error")
        return 1
    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
