from services.file_initializer import ensure_required_files
from ui.main_window import LedgerFlowApp


def main() -> None:
    ensure_required_files()

    app = LedgerFlowApp()
    app.mainloop()


if __name__ == "__main__":
    main()