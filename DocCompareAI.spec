# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import copy_metadata

datas = [('ui/assets', 'ui/assets')]
datas += copy_metadata('pytz')
datas += copy_metadata('pandas')

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pandas', 'pytz', 'openpyxl', 'qdarktheme', 'PyQt6.QtSvg', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'torchaudio', 'paddle', 'paddleocr', 'easyocr', 'cv2', 'opencv', 'transformers', 'onnxruntime', 'bitsandbytes', 'scipy', 'sklearn', 'sentencepiece'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DocCompareAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DocCompareAI',
)
