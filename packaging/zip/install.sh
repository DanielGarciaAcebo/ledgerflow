#!/usr/bin/env bash

set -euo pipefail

APP_NAME="LedgerFlow"
APP_COMMAND="ledgerflow"
APP_ID="io.github.DanielGarciaAcebo.LedgerFlow"

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

SOURCE_APP_DIR="$SCRIPT_DIR/app"
SOURCE_ICON="$SCRIPT_DIR/ledgerflow.svg"
SOURCE_UNINSTALLER="$SCRIPT_DIR/uninstall.sh"

INSTALL_DIR="$HOME/.local/opt/ledgerflow"
BIN_DIR="$HOME/.local/bin"

APPLICATIONS_DIR="$HOME/.local/share/applications"

ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"

EXECUTABLE="$INSTALL_DIR/$APP_NAME"
COMMAND_LINK="$BIN_DIR/$APP_COMMAND"

DESKTOP_FILE="$APPLICATIONS_DIR/$APP_ID.desktop"
ICON_FILE="$ICON_DIR/ledgerflow.svg"

INSTALLED_UNINSTALLER="$INSTALL_DIR/uninstall.sh"


# Verify package contents.
for required_path in \
    "$SOURCE_APP_DIR/$APP_NAME" \
    "$SOURCE_ICON" \
    "$SOURCE_UNINSTALLER"
do
    if [[ ! -e "$required_path" ]]; then
        printf 'Error: required package file not found: %s\n' \
            "$required_path" >&2

        exit 1
    fi
done


printf 'Installing %s for user %s...\n' \
    "$APP_NAME" \
    "$USER"


# Replace an existing installation.
rm -rf "$INSTALL_DIR"


mkdir -p \
    "$INSTALL_DIR" \
    "$BIN_DIR" \
    "$APPLICATIONS_DIR" \
    "$ICON_DIR"


# Copy the PyInstaller application.
cp -a \
    "$SOURCE_APP_DIR/." \
    "$INSTALL_DIR/"


# Keep an uninstaller inside the installed application.
install -m 755 \
    "$SOURCE_UNINSTALLER" \
    "$INSTALLED_UNINSTALLER"


# Create the terminal command:
#
# ledgerflow
#
ln -sfn \
    "$EXECUTABLE" \
    "$COMMAND_LINK"


# Install the application icon.
install -m 644 \
    "$SOURCE_ICON" \
    "$ICON_FILE"


# Create the application menu launcher.
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.5
Name=LedgerFlow
GenericName=Financial Excel Organizer
Comment=Organize and classify financial Excel transactions
Exec=$EXECUTABLE
TryExec=$EXECUTABLE
Icon=ledgerflow
Terminal=false
StartupNotify=true
Categories=Office;Finance;Utility;
Keywords=finance;excel;spreadsheet;ledger;transactions;
EOF


chmod 644 "$DESKTOP_FILE"


# Validate the desktop file when the tool is installed.
if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate "$DESKTOP_FILE"
fi


# Refresh the application database when available.
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPLICATIONS_DIR"
fi


printf '\n%s was installed successfully.\n' \
    "$APP_NAME"

printf 'Application: %s\n' \
    "$EXECUTABLE"

printf 'Command:     %s\n' \
    "$APP_COMMAND"

printf 'Uninstall:   %s\n' \
    "$INSTALLED_UNINSTALLER"

printf '\nOpen the application menu and search for LedgerFlow.\n'