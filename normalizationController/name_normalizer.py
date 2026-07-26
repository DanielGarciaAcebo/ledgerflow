import re


def normalize_transaction_name(value: object) -> str:
    if value is None:
        return ""

    transaction_name = " ".join(
        str(value).strip().split()
    )

    if is_bizum_name(transaction_name):
        return normalize_bizum_name(transaction_name)

    return transaction_name


def is_bizum_name(transaction_name: str) -> bool:
    return bool(
        re.match(
            pattern=r"^(cargo|abono)\s+bizum\b",
            string=transaction_name,
            flags=re.IGNORECASE,
        )
    )


def normalize_bizum_name(transaction_name: str) -> str:
    bizum_match = re.match(
        pattern=r"^(cargo|abono)\s+bizum\b",
        string=transaction_name,
        flags=re.IGNORECASE,
    )

    if bizum_match is None:
        return transaction_name

    transaction_type = bizum_match.group(1).casefold()

    if transaction_type == "cargo":
        return "Cargo Bizum"

    return "Abono Bizum"