# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['F:\\SteamLibrary\\steamapps\\common\\EARTH DEFENSE FORCE 6\\EDFModloaderHead\\EDF_ModloaderHead_B\\EarthDefenseForceModloaderHead.py'],
    pathex=[],
    binaries=[],
    datas=[('fonts/RobotoCondensed-Bold.TTF', 'fonts'), ('EDF_ModloaderHeadFunc.py', '.'), ('ConfigManifestUninstaller.py', '.'), ('ProgressTrackerPercent.exe', '.'), ('ImageResources.py', '.'), ('images/*', 'images'), ('Icon_256.ico', '.'), ('eggs.py', '.')],
    hiddenimports=['PIL', 'requests', 'tkinter.filedialog', 'shutil', 'watchdog', 'os'],
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
    name='EDF MML',
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
    version='version_info.txt',
    icon=['Icon_256.ico'],
)
