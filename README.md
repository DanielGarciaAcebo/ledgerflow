# LedgerFlow

LedgerFlow is a local desktop application for organizing and classifying financial transactions imported from Excel files.

The application reads an Excel workbook, lets the user select the transaction name and amount columns, classifies each transaction into one or more custom groups, remembers previous classifications, and exports a new organized Excel file.

## Download

### Windows portable

Download the portable Windows build:

[Download LedgerFlow 1.0.0 for Windows](https://github.com/DanielGarciaAcebo/ledgerflow/releases/download/v1.0.0/LedgerFlow-1.0.0-windows-x86_64.zip)

This version does not require installation.

1. Download the ZIP.
2. Extract the complete archive.
3. Open the extracted directory.
4. Double-click `LedgerFlow.exe`.

Do not move `LedgerFlow.exe` outside the extracted directory. The `_internal` directory contains required application files.

LedgerFlow stores its application data locally, normally in:

```text
%LOCALAPPDATA%\LedgerFlow
```

To remove the portable version, delete the extracted directory. Personal application data is not deleted automatically.

### AppImage

Download the portable AppImage:

[Download LedgerFlow 1.0.0 AppImage](https://github.com/DanielGarciaAcebo/ledgerflow/releases/download/v1.0.0/LedgerFlow-1.0.0-x86_64.AppImage)

Give the file execution permission:

```bash
chmod +x LedgerFlow-1.0.0-x86_64.AppImage
```

Run it:

```bash
./LedgerFlow-1.0.0-x86_64.AppImage
```

If FUSE is unavailable:

```bash
./LedgerFlow-1.0.0-x86_64.AppImage --appimage-extract-and-run
```

The AppImage does not require installation or administrator permissions.

### Generic Linux ZIP

Download the packaged Linux version:

[Download LedgerFlow 1.0.0 for Linux](https://github.com/DanielGarciaAcebo/ledgerflow/releases/download/v1.0.0/LedgerFlow-1.0.0-linux-x86_64.zip)

After downloading the ZIP:

```bash
bsdtar -xf LedgerFlow-1.0.0-linux-x86_64.zip
cd LedgerFlow-1.0.0-linux-x86_64
bash install.sh
```

Administrator permissions are not required.

LedgerFlow will be installed for the current user in:

```text
~/.local/opt/ledgerflow/
```

After installation, open the application menu and search for:

```text
LedgerFlow
```

You can also run it from a terminal:

```bash
ledgerflow
```

To uninstall it:

```bash
~/.local/opt/ledgerflow/uninstall.sh
```

### Arch Linux package

Arch Linux users can download the native package:

[Download LedgerFlow 1.0.0 for Arch Linux](https://github.com/DanielGarciaAcebo/ledgerflow/releases/download/v1.0.0/ledgerflow-1.0.0-1-any.pkg.tar.zst)

Install it with:

```bash
sudo pacman -U ledgerflow-1.0.0-1-any.pkg.tar.zst
```

The package installs LedgerFlow system-wide and lets `pacman` manage the application and its dependencies.

To uninstall it:

```bash
sudo pacman -Rns ledgerflow
```

You can view all published versions on the [LedgerFlow releases page](https://github.com/DanielGarciaAcebo/ledgerflow/releases).

## Status

LedgerFlow 1.0.0 supports:

- Loading `.xlsx` files.
- Selecting the Excel header row.
- Selecting the transaction name column.
- Selecting the transaction amount column.
- Displaying imported Excel data.
- Creating and deleting custom groups.
- Classifying transactions into one or more groups.
- Assigning normal or inverted signs independently for each group.
- Saving previous classifications.
- Reusing saved classifications in future imports.
- Applying automatic classification rules.
- Normalizing transaction names such as Bizum operations.
- Exporting an organized Excel file.
- Installing LedgerFlow as a desktop application on Linux.
- Displaying LedgerFlow in Linux application menus.
- Running LedgerFlow through the `ledgerflow` terminal command.
- Installing LedgerFlow through a native Arch Linux package.
- Running LedgerFlow as a portable AppImage.
- Running LedgerFlow as a portable Windows application.

## How it works

The basic workflow is:

1. Open LedgerFlow.
2. Select an Excel file.
3. Choose the header row.
4. Select the column containing the transaction name.
5. Select the column containing the transaction amount.
6. Start the classification process.
7. Assign each transaction to one or more groups.
8. Optionally invert the amount sign for specific groups.
9. Export the organized Excel file.

The exported file contains:

- A fixed `Name` column.
- One column for each configured group.
- The transaction amount in every assigned group column.
- The opposite amount sign when `Invert` is enabled for that group.

Example:

| Name | Food | Income | Internal Transfer |
| --- | ---: | ---: | ---: |
| Supermarket | -42.50 | | |
| Salary | | 1500.00 | -1500.00 |

## Installing from source

### Requirements

- Linux.
- Python 3.
- Tkinter.
- `openpyxl`.
- `platformdirs`.

Install the system dependencies on Arch Linux:

```bash
sudo pacman -S --needed python python-pip tk
```

Clone the repository:

```bash
git clone https://github.com/DanielGarciaAcebo/ledgerflow.git
cd ledgerflow
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Local development installation

LedgerFlow can be built and installed locally for the current Linux user:

```bash
chmod +x scripts/install_arch.sh
./scripts/install_arch.sh
```

This installs the application in:

```text
~/.local/opt/ledgerflow/
```

It also creates:

```text
~/.local/bin/ledgerflow
~/.local/share/applications/io.github.DanielGarciaAcebo.LedgerFlow.desktop
~/.local/share/icons/hicolor/scalable/apps/ledgerflow.svg
```

To remove the local installation:

```bash
./scripts/uninstall_arch.sh
```

## Building the distributable ZIP

Give the packaging scripts execution permission:

```bash
chmod +x packaging/zip/build_zip.sh
chmod +x packaging/zip/install.sh
chmod +x packaging/zip/uninstall.sh
```

Build version `1.0.0`:

```bash
./packaging/zip/build_zip.sh 1.0.0
```

The generated package will be located at:

```text
release/LedgerFlow-1.0.0-linux-x86_64.zip
```

## Building the Arch Linux package

Install the package-building tools:

```bash
sudo pacman -S --needed base-devel
```

Give the scripts execution permission:

```bash
chmod +x packaging/arch/build_pkg.sh
chmod +x packaging/arch/ledgerflow
```

Build version `1.0.0`:

```bash
./packaging/arch/build_pkg.sh 1.0.0
```

Do not run the build script with `sudo`.

The generated package will be located at:

```text
release/ledgerflow-1.0.0-1-any.pkg.tar.zst
```

Inspect the package:

```bash
pacman -Qip release/ledgerflow-1.0.0-1-any.pkg.tar.zst
pacman -Qlp release/ledgerflow-1.0.0-1-any.pkg.tar.zst
```

Install it:

```bash
sudo pacman -U release/ledgerflow-1.0.0-1-any.pkg.tar.zst
```

## Building the AppImage

Give the AppImage scripts execution permission:

```bash
chmod +x packaging/appimage/AppRun
chmod +x packaging/appimage/build_appimage.sh
```

Build version `1.0.0`:

```bash
./packaging/appimage/build_appimage.sh 1.0.0
```

Do not run the build script with `sudo`.

The generated AppImage will be located at:

```text
release/LedgerFlow-1.0.0-x86_64.AppImage
```

Run it:

```bash
./release/LedgerFlow-1.0.0-x86_64.AppImage
```

If FUSE is unavailable:

```bash
./release/LedgerFlow-1.0.0-x86_64.AppImage \
    --appimage-extract-and-run
```

## Building the Windows portable package

The Windows package is built on a Windows runner through GitHub Actions.

The workflow is located at:

```text
.github/workflows/build-windows.yml
```

To create the package:

1. Push the Windows packaging files and workflow to GitHub.
2. Open the repository's **Actions** tab.
3. Select **Build Windows portable**.
4. Select **Run workflow**.
5. Enter version `1.0.0`.
6. Open the completed workflow execution.
7. Download the generated artifact.

The generated file is:

```text
LedgerFlow-1.0.0-windows-x86_64.zip
```

The archive contains `LedgerFlow.exe`, its `_internal` dependencies, and a portable usage guide.

## Project structure

```text
ledgerflow/
├── .github/
│   └── workflows/
│       └── build-windows.yml
├── assets/
│   ├── ledgerflow.png
│   └── ledgerflow.svg
├── controllers/
│   ├── __init__.py
│   ├── columns.py
│   ├── groups.py
│   └── transactions.py
├── models/
│   ├── __init__.py
│   ├── excel_data.py
│   └── transaction.py
├── packaging/
│   ├── appimage/
│   │   ├── AppRun
│   │   ├── build_appimage.sh
│   │   └── io.github.DanielGarciaAcebo.LedgerFlow.desktop
│   ├── arch/
│   │   ├── PKGBUILD
│   │   ├── build_pkg.sh
│   │   ├── ledgerflow
│   │   └── io.github.DanielGarciaAcebo.LedgerFlow.desktop
│   ├── windows/
│   │   ├── requirements.txt
│   │   ├── create_icon.py
│   │   ├── LedgerFlow.windows.spec
│   │   └── build_windows.ps1
│   └── zip/
│       ├── build_zip.sh
│       ├── install.sh
│       ├── uninstall.sh
│       └── README.txt
├── scripts/
│   ├── install_arch.sh
│   └── uninstall_arch.sh
├── services/
│   ├── __init__.py
│   ├── automatic_classifier.py
│   ├── classification_repository.py
│   ├── excel_exporter.py
│   ├── excel_reader.py
│   ├── file_initializer.py
│   └── name_normalizer.py
├── ui/
│   ├── components/
│   │   ├── __init__.py
│   │   └── excel_table.py
│   ├── __init__.py
│   ├── classification_window.py
│   └── main_window.py
├── .gitignore
├── LedgerFlow.spec
├── main.py
├── README.md
└── requirements.txt
```

The following directories and files are generated automatically and are not committed:

```text
build/
dist/
release/
packaging/arch/src/
packaging/arch/pkg/
packaging/arch/*.tar.gz
packaging/arch/*.pkg.tar.zst
packaging/arch/.SRCINFO
*.AppImage
```

## Application data

LedgerFlow stores mutable application data in the current user's application data directory.

On Linux, this will normally be:

```text
~/.local/share/LedgerFlow/
```

On Windows, this will normally be:

```text
%LOCALAPPDATA%\LedgerFlow
```

The main application data files are:

```text
group.txt
classification.txt
```

These files are created automatically when required.

### `group.txt`

Stores the available classification groups.

Each group is stored on a separate line:

```text
Food
Transport
Income
Subscriptions
Internal Transfer
```

Group names are treated as case-insensitive when checking for duplicates.

### `classification.txt`

Stores remembered classifications.

The current format is:

```text
Transaction name<TAB>Direction<TAB>Group=NORMAL | Another Group=INVERTED
```

Example:

```text
Mercadona	DEBIT	Food=NORMAL
Salary	CREDIT	Income=NORMAL | Internal Transfer=INVERTED
```

This file is generated and updated automatically by LedgerFlow.

## Name normalization

LedgerFlow normalizes certain transaction names before classification.

For example:

```text
Cargo Bizum - Dinner
Cargo Bizum - Gift
```

Both can be normalized to:

```text
Cargo Bizum
```

Likewise:

```text
Abono Bizum - No concept
```

can be normalized to:

```text
Abono Bizum
```

Additional normalization rules can be added in:

```text
services/name_normalizer.py
```

## Automatic classification

Automatic rules can assign groups before the manual classification window opens.

These rules are located in:

```text
services/automatic_classifier.py
```

Saved manual classifications can override automatically assigned values.

## Local-only operation

LedgerFlow runs entirely on the local computer.

It does not require:

- A server.
- An external database.
- An internet connection.
- A cloud account.

Imported financial files and saved classifications remain on the user's computer.

## Development notes

Activate the virtual environment before working on the Linux version:

```bash
source .venv/bin/activate
```

Exit the environment with:

```bash
deactivate
```

Build and reinstall the local development version:

```bash
./scripts/install_arch.sh
```

Build the distributable Linux ZIP:

```bash
./packaging/zip/build_zip.sh 1.0.0
```

Build the native Arch package:

```bash
./packaging/arch/build_pkg.sh 1.0.0
```

Build the AppImage:

```bash
./packaging/appimage/build_appimage.sh 1.0.0
```

The Windows package is generated through the **Build Windows portable** GitHub Actions workflow.

## License

No license has been selected yet.
