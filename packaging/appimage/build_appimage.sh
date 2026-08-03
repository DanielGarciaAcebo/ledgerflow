#!/usr/bin/env bash

set -euo pipefail

APP_NAME="LedgerFlow"
APP_ID="io.github.DanielGarciaAcebo.LedgerFlow"
VERSION="${1:-1.0.0}"

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

PROJECT_DIR="$(
    cd "$SCRIPT_DIR/../.."
    pwd
)"

SYSTEM_ARCH="$(uname -m)"

case "$SYSTEM_ARCH" in
    x86_64 | amd64)
        APPIMAGE_ARCH="x86_64"
        ;;

    aarch64 | arm64)
        APPIMAGE_ARCH="aarch64"
        ;;

    *)
        printf 'Error: unsupported architecture: %s\n' \
            "$SYSTEM_ARCH" >&2

        exit 1
        ;;
esac


DIST_DIR="$PROJECT_DIR/dist/$APP_NAME"

BUILD_ROOT="$PROJECT_DIR/build/appimage"
APPDIR="$BUILD_ROOT/$APP_NAME.AppDir"
TOOLS_DIR="$BUILD_ROOT/tools"

RELEASE_DIR="$PROJECT_DIR/release"

OUTPUT_FILE="$RELEASE_DIR/$APP_NAME-$VERSION-$APPIMAGE_ARCH.AppImage"

APPIMAGETOOL="$TOOLS_DIR/appimagetool-$APPIMAGE_ARCH.AppImage"

APPIMAGETOOL_URL="https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-$APPIMAGE_ARCH.AppImage"

ICON_SOURCE="$PROJECT_DIR/assets/ledgerflow.svg"

APPRUN_SOURCE="$SCRIPT_DIR/AppRun"

DESKTOP_SOURCE="$SCRIPT_DIR/$APP_ID.desktop"


# Use the project virtual environment when available.
if [[ -x "$PROJECT_DIR/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
else
    PYTHON="python"
fi


required_paths=(
    "$PROJECT_DIR/LedgerFlow.spec"
    "$ICON_SOURCE"
    "$APPRUN_SOURCE"
    "$DESKTOP_SOURCE"
)


for required_path in "${required_paths[@]}"; do
    if [[ ! -f "$required_path" ]]; then
        printf 'Error: required file not found: %s\n' \
            "$required_path" >&2

        exit 1
    fi
done


if ! command -v curl >/dev/null 2>&1; then
    printf 'Error: curl is required to download appimagetool.\n' >&2
    printf 'Install it with:\n' >&2
    printf 'sudo pacman -S --needed curl\n' >&2

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


if [[ ! -x "$DIST_DIR/$APP_NAME" ]]; then
    printf 'Error: PyInstaller executable not found:\n' >&2
    printf '%s\n' "$DIST_DIR/$APP_NAME" >&2

    exit 1
fi


printf 'Preparing AppDir...\n'


rm -rf "$APPDIR"


mkdir -p \
    "$APPDIR/usr/lib/ledgerflow" \
    "$APPDIR/usr/share/applications" \
    "$APPDIR/usr/share/icons/hicolor/scalable/apps" \
    "$TOOLS_DIR" \
    "$RELEASE_DIR"


# Copy the complete PyInstaller application.
cp -a \
    "$DIST_DIR/." \
    "$APPDIR/usr/lib/ledgerflow/"


# Install the AppImage entry point.
install -m 755 \
    "$APPRUN_SOURCE" \
    "$APPDIR/AppRun"


# Install the desktop file in the AppDir root.
install -m 644 \
    "$DESKTOP_SOURCE" \
    "$APPDIR/$APP_ID.desktop"


# Also include it in the standard applications directory.
install -m 644 \
    "$DESKTOP_SOURCE" \
    "$APPDIR/usr/share/applications/$APP_ID.desktop"


# Install the icon in the AppDir root.
install -m 644 \
    "$ICON_SOURCE" \
    "$APPDIR/ledgerflow.svg"


# Also include the icon in the standard icon directory.
install -m 644 \
    "$ICON_SOURCE" \
    "$APPDIR/usr/share/icons/hicolor/scalable/apps/ledgerflow.svg"


# AppImage launchers can use .DirIcon as the application icon.
ln -sfn \
    "ledgerflow.svg" \
    "$APPDIR/.DirIcon"


chmod +x \
    "$APPDIR/AppRun" \
    "$APPDIR/usr/lib/ledgerflow/$APP_NAME"


if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate \
        "$APPDIR/$APP_ID.desktop"
fi


# Download appimagetool only when it is not already available.
if [[ ! -x "$APPIMAGETOOL" ]]; then
    printf 'Downloading appimagetool...\n'

    TEMP_TOOL="$APPIMAGETOOL.download"

    rm -f "$TEMP_TOOL"

    curl \
        --fail \
        --location \
        --progress-bar \
        --output "$TEMP_TOOL" \
        "$APPIMAGETOOL_URL"

    chmod +x "$TEMP_TOOL"

    mv \
        "$TEMP_TOOL" \
        "$APPIMAGETOOL"
fi


printf 'Creating AppImage...\n'


rm -f "$OUTPUT_FILE"


# appimagetool is itself an AppImage. The extraction flag avoids requiring
# FUSE during the build process.
ARCH="$APPIMAGE_ARCH" \
    "$APPIMAGETOOL" \
    --appimage-extract-and-run \
    "$APPDIR" \
    "$OUTPUT_FILE"


if [[ ! -f "$OUTPUT_FILE" ]]; then
    printf 'Error: AppImage was not generated:\n' >&2
    printf '%s\n' "$OUTPUT_FILE" >&2

    exit 1
fi


chmod +x "$OUTPUT_FILE"


printf '\nAppImage created successfully:\n'
printf '%s\n' "$OUTPUT_FILE"

printf '\nRun it with:\n'
printf '"%s"\n' "$OUTPUT_FILE"