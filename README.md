# LedgerFlow

LedgerFlow is a local desktop application for organizing financial transactions from Excel files.

The application reads an Excel file, lets the user choose which columns contain the transaction name and amount, classifies each transaction into one or more custom groups, remembers previous classifications, and exports a new organized Excel file.

## Status

LedgerFlow is currently under active development.

The current version supports:

* Loading `.xlsx` files.
* Selecting the Excel header row.
* Selecting the transaction name column.
* Selecting the transaction amount column.
* Displaying the imported Excel data.
* Creating and deleting custom groups.
* Saving groups in `group.txt`.
* Classifying transactions into one or more groups.
* Assigning normal or inverted signs independently for each group.
* Saving classifications in `classification.txt`.
* Reusing saved classifications in future imports.
* Applying automatic classification rules.
* Normalizing transaction names such as Bizum operations.
* Exporting an organized Excel file.

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

* A fixed `Name` column.
* One column for each group stored in `group.txt`.
* The transaction amount in every assigned group column.
* The opposite amount sign when `Invert` is enabled for that group.

Example:

| Name        |   Food |  Income | Internal Transfer |
| ----------- | -----: | ------: | ----------------: |
| Supermarket | -42.50 |         |                   |
| Salary      |        | 1500.00 |          -1500.00 |

## Requirements

* Arch Linux
* Python 3
* Tkinter
* `openpyxl`

Install the system dependencies:

```bash
sudo pacman -S --needed python python-pip tk
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd ledgerflow
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python -m pip install openpyxl
```

Run the application:

```bash
python main.py
```

## Project structure

```text
ledgerflow/
├── main.py
├── group.txt
├── classification.txt
├── classificationController/
│   ├── __init__.py
│   ├── automatic_classifier.py
│   ├── classification_repository.py
│   └── classification_window.py
├── columnController/
│   ├── __init__.py
│   └── column_controller.py
├── exportController/
│   ├── __init__.py
│   └── excel_exporter.py
├── groupController/
│   ├── __init__.py
│   └── group_controller.py
├── normalizationController/
│   ├── __init__.py
│   └── name_normalizer.py
├── selectController/
│   ├── __init__.py
│   └── select_controller.py
├── tableController/
│   ├── __init__.py
│   └── table_controller.py
└── transactionController/
    ├── __init__.py
    └── transaction_controller.py
```

## Data files

### `group.txt`

Stores the available classification groups.

Use one group per line:

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

LedgerFlow can normalize transaction names before classification.

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
normalizationController/name_normalizer.py
```

## Automatic classification

Automatic rules can assign groups before the manual classification screen opens.

These rules are located in:

```text
classificationController/automatic_classifier.py
```

Manual saved classifications can override automatic values.

## Local-only operation

LedgerFlow runs entirely on the local computer.

It does not require:

* A server.
* An external database.
* An internet connection.
* A cloud account.

The imported financial files and classifications remain on the user's machine.

## Planned improvements

* Improve the final Excel formatting.
* Add a classification summary screen.
* Add editing for saved classifications.
* Add import validation and clearer error messages.
* Add support for additional Excel formats.
* Package LedgerFlow as a native Linux executable.
* Add a `.desktop` launcher for Linux application menus.
* Add automated tests.

## Development notes

Activate the virtual environment before working on the project:

```bash
source .venv/bin/activate
```

Exit the environment with:

```bash
deactivate
```

## License

No license has been selected yet.
