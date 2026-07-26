import tkinter as tk
from tkinter import messagebox, ttk


def configure_column_selectors(
    headers: list[str],
    name_selector: ttk.Combobox,
    amount_selector: ttk.Combobox,
    name_var: tk.StringVar,
    amount_var: tk.StringVar,
) -> None:
    name_selector["values"] = headers
    amount_selector["values"] = headers

    name_selector.config(state="readonly")
    amount_selector.config(state="readonly")

    name_var.set("")
    amount_var.set("")


def get_selected_columns(
    name_var: tk.StringVar,
    amount_var: tk.StringVar,
) -> tuple[str, str] | None:
    name_column = name_var.get().strip()
    amount_column = amount_var.get().strip()

    if not name_column:
        messagebox.showwarning(
            title="Missing Name Column",
            message="Select the column containing the transaction name.",
        )
        return None

    if not amount_column:
        messagebox.showwarning(
            title="Missing Amount Column",
            message="Select the column containing the transaction amount.",
        )
        return None

    if name_column == amount_column:
        messagebox.showwarning(
            title="Invalid Column Selection",
            message="Name and amount columns must be different.",
        )
        return None

    return name_column, amount_column