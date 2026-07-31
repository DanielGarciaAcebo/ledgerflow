from pathlib import Path
import tkinter as tk
from tkinter import ttk

from controllers.columns import (
    configure_column_selectors,
    get_selected_columns,
)
from controllers.groups import (
    create_group,
    delete_group,
    load_groups,
)
from controllers.selection import select_excel_file
from controllers.table import show_excel_data
from controllers.transactions import build_transactions
from models.transaction import Transaction
from services.excel_exporter import export_transactions_to_excel
from services.file_initializer import ensure_required_files
from ui.classification_window import open_classification_window



APP_TITLE = "LedgerFlow"


def main() -> None:
    # =========================================================
    # MAIN WINDOW
    # =========================================================
    ensure_required_files()

    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("1050x900")
    root.minsize(850, 700)

    icon_path = (
        Path(__file__).resolve().parent
        / "assets"
        / "ledgerflow.png"
    )

    if icon_path.exists():
        app_icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, app_icon)

    container = ttk.Frame(
        root,
        padding=30,
    )
    container.pack(
        fill="both",
        expand=True,
    )

    # =========================================================
    # APPLICATION HEADER
    # =========================================================

    title_label = ttk.Label(
        container,
        text=APP_TITLE,
        font=("Sans", 22, "bold"),
    )
    title_label.pack(pady=(0, 8))

    description_label = ttk.Label(
        container,
        text="Financial Excel Organizer",
    )
    description_label.pack(pady=(0, 25))

    # =========================================================
    # APPLICATION STATE
    # =========================================================

    start_row_var = tk.IntVar(value=3)

    name_column_var = tk.StringVar()
    amount_column_var = tk.StringVar()

    new_group_var = tk.StringVar()

    loaded_headers: list[str] = []
    loaded_rows: list[list[object]] = []
    transactions: list[Transaction] = []

    groups = load_groups()

    # =========================================================
    # EXCEL FILE OPTIONS
    # =========================================================

    excel_options_frame = ttk.LabelFrame(
        container,
        text="Excel File",
        padding=15,
    )
    excel_options_frame.pack(
        fill="x",
        pady=(0, 15),
    )

    row_label = ttk.Label(
        excel_options_frame,
        text="Header row:",
    )
    row_label.pack(
        side="left",
        padx=(0, 10),
    )

    row_selector = ttk.Spinbox(
        excel_options_frame,
        from_=0,
        to=10000,
        width=8,
        textvariable=start_row_var,
    )
    row_selector.pack(
        side="left",
        padx=(0, 15),
    )

    status_label = ttk.Label(
        excel_options_frame,
        text="Ready",
    )
    status_label.pack(
        side="right",
        padx=(15, 0),
    )

    # =========================================================
    # COLUMN SELECTION
    # =========================================================

    column_selection_frame = ttk.LabelFrame(
        container,
        text="Column Selection",
        padding=15,
    )
    column_selection_frame.pack(
        fill="x",
        pady=(0, 15),
    )

    column_selection_frame.columnconfigure(
        1,
        weight=1,
    )

    name_column_label = ttk.Label(
        column_selection_frame,
        text="Name column:",
    )
    name_column_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 10),
        pady=(0, 10),
    )

    name_column_selector = ttk.Combobox(
        column_selection_frame,
        textvariable=name_column_var,
        state="disabled",
        width=30,
    )
    name_column_selector.grid(
        row=0,
        column=1,
        sticky="ew",
        pady=(0, 10),
    )

    amount_column_label = ttk.Label(
        column_selection_frame,
        text="Amount column:",
    )
    amount_column_label.grid(
        row=1,
        column=0,
        sticky="w",
        padx=(0, 10),
    )

    amount_column_selector = ttk.Combobox(
        column_selection_frame,
        textvariable=amount_column_var,
        state="disabled",
        width=30,
    )
    amount_column_selector.grid(
        row=1,
        column=1,
        sticky="ew",
    )

    # =========================================================
    # EXCEL TABLE
    # =========================================================

    excel_frame = ttk.LabelFrame(
        container,
        text="Excel Data",
        padding=10,
    )
    excel_frame.pack(
        fill="both",
        expand=True,
        pady=(0, 15),
    )

    table_container = ttk.Frame(excel_frame)
    table_container.pack(
        fill="both",
        expand=True,
    )

    table_container.columnconfigure(
        0,
        weight=1,
    )
    table_container.rowconfigure(
        0,
        weight=1,
    )

    excel_tree = ttk.Treeview(
        table_container,
        show="headings",
        height=12,
    )

    vertical_scrollbar = ttk.Scrollbar(
        table_container,
        orient="vertical",
        command=excel_tree.yview,
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_container,
        orient="horizontal",
        command=excel_tree.xview,
    )

    excel_tree.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    excel_tree.grid(
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

    # =========================================================
    # EXCEL ACTIONS
    # =========================================================

    def load_selected_excel() -> None:
        nonlocal loaded_headers
        nonlocal loaded_rows
        nonlocal transactions

        header_row = start_row_var.get() + 1

        result = select_excel_file(
            status_label,
            header_row,
        )

        if result is None:
            return

        headers, rows = result

        loaded_headers = headers
        loaded_rows = rows
        transactions = []

        show_excel_data(
            excel_tree,
            headers,
            rows,
        )

        configure_column_selectors(
            headers,
            name_column_selector,
            amount_column_selector,
            name_column_var,
            amount_column_var,
        )

    def prepare_transactions() -> None:
        nonlocal transactions

        selected_columns = get_selected_columns(
            name_column_var,
            amount_column_var,
        )

        if selected_columns is None:
            return

        name_column, amount_column = selected_columns

        transactions = build_transactions(
            loaded_headers,
            loaded_rows,
            name_column,
            amount_column,
        )

        status_label.config(
            text=f"{len(transactions)} transactions ready",
        )

        open_classification_window(
            root,
            transactions,
            groups,
        )

        export_button.config(
            state="normal",
        )

    def export_excel() -> None:
        export_transactions_to_excel(
            root,
            transactions,
            groups,
        )


    select_button = ttk.Button(
        excel_options_frame,
        text="Select Excel File",
        command=load_selected_excel,
    )
    select_button.pack(side="left")

    actions_frame = ttk.Frame(
        column_selection_frame,
    )
    actions_frame.grid(
        row=2,
        column=0,
        columnspan=2,
        pady=(15, 0),
    )

    prepare_button = ttk.Button(
        actions_frame,
        text="Start Classification",
        command=prepare_transactions,
    )
    prepare_button.pack(
        side="left",
        padx=(0, 5),
    )

    export_button = ttk.Button(
        column_selection_frame,
        text="Export Excel",
        command=export_excel,
        state="disabled",
    )

    export_button.grid(
        row=2,
        column=1,
        pady=(15, 0),
        padx=(5, 0),
    )

    # =========================================================
    # GROUP CREATION
    # =========================================================

    group_creation_frame = ttk.LabelFrame(
        container,
        text="Create Group",
        padding=15,
    )
    group_creation_frame.pack(
        fill="x",
        pady=(0, 15),
    )

    new_group_entry = ttk.Entry(
        group_creation_frame,
        textvariable=new_group_var,
    )
    new_group_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10),
    )

    create_group_button = ttk.Button(
        group_creation_frame,
        text="Create Group",
        command=lambda: create_group(
            new_group_var,
            groups_listbox,
            groups,
        ),
    )
    create_group_button.pack(side="left")

    # =========================================================
    # AVAILABLE GROUPS
    # =========================================================

    groups_frame = ttk.LabelFrame(
        container,
        text="Available Groups",
        padding=15,
    )
    groups_frame.pack(
        fill="both",
        pady=(0, 10),
    )

    groups_listbox = tk.Listbox(
        groups_frame,
        height=8,
        exportselection=False,
    )
    groups_listbox.pack(
        fill="both",
        expand=True,
    )

    for group_name in groups:
        groups_listbox.insert(
            tk.END,
            group_name,
        )

    delete_group_button = ttk.Button(
        groups_frame,
        text="Delete Selected Group",
        command=lambda: delete_group(
            groups_listbox,
            groups,
        ),
    )
    delete_group_button.pack(
        pady=(10, 0),
    )

    # =========================================================
    # KEYBOARD EVENTS
    # =========================================================

    new_group_entry.bind(
        "<Return>",
        lambda event: create_group(
            new_group_var,
            groups_listbox,
            groups,
        ),
    )

    groups_listbox.bind(
        "<Delete>",
        lambda event: delete_group(
            groups_listbox,
            groups,
        ),
    )

    # =========================================================
    # START APPLICATION
    # =========================================================

    root.mainloop()


if __name__ == "__main__":
    main()