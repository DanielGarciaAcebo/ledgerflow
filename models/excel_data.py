from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ExcelData:
    file_path: Path
    sheet_name: str
    headers: list[str]
    rows: list[list[object]]