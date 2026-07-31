class ColumnSelectionError(ValueError):
    """Base exception for column selection errors."""


class MissingNameColumnError(ColumnSelectionError):
    """Raised when the name column is not selected."""


class MissingAmountColumnError(ColumnSelectionError):
    """Raised when the amount column is not selected."""


class SameColumnSelectionError(ColumnSelectionError):
    """Raised when both selections reference the same column."""


class ColumnNotFoundError(ColumnSelectionError):
    """Raised when a selected column is not available."""


def validate_column_selection(
    name_column: str,
    amount_column: str,
    available_headers: list[str],
) -> tuple[str, str]:
    clean_name_column = name_column.strip()
    clean_amount_column = amount_column.strip()

    if not clean_name_column:
        raise MissingNameColumnError(
            "Select the column containing the transaction name."
        )

    if not clean_amount_column:
        raise MissingAmountColumnError(
            "Select the column containing the transaction amount."
        )

    if clean_name_column == clean_amount_column:
        raise SameColumnSelectionError(
            "Name and amount columns must be different."
        )

    if clean_name_column not in available_headers:
        raise ColumnNotFoundError(
            f'The column "{clean_name_column}" is not available.'
        )

    if clean_amount_column not in available_headers:
        raise ColumnNotFoundError(
            f'The column "{clean_amount_column}" is not available.'
        )

    return clean_name_column, clean_amount_column