import tkinter as tk
from tkinter import messagebox

from appController.file_initializer import GROUPS_FILE

def load_groups() -> list[str]:
    if not GROUPS_FILE.exists():
        return []

    groups: list[str] = []
    normalized_groups: set[str] = set()

    for line in GROUPS_FILE.read_text(encoding="utf-8").splitlines():
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
    new_group_var: tk.StringVar,
    groups_listbox: tk.Listbox,
    groups: list[str],
) -> None:
    group_name = new_group_var.get().strip()

    if not group_name:
        messagebox.showwarning(
            title="Invalid Group",
            message="Enter a group name.",
        )
        return

    group_exists = any(
        existing_group.casefold() == group_name.casefold()
        for existing_group in groups
    )

    if group_exists:
        messagebox.showwarning(
            title="Group Already Exists",
            message=f'The group "{group_name}" already exists.',
        )
        return

    groups.append(group_name)
    save_groups(groups)

    groups_listbox.insert(tk.END, group_name)
    new_group_var.set("")


def delete_group(
    groups_listbox: tk.Listbox,
    groups: list[str],
) -> None:
    selected_indices = groups_listbox.curselection()

    if not selected_indices:
        messagebox.showwarning(
            title="No Group Selected",
            message="Select a group to delete.",
        )
        return

    selected_index = selected_indices[0]
    group_name = groups_listbox.get(selected_index)

    confirmed = messagebox.askyesno(
        title="Delete Group",
        message=f'Delete the group "{group_name}"?',
    )

    if not confirmed:
        return

    groups.pop(selected_index)
    groups_listbox.delete(selected_index)

    save_groups(groups)