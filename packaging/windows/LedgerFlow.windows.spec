# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


PROJECT_DIRECTORY = (
    Path(SPECPATH)
    .resolve()
    .parents[1]
)

WINDOWS_BUILD_DIRECTORY = (
    PROJECT_DIRECTORY
    / "build"
    / "windows"
)

ICON_FILE = (
    WINDOWS_BUILD_DIRECTORY
    / "ledgerflow.ico"
)

VERSION_FILE = (
    WINDOWS_BUILD_DIRECTORY
    / "version_info.txt"
)


analysis = Analysis(
    [
        str(
            PROJECT_DIRECTORY
            / "main.py"
        ),
    ],
    pathex=[
        str(PROJECT_DIRECTORY),
    ],
    binaries=[],
    datas=[
        (
            str(
                PROJECT_DIRECTORY
                / "assets"
            ),
            "assets",
        ),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)


python_archive = PYZ(
    analysis.pure,
)


executable = EXE(
    python_archive,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="LedgerFlow",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_FILE),
    version=str(VERSION_FILE),
)


collection = COLLECT(
    executable,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="LedgerFlow",
)