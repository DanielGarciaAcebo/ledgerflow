#!/usr/bin/env bash
set -euo pipefail

APP_ID="io.github.DanielGarciaAcebo.LedgerFlow"

INSTALL_DIR="$HOME/.local/opt/ledgerflow"
COMMAND_FILE="$HOME/.local/bin/ledgerflow"
DESKTOP_FILE="$HOME/.local/share/applications/$APP_ID.desktop"
ICON_FILE="$HOME/.local/share/icons/hicolor/scalable/apps/ledgerflow.svg"

rm -rf "$INSTALL_DIR"
rm -f "$COMMAND_FILE"
rm -f "$DESKTOP_FILE"
rm -f "$ICON_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME/.local/share/applications"
fi

printf 'LedgerFlow was removed from this user account.\n'
