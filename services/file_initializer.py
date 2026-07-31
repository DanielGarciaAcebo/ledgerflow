from pathlib import Path

from platformdirs import user_data_path


APP_NAME = "LedgerFlow"

APP_DATA_DIRECTORY: Path = user_data_path(
    APP_NAME,
    appauthor=False,
    ensure_exists=True,
)

GROUPS_FILE = APP_DATA_DIRECTORY / "group.txt"
CLASSIFICATIONS_FILE = APP_DATA_DIRECTORY / "classification.txt"


def ensure_required_files() -> None:
    GROUPS_FILE.touch(exist_ok=True)

    if CLASSIFICATIONS_FILE.exists():
        return

    CLASSIFICATIONS_FILE.write_text(
        (
            "# LedgerFlow classifications\n"
            "# Name<TAB>Direction<TAB>"
            "Group=NORMAL | Another Group=INVERTED\n"
        ),
        encoding="utf-8",
    )