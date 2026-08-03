#!/usr/bin/env bash

set -euo pipefail

VERSION="${1:-1.0.0}"

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

PROJECT_DIR="$(
    cd "$SCRIPT_DIR/../.."
    pwd
)"

PACKAGE_NAME="ledgerflow"
SOURCE_NAME="$PACKAGE_NAME-$VERSION"

SOURCE_ROOT="$PROJECT_DIR/build/arch-source"
STAGE_DIR="$SOURCE_ROOT/$SOURCE_NAME"

SOURCE_ARCHIVE="$SCRIPT_DIR/$SOURCE_NAME.tar.gz"

RELEASE_DIR="$PROJECT_DIR/release"

PKGBUILD_FILE="$SCRIPT_DIR/PKGBUILD"

EXPECTED_PACKAGE="$SCRIPT_DIR/$PACKAGE_NAME-$VERSION-1-any.pkg.tar.zst"


required_paths=(
    "$PROJECT_DIR/main.py"
    "$PROJECT_DIR/README.md"
    "$PROJECT_DIR/assets/ledgerflow.svg"
    "$PROJECT_DIR/controllers"
    "$PROJECT_DIR/models"
    "$PROJECT_DIR/services"
    "$PROJECT_DIR/ui"
    "$PKGBUILD_FILE"
    "$SCRIPT_DIR/ledgerflow"
    "$SCRIPT_DIR/io.github.DanielGarciaAcebo.LedgerFlow.desktop"
)


for required_path in "${required_paths[@]}"; do
    if [[ ! -e "$required_path" ]]; then
        printf 'Error: required path not found: %s\n' \
            "$required_path" >&2

        exit 1
    fi
done


if ! command -v makepkg >/dev/null 2>&1; then
    printf 'Error: makepkg is not installed.\n' >&2
    printf 'Install base-devel first:\n' >&2
    printf 'sudo pacman -S --needed base-devel\n' >&2

    exit 1
fi


printf 'Preparing LedgerFlow %s source package...\n' \
    "$VERSION"


rm -rf "$SOURCE_ROOT"
rm -f "$SOURCE_ARCHIVE"

mkdir -p \
    "$STAGE_DIR" \
    "$RELEASE_DIR"


cp -a \
    "$PROJECT_DIR/main.py" \
    "$PROJECT_DIR/README.md" \
    "$PROJECT_DIR/controllers" \
    "$PROJECT_DIR/models" \
    "$PROJECT_DIR/services" \
    "$PROJECT_DIR/ui" \
    "$PROJECT_DIR/assets" \
    "$STAGE_DIR/"


# Remove generated Python files from the source package.
find "$STAGE_DIR" \
    -type d \
    -name "__pycache__" \
    -prune \
    -exec rm -rf {} +


find "$STAGE_DIR" \
    -type f \
    \( -name "*.pyc" -o -name "*.pyo" \) \
    -delete


# Update the version used by makepkg.
sed -i \
    "s/^pkgver=.*/pkgver=$VERSION/" \
    "$PKGBUILD_FILE"


# Create a reproducible source archive.
tar \
    --sort=name \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    -czf "$SOURCE_ARCHIVE" \
    -C "$SOURCE_ROOT" \
    "$SOURCE_NAME"


printf 'Building Arch Linux package...\n'


cd "$SCRIPT_DIR"


rm -rf \
    "$SCRIPT_DIR/src" \
    "$SCRIPT_DIR/pkg"


find "$SCRIPT_DIR" \
    -maxdepth 1 \
    -type f \
    -name "$PACKAGE_NAME-$VERSION-*.pkg.tar.zst" \
    -delete


makepkg \
    --syncdeps \
    --clean \
    --force


if [[ ! -f "$EXPECTED_PACKAGE" ]]; then
    printf 'Error: expected package was not generated:\n' >&2
    printf '%s\n' "$EXPECTED_PACKAGE" >&2

    exit 1
fi


cp -f \
    "$EXPECTED_PACKAGE" \
    "$RELEASE_DIR/"


makepkg --printsrcinfo > "$SCRIPT_DIR/.SRCINFO"


printf '\nArch package created successfully:\n'
printf '%s\n' \
    "$RELEASE_DIR/$(basename "$EXPECTED_PACKAGE")"