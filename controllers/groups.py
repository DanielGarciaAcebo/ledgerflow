from services.file_initializer import GROUPS_FILE


class GroupError(ValueError):
    """Base exception for group operations."""


class InvalidGroupNameError(GroupError):
    """Raised when a group name is empty or invalid."""


class GroupAlreadyExistsError(GroupError):
    """Raised when attempting to create a duplicate group."""


class GroupNotFoundError(GroupError):
    """Raised when attempting to delete a missing group."""


def load_groups() -> list[str]:
    if not GROUPS_FILE.exists():
        return []

    groups: list[str] = []
    normalized_groups: set[str] = set()

    for line in GROUPS_FILE.read_text(
        encoding="utf-8",
    ).splitlines():
        group_name = line.strip()

        if not group_name:
            continue

        normalized_name = group_name.casefold()

        if normalized_name in normalized_groups:
            continue

        normalized_groups.add(normalized_name)
        groups.append(group_name)

    return groups


def save_groups(groups: list[str]) -> None:
    content = "\n".join(groups)

    if content:
        content += "\n"

    GROUPS_FILE.write_text(
        content,
        encoding="utf-8",
    )


def create_group(
    group_name: str,
    groups: list[str],
) -> str:
    clean_name = group_name.strip()

    if not clean_name:
        raise InvalidGroupNameError(
            "Enter a group name."
        )

    group_exists = any(
        existing_group.casefold() == clean_name.casefold()
        for existing_group in groups
    )

    if group_exists:
        raise GroupAlreadyExistsError(
            f'The group "{clean_name}" already exists.'
        )

    groups.append(clean_name)
    save_groups(groups)

    return clean_name


def delete_group(
    group_name: str,
    groups: list[str],
) -> None:
    try:
        groups.remove(group_name)
    except ValueError as error:
        raise GroupNotFoundError(
            f'The group "{group_name}" does not exist.'
        ) from error

    save_groups(groups)