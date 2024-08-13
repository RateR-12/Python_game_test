# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('sprites/chest', 'sprites/chest'), ('sprites/hit_points', 'sprites/hit_points'), ('sprites/idle', 'sprites/idle'), ('sprites/jungle tileset', 'sprites/jungle tileset'), ('sprites/run', 'sprites/run'), ('sounds', 'sounds'), ('Jungle Asset Pack/parallax background', 'Jungle Asset Pack/parallax background'), ('Jungle Asset Pack/Character/sprites', 'Jungle Asset Pack/Character/sprites')],
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
