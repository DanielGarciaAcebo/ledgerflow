from dataclasses import dataclass, field

from classificationController.automatic_classifier import (
    get_automatic_groups,
)
from classificationController.classification_repository import (
    get_saved_group_assignments,
)
from normalizationController.name_normalizer import (
    normalize_transaction_name,
)



@dataclass(slots=True)
class Transaction:
    name: str
    amount: object
    group_assignments: dict[str, bool] = field(
        default_factory=dict
    )

def build_transactions(
    headers: list[str],
    rows: list[list[object]],
    name_column: str,
    amount_column: str,
) -> list[Transaction]:
    try:
        name_index = headers.index(name_column)
        amount_index = headers.index(amount_column)

    except ValueError as error:
        raise ValueError(
            "The selected columns were not found in the Excel file."
        ) from error

    transactions: list[Transaction] = []

    for row in rows:
        name_value = (
            row[name_index]
            if name_index < len(row)
            else None
        )

        amount_value = (
            row[amount_index]
            if amount_index < len(row)
            else None
        )

        if name_value is None and amount_value is None:
            continue

        normalized_name = normalize_transaction_name(
            name_value,
        )

        automatic_assignments = {
            group_name: False
            for group_name in get_automatic_groups(
                normalized_name,
                amount_value,
            )
        }

        saved_assignments = get_saved_group_assignments(
            normalized_name,
            amount_value,
        )

        combined_assignments = {
            **automatic_assignments,
            **saved_assignments,
        }

        transaction = Transaction(
            name=normalized_name,
            amount=amount_value,
            group_assignments=combined_assignments,
        )

        transactions.append(transaction)

    return transactions