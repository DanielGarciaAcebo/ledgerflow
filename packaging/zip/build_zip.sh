#!/usr/bin/env bash

set -euo pipefail

APP_NAME="LedgerFlow"
VERSION="${1:-1.0.0}"

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

PROJECT_DIR="$(
    cd "$SCRIPT_DIR/../.."
    pwd
)"

ARCH="$(uname -m)"

PACKAGE_NAME="${APP_NAME}-${VERSION}-linux-${ARCH}"

PYINSTALLER_OUTPUT="$PROJECT_DIR/dist/$APP_NAME"

BUILD_ROOT="$PROJECT_DIR/build/zip-package"
STAGE_DIR="$BUILD_ROOT/$PACKAGE_NAME"

RELEASE_DIR="$PROJECT_DIR/release"
ARCHIVE_PATH="$RELEASE_DIR/$PACKAGE_NAME.zip"

ICON_SOURCE="$PROJECT_DIR/assets/ledgerflow.svg"
INSTALLER_SOURCE="$SCRIPT_DIR/install.sh"
UNINSTALLER_SOURCE="$SCRIPT_DIR/uninstall.sh"
README_SOURCE="$SCRIPT_DIR/README.txt"


# Use the project virtual environment when available.
if [[ -x "$PROJECT_DIR/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
else
    PYTHON="python"
fi


# Verify required files.
for required_file in \
    "$PROJECT_DIR/LedgerFlow.spec" \
    "$ICON_SOURCE" \
    "$INSTALLER_SOURCE" \
    "$UNINSTALLER_SOURCE" \
    "$README_SOURCE"
do
    if [[ ! -f "$required_file" ]]; then
        printf 'Error: required file not found: %s\n' \
            "$required_file" >&2

        exit 1
    fi
done


# bsdtar is used to create the ZIP archive.
if ! command -v bsdtar >/dev/null 2>&1; then
    printf 'Error: bsdtar is required.\n' >&2
    printf 'Install it on Arch with:\n' >&2
    printf 'sudo pacman -S libarchive\n' >&2

    exit 1
fi


cd "$PROJECT_DIR"

printf 'Building %s %s with PyInstaller...\n' \
    "$APP_NAME" \
    "$VERSION"


"$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    "$PROJECT_DIR/LedgerFlow.spec"


if [[ ! -x "$PYINSTALLER_OUTPUT/$APP_NAME" ]]; then
    printf 'Error: executable not found: %s\n' \
        "$PYINSTALLER_OUTPUT/$APP_NAME" >&2

    exit 1
fi


printf 'Preparing ZIP package...\n'


# Remove the previous temporary package.
rm -rf "$BUILD_ROOT"


mkdir -p \
    "$STAGE_DIR/app" \
    "$RELEASE_DIR"


# Copy the complete PyInstaller application.
cp -a \
    "$PYINSTALLER_OUTPUT/." \
    "$STAGE_DIR/app/"


# Copy package resources.
install -m 644 \
    "$ICON_SOURCE" \
    "$STAGE_DIR/ledgerflow.svg"


install -m 755 \
    "$INSTALLER_SOURCE" \
    "$STAGE_DIR/install.sh"


install -m 755 \
    "$UNINSTALLER_SOURCE" \
    "$STAGE_DIR/uninstall.sh"


install -m 644 \
    "$README_SOURCE" \
    "$STAGE_DIR/README.txt"


# Remove an older ZIP with the same version.
rm -f "$ARCHIVE_PATH"


# Create the ZIP while preserving the top-level package directory.
(
    cd "$BUILD_ROOT"

    bsdtar \
        -a \
        -cf "$ARCHIVE_PATH" \
        "$PACKAGE_NAME"
)


printf '\nZIP package created successfully:\n'
printf '%s\n' "$ARCHIVE_PATH"