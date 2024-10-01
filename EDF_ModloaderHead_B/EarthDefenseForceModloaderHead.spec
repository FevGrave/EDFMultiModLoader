# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['EarthDefenseForceModloaderHead.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('EDF_ModloaderHeadFunc.py', '.'), 
        ('ConfigManifestUninstaller.py', '.'), 
        ('ImageResources.py', '.'), 
        ('images/*', 'images'),
        ('Icon_256.ico', '.')
    ],
    hiddenimports=[],
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
    name='EDF: MML',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EDF: MML',
)
