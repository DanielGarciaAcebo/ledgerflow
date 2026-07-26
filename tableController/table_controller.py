import tkinter as tk
from tkinter import ttk


def show_excel_data(
    table: ttk.Treeview,
    headers: list[str],
    rows: list[list[object]],
) -> None:
    table.delete(*table.get_children())

    table["columns"] = headers
    table["show"] = "headings"

    for header in headers:
        table.heading(header, text=header)
        table.column(
            header,
            width=140,
            minwidth=80,
            anchor="w",
        )

    for row in rows:
        formatted_row = [
            "" if value is None else value
            for value in row
        ]

        table.insert(
            "",
            tk.END,
            values=formatted_row,
        )