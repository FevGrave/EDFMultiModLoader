# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['F:\\SteamLibrary\\steamapps\\common\\EARTH DEFENSE FORCE 6\\EDF_ModloaderHead_B\\EarthDefenseForceModloaderHead.py'],
    pathex=[],
    binaries=[],
    datas=[('fonts/ARUDJINGXIHEIG30_BD.TTF', 'fonts'), ('EDF_ModloaderHeadFunc.py', '.'), ('ConfigManifestUninstaller.py', '.'), ('ImageResources.py', '.'), ('images/*', 'images'), ('Icon_256.ico', '.')],
    hiddenimports=['PIL', 'PIL._imaging', 'requests', 'threading', 'tkinter.filedialog', 'tkinter.messagebox', 'shutil', 'os', 'sys'],
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
    [],
    exclude_binaries=True,
    name='EDF MML',
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
    version='version_info.txt',
    icon=['Icon_256.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EDF MML',
)
