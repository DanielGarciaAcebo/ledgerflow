import tkinter as tk
from tkinter import messagebox, ttk

from classificationController.classification_repository import (
    save_classification,
)
from transactionController.transaction_controller import Transaction


def open_classification_window(
    parent: tk.Misc,
    transactions: list[Transaction],
    groups: list[str],
) -> None:
    if not transactions:
        messagebox.showwarning(
            title="No Transactions",
            message="There are no transactions to classify.",
            parent=parent,
        )
        return

    if not groups:
        messagebox.showwarning(
            title="No Groups",
            message="Create at least one group before starting classification.",
            parent=parent,
        )
        return

    # =========================================================
    # WINDOW
    # =========================================================

    window = tk.Toplevel(parent)
    window.title("Classify Transactions")
    window.geometry("900x700")
    window.minsize(750, 600)
    window.resizable(True, True)

    window.transient(parent)
    window.grab_set()

    current_index = 0

    name_var = tk.StringVar()
    amount_var = tk.StringVar()
    progress_var = tk.StringVar()
    status_var = tk.StringVar()

    # Each group contains:
    # selected variable
    # inverted variable
    # inverted checkbox
    group_controls: dict[
        str,
        tuple[
            tk.BooleanVar,
            tk.BooleanVar,
            ttk.Checkbutton,
        ],
    ] = {}

    # =========================================================
    # HEADER
    # =========================================================

    title_label = ttk.Label(
        window,
        text="Classify Transaction",
        font=("Sans", 20, "bold"),
    )
    title_label.pack(
        pady=(25, 5),
    )

    progress_label = ttk.Label(
        window,
        textvariable=progress_var,
    )
    progress_label.pack(
        pady=(0, 20),
    )

    # =========================================================
    # TRANSACTION INFORMATION
    # =========================================================

    transaction_frame = ttk.LabelFrame(
        window,
        text="Transaction",
        padding=15,
    )
    transaction_frame.pack(
        fill="x",
        padx=25,
        pady=(0, 15),
    )

    transaction_frame.columnconfigure(
        1,
        weight=1,
    )

    name_title = ttk.Label(
        transaction_frame,
        text="Name:",
        font=("Sans", 10, "bold"),
    )
    name_title.grid(
        row=0,
        column=0,
        sticky="nw",
        padx=(0, 10),
        pady=(0, 10),
    )

    name_label = ttk.Label(
        transaction_frame,
        textvariable=name_var,
        wraplength=700,
    )
    name_label.grid(
        row=0,
        column=1,
        sticky="w",
        pady=(0, 10),
    )

    amount_title = ttk.Label(
        transaction_frame,
        text="Amount:",
        font=("Sans", 10, "bold"),
    )
    amount_title.grid(
        row=1,
        column=0,
        sticky="w",
        padx=(0, 10),
    )

    amount_label = ttk.Label(
        transaction_frame,
        textvariable=amount_var,
        font=("Sans", 11, "bold"),
    )
    amount_label.grid(
        row=1,
        column=1,
        sticky="w",
    )

    # =========================================================
    # GROUP SELECTION
    # =========================================================

    groups_frame = ttk.LabelFrame(
        window,
        text="Select Groups",
        padding=15,
    )
    groups_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 15),
    )

    groups_frame.columnconfigure(
        0,
        weight=1,
    )
    groups_frame.rowconfigure(
        1,
        weight=1,
    )

    # Column headers
    groups_header = ttk.Frame(
        groups_frame,
    )
    groups_header.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=(5, 20),
        pady=(0, 10),
    )

    groups_header.columnconfigure(
        0,
        weight=1,
    )

    group_header_label = ttk.Label(
        groups_header,
        text="Group",
        font=("Sans", 10, "bold"),
    )
    group_header_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    invert_header_label = ttk.Label(
        groups_header,
        text="Invert sign",
        font=("Sans", 10, "bold"),
    )
    invert_header_label.grid(
        row=0,
        column=1,
        sticky="e",
    )

    # Scrollable groups container
    groups_canvas = tk.Canvas(
        groups_frame,
        highlightthickness=0,
    )
    groups_canvas.grid(
        row=1,
        column=0,
        sticky="nsew",
    )

    groups_scrollbar = ttk.Scrollbar(
        groups_frame,
        orient="vertical",
        command=groups_canvas.yview,
    )
    groups_scrollbar.grid(
        row=1,
        column=1,
        sticky="ns",
    )

    groups_canvas.configure(
        yscrollcommand=groups_scrollbar.set,
    )

    groups_content = ttk.Frame(
        groups_canvas,
    )

    groups_canvas_window = groups_canvas.create_window(
        (0, 0),
        window=groups_content,
        anchor="nw",
    )

    groups_content.columnconfigure(
        0,
        weight=1,
    )

    def update_scroll_region(_event: tk.Event) -> None:
        groups_canvas.configure(
            scrollregion=groups_canvas.bbox("all"),
        )

    def update_content_width(event: tk.Event) -> None:
        groups_canvas.itemconfigure(
            groups_canvas_window,
            width=event.width,
        )

    groups_content.bind(
        "<Configure>",
        update_scroll_region,
    )

    groups_canvas.bind(
        "<Configure>",
        update_content_width,
    )

    # =========================================================
    # GROUP CONTROLS
    # =========================================================

    def update_invert_control(
        group_name: str,
    ) -> None:
        selected_var, inverted_var, inverted_checkbox = (
            group_controls[group_name]
        )

        if selected_var.get():
            inverted_checkbox.config(
                state="normal",
            )
            return

        inverted_var.set(False)

        inverted_checkbox.config(
            state="disabled",
        )

    for row_index, group_name in enumerate(groups):
        group_row = ttk.Frame(
            groups_content,
            padding=(5, 5),
        )
        group_row.grid(
            row=row_index,
            column=0,
            sticky="ew",
        )

        group_row.columnconfigure(
            0,
            weight=1,
        )

        selected_var = tk.BooleanVar(
            value=False,
        )

        inverted_var = tk.BooleanVar(
            value=False,
        )

        selected_checkbox = ttk.Checkbutton(
            group_row,
            text=group_name,
            variable=selected_var,
            command=lambda name=group_name: update_invert_control(
                name
            ),
        )
        selected_checkbox.grid(
            row=0,
            column=0,
            sticky="w",
        )

        inverted_checkbox = ttk.Checkbutton(
            group_row,
            text="Invert",
            variable=inverted_var,
            state="disabled",
        )
        inverted_checkbox.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(20, 5),
        )

        group_controls[group_name] = (
            selected_var,
            inverted_var,
            inverted_checkbox,
        )

    # =========================================================
    # STATUS
    # =========================================================

    selection_status_label = ttk.Label(
        window,
        textvariable=status_var,
    )
    selection_status_label.pack(
        pady=(0, 10),
    )

    # =========================================================
    # CLASSIFICATION LOGIC
    # =========================================================

    def get_current_assignments() -> dict[str, bool]:
        return {
            group_name: inverted_var.get()
            for group_name, (
                selected_var,
                inverted_var,
                _,
            ) in group_controls.items()
            if selected_var.get()
        }

    def save_current_selection() -> None:
        transaction = transactions[current_index]

        assignments = get_current_assignments()

        transaction.group_assignments = assignments

        save_classification(
            transaction.name,
            transaction.amount,
            transaction.group_assignments,
        )

    def apply_current_selection() -> None:
        assignments = get_current_assignments()

        if not assignments:
            messagebox.showwarning(
                title="No Group Selected",
                message="Select at least one group.",
                parent=window,
            )
            return

        save_current_selection()

        assignment_names = [
            (
                f"{group_name} (inverted)"
                if inverted
                else group_name
            )
            for group_name, inverted
            in transactions[
                current_index
            ].group_assignments.items()
        ]

        status_var.set(
            "Saved: " + ", ".join(assignment_names)
        )

    def load_current_transaction() -> None:
        transaction = transactions[current_index]

        name_var.set(
            transaction.name,
        )

        amount_var.set(
            str(transaction.amount),
        )

        progress_var.set(
            f"Transaction {current_index + 1} "
            f"of {len(transactions)}"
        )

        status_var.set("")

        for group_name, (
            selected_var,
            inverted_var,
            inverted_checkbox,
        ) in group_controls.items():
            is_selected = (
                group_name
                in transaction.group_assignments
            )

            is_inverted = (
                transaction.group_assignments.get(
                    group_name,
                    False,
                )
            )

            selected_var.set(
                is_selected,
            )

            inverted_var.set(
                is_inverted,
            )

            inverted_checkbox.config(
                state=(
                    "normal"
                    if is_selected
                    else "disabled"
                ),
            )

        if current_index == 0:
            previous_button.config(
                state="disabled",
            )
        else:
            previous_button.config(
                state="normal",
            )

        if current_index == len(transactions) - 1:
            next_button.config(
                text="Finish",
            )
        else:
            next_button.config(
                text="Next",
            )

    def previous_transaction() -> None:
        nonlocal current_index

        save_current_selection()

        if current_index > 0:
            current_index -= 1
            load_current_transaction()

    def next_transaction() -> None:
        nonlocal current_index

        save_current_selection()

        if current_index < len(transactions) - 1:
            current_index += 1
            load_current_transaction()
            return

        unclassified_count = sum(
            not transaction.group_assignments
            for transaction in transactions
        )

        if unclassified_count:
            confirmed = messagebox.askyesno(
                title="Unclassified Transactions",
                message=(
                    f"{unclassified_count} transactions "
                    "have no group.\n\n"
                    "Finish classification anyway?"
                ),
                parent=window,
            )

            if not confirmed:
                return

        messagebox.showinfo(
            title="Classification Complete",
            message="The transactions have been classified.",
            parent=window,
        )

        window.destroy()

    def close_window() -> None:
        save_current_selection()
        window.destroy()

    # =========================================================
    # NAVIGATION BUTTONS
    # =========================================================

    buttons_frame = ttk.Frame(
        window,
    )
    buttons_frame.pack(
        fill="x",
        padx=25,
        pady=(0, 25),
    )

    previous_button = ttk.Button(
        buttons_frame,
        text="Previous",
        command=previous_transaction,
    )
    previous_button.pack(
        side="left",
    )

    apply_button = ttk.Button(
        buttons_frame,
        text="Apply Selection",
        command=apply_current_selection,
    )
    apply_button.pack(
        side="left",
        padx=(10, 0),
    )

    close_button = ttk.Button(
        buttons_frame,
        text="Save and Close",
        command=close_window,
    )
    close_button.pack(
        side="left",
        padx=(10, 0),
    )

    next_button = ttk.Button(
        buttons_frame,
        text="Next",
        command=next_transaction,
    )
    next_button.pack(
        side="right",
    )

    # =========================================================
    # WINDOW EVENTS
    # =========================================================

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window,
    )

    load_current_transaction()

    window.wait_window()