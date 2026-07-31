#!/usr/bin/env bash

set -euo pipefail

APP_ID="io.github.DanielGarciaAcebo.LedgerFlow"

INSTALL_DIR="$HOME/.local/opt/ledgerflow"

COMMAND_LINK="$HOME/.local/bin/ledgerflow"

DESKTOP_FILE="$HOME/.local/share/applications/$APP_ID.desktop"

ICON_FILE="$HOME/.local/share/icons/hicolor/scalable/apps/ledgerflow.svg"


rm -f "$COMMAND_LINK"

rm -f "$DESKTOP_FILE"

rm -f "$ICON_FILE"

rm -rf "$INSTALL_DIR"


if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database \
        "$HOME/.local/share/applications"
fi


printf 'LedgerFlow was removed from this user account.\n'