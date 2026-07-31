from decimal import Decimal, InvalidOperation


DANIEL_TRANSFER_NAME = "trf.danielgarciaacebo"

SENT_TRANSFER_GROUP = "Sent Transfers"
RECEIVED_TRANSFER_GROUP = "Received Transfers"


def parse_amount(value: object) -> Decimal | None:
    if value is None:
        return None

    if isinstance(value, Decimal):
        return value

    if isinstance(value, int | float):
        return Decimal(str(value))

    normalized_value = (
        str(value)
        .strip()
        .replace("€", "")
        .replace(" ", "")
        .replace(",", ".")
    )

    try:
        return Decimal(normalized_value)
    except InvalidOperation:
        return None


def get_automatic_groups(
    transaction_name: str,
    amount: object,
) -> list[str]:
    normalized_name = transaction_name.strip().casefold()

    if not normalized_name.startswith(DANIEL_TRANSFER_NAME):
        return []

    parsed_amount = parse_amount(amount)

    if parsed_amount is None or parsed_amount == 0:
        return []

    if parsed_amount < 0:
        return SENT_TRANSFER_GROUP.copy()

    return RECEIVED_TRANSFER_GROUP.copy()