# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['F:\\SteamLibrary\\steamapps\\common\\EARTH DEFENSE FORCE 6\\EDFModloaderHead\\EDF_ModloaderHead_B\\ProgressTrackerPercent.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['os'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ProgressTrackerPercent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='ptp_version_info.txt',
)
