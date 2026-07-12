# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['laserdaq.py'],
    pathex=[],
    binaries=[],
    datas=[('laser_characterization_V1.ui', '.'),],
    hiddenimports=['PyQt5.QtPrintSupport',
    'PyQt5.QtSvg',],
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
    name='LaserDAQ',
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
    name='LaserDAQ',
)
