# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
a = Analysis(
    ['project.py'],
    pathex=[r"C:\Users\iad\OneDrive\Code\110814283\CS50P\project"],
    binaries=[],
    datas=[
        ('recipes.json', '.'),
        ('scrapy.cfg', '.'),
    ],
    hiddenimports=[
        'scrapy_selenium',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    a.binaries,
    a.datas,
    [],
    name='recipider',
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
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='recipider',
)