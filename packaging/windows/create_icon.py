from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ICON_SIZES = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def create_windows_icon(
    source_path: Path,
    output_path: Path,
) -> None:
    if not source_path.is_file():
        raise FileNotFoundError(
            f"Source icon not found: {source_path}"
        )

    with Image.open(source_path) as source_image:
        image = source_image.convert("RGBA")

        canvas_size = max(
            image.width,
            image.height,
            256,
        )

        canvas = Image.new(
            mode="RGBA",
            size=(canvas_size, canvas_size),
            color=(0, 0, 0, 0),
        )

        position = (
            (canvas_size - image.width) // 2,
            (canvas_size - image.height) // 2,
        )

        canvas.alpha_composite(
            image,
            dest=position,
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        canvas.save(
            output_path,
            format="ICO",
            sizes=ICON_SIZES,
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the LedgerFlow Windows icon.",
    )

    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="Source PNG file.",
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination ICO file.",
    )

    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    create_windows_icon(
        source_path=arguments.source,
        output_path=arguments.output,
    )

    print(
        f"Windows icon created: {arguments.output}"
    )


if __name__ == "__main__":
    main()