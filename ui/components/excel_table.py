import tkinter as tk
from tkinter import ttk


DEFAULT_COLUMN_WIDTH = 140
MINIMUM_COLUMN_WIDTH = 80


class ExcelTable(ttk.LabelFrame):
    def __init__(
        self,
        parent: tk.Misc,
    ) -> None:
        super().__init__(
            parent,
            text="Excel Data",
            padding=10,
        )

        self.columnconfigure(
            0,
            weight=1,
        )
        self.rowconfigure(
            0,
            weight=1,
        )

        self.tree = ttk.Treeview(
            self,
            show="headings",
            height=12,
        )

        vertical_scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview,
        )

        horizontal_scrollbar = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.tree.xview,
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set,
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew",
        )

    def show_data(
        self,
        headers: list[str],
        rows: list[list[object]],
    ) -> None:
        self.clear()

        column_ids = [
            f"column_{index}"
            for index in range(len(headers))
        ]

        self.tree.configure(
            columns=column_ids,
            show="headings",
        )

        for column_id, header in zip(
            column_ids,
            headers,
            strict=True,
        ):
            self.tree.heading(
                column_id,
                text=header,
            )

            self.tree.column(
                column_id,
                width=DEFAULT_COLUMN_WIDTH,
                minwidth=MINIMUM_COLUMN_WIDTH,
                anchor="w",
            )

        for row in rows:
            formatted_row = self._format_row(
                row,
                len(headers),
            )

            self.tree.insert(
                "",
                tk.END,
                values=formatted_row,
            )

    def clear(self) -> None:
        children = self.tree.get_children()

        if children:
            self.tree.delete(*children)

        self.tree.configure(
            columns=(),
        )

    @staticmethod
    def _format_row(
        row: list[object],
        column_count: int,
    ) -> list[object]:
        formatted_row = [
            "" if value is None else value
            for value in row[:column_count]
        ]

        missing_values = (
            column_count - len(formatted_row)
        )

        if missing_values > 0:
            formatted_row.extend(
                [""] * missing_values,
            )

        return formatted_row