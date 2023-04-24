# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['jadeApps.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [
    ('jadeapps/main.ui','./ui/jadeapps/main.ui', "DATA"),
	('nfoert_example/main.ui','./ui/nfoert_example/main.ui', "DATA"),
    ('keys.txt','./keys.txt', "DATA"),
    ('jadeapps_quickgoogle/main.ui','./ui/jadeapps_quickgoogle/main.ui', "DATA"),
    ('jadeapps_spotifyremotecontrol/main.ui','./ui/jadeapps_spotifyremotecontrol/main.ui', "DATA"),
    ('jadeapps_weather/main.ui','./ui/jadeapps_weather/main.ui', "DATA")
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Jade Apps',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="favicon.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
