from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from controllers.columns import (
    ColumnNotFoundError,
    MissingAmountColumnError,
    MissingNameColumnError,
    SameColumnSelectionError,
    validate_column_selection,
)
from controllers.groups import (
    GroupAlreadyExistsError,
    GroupNotFoundError,
    InvalidGroupNameError,
    create_group,
    delete_group,
    load_groups,
)
from ui.components.excel_table import ExcelTable
from controllers.transactions import build_transactions
from models.transaction import Transaction
from services.excel_exporter import export_transactions_to_excel
from services.excel_reader import (
    EmptyExcelFileError,
    ExcelReadError,
    HeaderRowNotFoundError,
    InvalidHeaderRowError,
    read_excel_file,
)
from ui.classification_window import open_classification_window


APP_TITLE = "LedgerFlow"


class LedgerFlowApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.start_row_var = tk.IntVar(value=3)
        self.name_column_var = tk.StringVar()
        self.amount_column_var = tk.StringVar()
        self.new_group_var = tk.StringVar()

        self.loaded_headers: list[str] = []
        self.loaded_rows: list[list[object]] = []
        self.transactions: list[Transaction] = []
        self.groups = load_groups()

        self._app_icon: tk.PhotoImage | None = None

        self._configure_window()
        self._create_layout()
        self._bind_events()

    # =========================================================
    # WINDOW CONFIGURATION
    # =========================================================

    def _configure_window(self) -> None:
        self.title(APP_TITLE)
        self.geometry("1050x900")
        self.minsize(850, 700)

        icon_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "ledgerflow.png"
        )

        if icon_path.exists():
            self._app_icon = tk.PhotoImage(
                file=icon_path,
            )

            self.iconphoto(
                True,
                self._app_icon,
            )

    # =========================================================
    # MAIN LAYOUT
    # =========================================================

    def _create_layout(self) -> None:
        self.container = ttk.Frame(
            self,
            padding=30,
        )
        self.container.pack(
            fill="both",
            expand=True,
        )

        self._create_header()
        self._create_excel_options()
        self._create_column_selection()
        self._create_excel_table()
        self._create_group_creation()
        self._create_groups_section()

    # =========================================================
    # HEADER
    # =========================================================

    def _create_header(self) -> None:
        title_label = ttk.Label(
            self.container,
            text=APP_TITLE,
            font=("Sans", 22, "bold"),
        )
        title_label.pack(
            pady=(0, 8),
        )

        description_label = ttk.Label(
            self.container,
            text="Financial Excel Organizer",
        )
        description_label.pack(
            pady=(0, 25),
        )

    # =========================================================
    # EXCEL OPTIONS
    # =========================================================

    def _create_excel_options(self) -> None:
        excel_options_frame = ttk.LabelFrame(
            self.container,
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
            textvariable=self.start_row_var,
        )
        row_selector.pack(
            side="left",
            padx=(0, 15),
        )

        select_button = ttk.Button(
            excel_options_frame,
            text="Select Excel File",
            command=self._load_selected_excel,
        )
        select_button.pack(
            side="left",
        )

        self.status_label = ttk.Label(
            excel_options_frame,
            text="Ready",
        )
        self.status_label.pack(
            side="right",
            padx=(15, 0),
        )

    # =========================================================
    # COLUMN SELECTION
    # =========================================================

    def _create_column_selection(self) -> None:
        column_selection_frame = ttk.LabelFrame(
            self.container,
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

        self.name_column_selector = ttk.Combobox(
            column_selection_frame,
            textvariable=self.name_column_var,
            state="disabled",
            width=30,
        )
        self.name_column_selector.grid(
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

        self.amount_column_selector = ttk.Combobox(
            column_selection_frame,
            textvariable=self.amount_column_var,
            state="disabled",
            width=30,
        )
        self.amount_column_selector.grid(
            row=1,
            column=1,
            sticky="ew",
        )

        actions_frame = ttk.Frame(
            column_selection_frame,
        )
        actions_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(15, 0),
        )

        self.prepare_button = ttk.Button(
            actions_frame,
            text="Start Classification",
            command=self._prepare_transactions,
            state="disabled",
        )
        self.prepare_button.pack(
            side="left",
            padx=(0, 5),
        )

        self.export_button = ttk.Button(
            actions_frame,
            text="Export Excel",
            command=self._export_excel,
            state="disabled",
        )
        self.export_button.pack(
            side="left",
            padx=(5, 0),
        )

    def _configure_column_selectors(
        self,
        headers: list[str],
    ) -> None:
        self.name_column_selector["values"] = headers
        self.amount_column_selector["values"] = headers

        self.name_column_selector.config(
            state="readonly",
        )

        self.amount_column_selector.config(
            state="readonly",
        )

        self.name_column_var.set("")
        self.amount_column_var.set("")

    # =========================================================
    # EXCEL TABLE
    # =========================================================

    def _create_excel_table(self) -> None:
        self.excel_table = ExcelTable(
            self.container,
        )

        self.excel_table.pack(
            fill="both",
            expand=True,
            pady=(0, 15),
        )

    # =========================================================
    # GROUP CREATION
    # =========================================================

    def _create_group_creation(self) -> None:
        group_creation_frame = ttk.LabelFrame(
            self.container,
            text="Create Group",
            padding=15,
        )
        group_creation_frame.pack(
            fill="x",
            pady=(0, 15),
        )

        self.new_group_entry = ttk.Entry(
            group_creation_frame,
            textvariable=self.new_group_var,
        )
        self.new_group_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10),
        )

        create_group_button = ttk.Button(
            group_creation_frame,
            text="Create Group",
            command=self._create_group,
        )
        create_group_button.pack(
            side="left",
        )

    # =========================================================
    # AVAILABLE GROUPS
    # =========================================================

    def _create_groups_section(self) -> None:
        groups_frame = ttk.LabelFrame(
            self.container,
            text="Available Groups",
            padding=15,
        )
        groups_frame.pack(
            fill="both",
            pady=(0, 10),
        )

        self.groups_listbox = tk.Listbox(
            groups_frame,
            height=8,
            exportselection=False,
        )
        self.groups_listbox.pack(
            fill="both",
            expand=True,
        )

        for group_name in self.groups:
            self.groups_listbox.insert(
                tk.END,
                group_name,
            )

        delete_group_button = ttk.Button(
            groups_frame,
            text="Delete Selected Group",
            command=self._delete_group,
        )
        delete_group_button.pack(
            pady=(10, 0),
        )

    # =========================================================
    # EVENTS
    # =========================================================

    def _bind_events(self) -> None:
        self.new_group_entry.bind(
            "<Return>",
            self._handle_create_group,
        )

        self.groups_listbox.bind(
            "<Delete>",
            self._handle_delete_group,
        )

    def _handle_create_group(
        self,
        _event: tk.Event,
    ) -> None:
        self._create_group()

    def _handle_delete_group(
        self,
        _event: tk.Event,
    ) -> None:
        self._delete_group()

    # =========================================================
    # EXCEL LOADING
    # =========================================================

    def _load_selected_excel(self) -> None:
        file_path = filedialog.askopenfilename(
            parent=self,
            title="Select Excel File",
            initialdir=str(Path.home()),
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            self.status_label.config(
                text="No file selected",
            )
            return

        header_row = self.start_row_var.get() + 1

        try:
            excel_data = read_excel_file(
                file_path,
                header_row,
            )
        except InvalidHeaderRowError as error:
            self._show_excel_error(
                "Invalid Header Row",
                error,
            )
            return
        except HeaderRowNotFoundError as error:
            self._show_excel_error(
                "Header Row Not Found",
                error,
            )
            return
        except EmptyExcelFileError as error:
            self._show_excel_error(
                "Empty Excel File",
                error,
            )
            return
        except ExcelReadError as error:
            self._show_excel_error(
                "Excel Error",
                error,
            )
            return

        self.loaded_headers = excel_data.headers
        self.loaded_rows = excel_data.rows
        self.transactions = []

        self.excel_table.show_data(
            excel_data.headers,
            excel_data.rows,
        )

        self._configure_column_selectors(
            excel_data.headers,
        )

        self.status_label.config(
            text=f"Selected: {excel_data.file_path.name}",
        )

        self.prepare_button.config(
            state="normal",
        )

        self.export_button.config(
            state="disabled",
        )

    def _show_excel_error(
        self,
        title: str,
        error: Exception,
    ) -> None:
        self.status_label.config(
            text="Could not read the file",
        )

        messagebox.showerror(
            title=title,
            message=str(error),
            parent=self,
        )

    # =========================================================
    # TRANSACTION CLASSIFICATION
    # =========================================================

    def _prepare_transactions(self) -> None:
        try:
            name_column, amount_column = (
                validate_column_selection(
                    self.name_column_var.get(),
                    self.amount_column_var.get(),
                    self.loaded_headers,
                )
            )
        except MissingNameColumnError as error:
            messagebox.showwarning(
                title="Missing Name Column",
                message=str(error),
                parent=self,
            )
            return
        except MissingAmountColumnError as error:
            messagebox.showwarning(
                title="Missing Amount Column",
                message=str(error),
                parent=self,
            )
            return
        except SameColumnSelectionError as error:
            messagebox.showwarning(
                title="Invalid Column Selection",
                message=str(error),
                parent=self,
            )
            return
        except ColumnNotFoundError as error:
            messagebox.showerror(
                title="Column Not Found",
                message=str(error),
                parent=self,
            )
            return

        self.transactions = build_transactions(
            self.loaded_headers,
            self.loaded_rows,
            name_column,
            amount_column,
        )

        self.status_label.config(
            text=(
                f"{len(self.transactions)} "
                "transactions ready"
            ),
        )

        open_classification_window(
            self,
            self.transactions,
            self.groups,
        )

        self.export_button.config(
            state="normal",
        )

    # =========================================================
    # EXCEL EXPORT
    # =========================================================

    def _export_excel(self) -> None:
        export_transactions_to_excel(
            self,
            self.transactions,
            self.groups,
        )

    # =========================================================
    # GROUP ACTIONS
    # =========================================================

    def _create_group(self) -> None:
        try:
            created_group = create_group(
                self.new_group_var.get(),
                self.groups,
            )
        except InvalidGroupNameError as error:
            messagebox.showwarning(
                title="Invalid Group",
                message=str(error),
                parent=self,
            )
            return
        except GroupAlreadyExistsError as error:
            messagebox.showwarning(
                title="Group Already Exists",
                message=str(error),
                parent=self,
            )
            return

        self.groups_listbox.insert(
            tk.END,
            created_group,
        )

        self.new_group_var.set("")

    def _delete_group(self) -> None:
        selected_indices = self.groups_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning(
                title="No Group Selected",
                message="Select a group to delete.",
                parent=self,
            )
            return

        selected_index = selected_indices[0]

        group_name = str(
            self.groups_listbox.get(selected_index)
        )

        confirmed = messagebox.askyesno(
            title="Delete Group",
            message=f'Delete the group "{group_name}"?',
            parent=self,
        )

        if not confirmed:
            return

        try:
            delete_group(
                group_name,
                self.groups,
            )
        except GroupNotFoundError as error:
            messagebox.showerror(
                title="Group Not Found",
                message=str(error),
                parent=self,
            )
            return

        self.groups_listbox.delete(
            selected_index,
        )