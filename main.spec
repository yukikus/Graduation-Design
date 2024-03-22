# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['book.py', 'bookShow.py', 'classfiy_dialog.py', 'CommonHelper.py', 'convert.py', 'mainView.py', 'ncxHandler.py', 'resources.py'],
    binaries=[],
    datas=[],
    hiddenimports=['book.py', 'bookShow.py', 'classfiy_dialog.py', 'CommonHelper.py', 'convert.py', 'mainView.py', 'ncxHandler.py', 'resources.py'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
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
    icon=['logo50.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='E-book Reader',
)
