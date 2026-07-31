#!/usr/bin/env bash
set -euo pipefail

APP_NAME="LedgerFlow"
APP_COMMAND="ledgerflow"
APP_ID="io.github.DanielGarciaAcebo.LedgerFlow"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

DIST_DIR="$PROJECT_DIR/dist/$APP_NAME"
EXECUTABLE_SOURCE="$DIST_DIR/$APP_NAME"
SVG_SOURCE="$PROJECT_DIR/assets/ledgerflow.svg"

INSTALL_DIR="$HOME/.local/opt/ledgerflow"
BIN_DIR="$HOME/.local/bin"
APPLICATIONS_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"
DESKTOP_FILE="$APPLICATIONS_DIR/$APP_ID.desktop"

cd "$PROJECT_DIR"

if [[ ! -f "$PROJECT_DIR/LedgerFlow.spec" ]]; then
    printf 'Error: LedgerFlow.spec was not found in %s\n' "$PROJECT_DIR" >&2
    exit 1
fi

if [[ ! -f "$SVG_SOURCE" ]]; then
    printf 'Error: the SVG icon was not found at %s\n' "$SVG_SOURCE" >&2
    exit 1
fi

if [[ -x "$PROJECT_DIR/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
else
    PYTHON="python"
fi

printf 'Building %s...\n' "$APP_NAME"
"$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    "$PROJECT_DIR/LedgerFlow.spec"

if [[ ! -x "$EXECUTABLE_SOURCE" ]]; then
    printf 'Error: PyInstaller did not create %s\n' "$EXECUTABLE_SOURCE" >&2
    exit 1
fi

printf 'Installing application files...\n'
rm -rf "$INSTALL_DIR"

mkdir -p \
    "$INSTALL_DIR" \
    "$BIN_DIR" \
    "$APPLICATIONS_DIR" \
    "$ICON_DIR"

cp -a "$DIST_DIR/." "$INSTALL_DIR/"
ln -sfn "$INSTALL_DIR/$APP_NAME" "$BIN_DIR/$APP_COMMAND"

install -Dm644 \
    "$SVG_SOURCE" \
    "$ICON_DIR/ledgerflow.svg"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.5
Name=LedgerFlow
GenericName=Financial Excel Organizer
Comment=Organize and classify financial Excel transactions
Exec=$INSTALL_DIR/$APP_NAME
TryExec=$INSTALL_DIR/$APP_NAME
Icon=ledgerflow
Terminal=false
StartupNotify=true
Categories=Office;Finance;Utility;
Keywords=finance;excel;spreadsheet;ledger;transactions;
EOF

chmod 644 "$DESKTOP_FILE"

if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate "$DESKTOP_FILE"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPLICATIONS_DIR"
fi

printf '\n%s was installed successfully.\n' "$APP_NAME"
printf 'Executable: %s\n' "$INSTALL_DIR/$APP_NAME"
printf 'Launcher:   %s\n' "$DESKTOP_FILE"
printf 'Command:    %s\n' "$APP_COMMAND"
printf '\nClose and reopen Wofi, then search for "LedgerFlow".\n'