from services.automatic_classifier import parse_amount
from services.file_initializer import CLASSIFICATIONS_FILE

FIELD_SEPARATOR = "\t"
GROUP_SEPARATOR = " | "
MODE_SEPARATOR = "="

NORMAL_MODE = "NORMAL"
INVERTED_MODE = "INVERTED"


def get_amount_direction(amount: object) -> str:
    parsed_amount = parse_amount(amount)

    if parsed_amount is None:
        return "UNKNOWN"

    if parsed_amount < 0:
        return "DEBIT"

    if parsed_amount > 0:
        return "CREDIT"

    return "ZERO"


def get_classification_key(
    transaction_name: str,
    amount: object,
) -> tuple[str, str]:
    return (
        transaction_name.strip().casefold(),
        get_amount_direction(amount),
    )


def parse_group_assignments(
    assignments_text: str,
) -> dict[str, bool]:
    assignments: dict[str, bool] = {}

    for item in assignments_text.split(GROUP_SEPARATOR):
        item = item.strip()

        if not item:
            continue

        if MODE_SEPARATOR not in item:
            # Compatibilidad con el formato anterior.
            assignments[item] = False
            continue

        group_name, mode = item.rsplit(
            MODE_SEPARATOR,
            maxsplit=1,
        )

        group_name = group_name.strip()
        mode = mode.strip().upper()

        if group_name:
            assignments[group_name] = mode == INVERTED_MODE

    return assignments


def load_classifications() -> dict[
    tuple[str, str],
    tuple[str, dict[str, bool]],
]:
    if not CLASSIFICATIONS_FILE.exists():
        return {}

    classifications: dict[
        tuple[str, str],
        tuple[str, dict[str, bool]],
    ] = {}

    for line in CLASSIFICATIONS_FILE.read_text(
        encoding="utf-8",
    ).splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(
            FIELD_SEPARATOR,
            maxsplit=2,
        )

        if len(parts) != 3:
            continue

        name, direction, assignments_text = parts

        key = (
            name.strip().casefold(),
            direction.strip().upper(),
        )

        classifications[key] = (
            name.strip(),
            parse_group_assignments(assignments_text),
        )

    return classifications


def get_saved_group_assignments(
    transaction_name: str,
    amount: object,
) -> dict[str, bool]:
    classifications = load_classifications()

    record = classifications.get(
        get_classification_key(
            transaction_name,
            amount,
        )
    )

    if record is None:
        return {}

    _, assignments = record

    return assignments.copy()


def save_classification(
    transaction_name: str,
    amount: object,
    assignments: dict[str, bool],
) -> None:
    classifications = load_classifications()

    key = get_classification_key(
        transaction_name,
        amount,
    )

    clean_assignments = {
        group_name.strip(): bool(inverted)
        for group_name, inverted in assignments.items()
        if group_name.strip()
    }

    if clean_assignments:
        classifications[key] = (
            transaction_name.strip(),
            clean_assignments,
        )
    else:
        classifications.pop(key, None)

    lines = [
        "# LedgerFlow classifications",
        "# Name<TAB>Direction<TAB>Group=NORMAL|INVERTED",
    ]

    sorted_records = sorted(
        classifications.items(),
        key=lambda item: (
            item[1][0].casefold(),
            item[0][1],
        ),
    )

    for (_, direction), (name, stored_assignments) in sorted_records:
        assignments_text = GROUP_SEPARATOR.join(
            (
                f"{group_name}="
                f"{INVERTED_MODE if inverted else NORMAL_MODE}"
            )
            for group_name, inverted
            in stored_assignments.items()
        )

        lines.append(
            FIELD_SEPARATOR.join(
                [
                    name,
                    direction,
                    assignments_text,
                ]
            )
        )

    CLASSIFICATIONS_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )