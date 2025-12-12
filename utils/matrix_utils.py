#!/usr/bin/env python3
"""Utility functions for RGB matrix operations."""

from typing import TYPE_CHECKING, Any

# Conditional import - only import rgbmatrix on Raspberry Pi
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

    HAS_MATRIX = True
except ImportError:
    HAS_MATRIX = False
    # Create dummy types for type checking
    if TYPE_CHECKING:
        from typing import Any as RGBMatrix

        class RGBMatrixOptions:  # noqa: N801
            """Dummy RGBMatrixOptions class for type checking."""

            rows: int
            cols: int
            chain_length: int
            parallel: int
            hardware_mapping: str
            gpio_slowdown: int

        class graphics:  # noqa: N801
            """Dummy graphics class for type checking."""

            class Font:
                """Dummy Font class for type checking."""

                def LoadFont(self, path: str) -> bool:  # noqa: N802
                    """Dummy LoadFont method."""
                    return True

            @staticmethod
            def Color(r: int, g: int, b: int) -> Any:  # noqa: N802
                """Dummy Color method."""
                pass

            @staticmethod
            def DrawText(  # noqa: N802
                canvas: Any, font: Any, x: int, y: int, color: Any, text: str
            ) -> None:  # noqa: N802
                """Dummy DrawText method."""
                pass


from config import DEFAULT_FONT, MATRIX_CONFIG


def initialize_matrix() -> tuple[Any, Any]:
    """Initialize the RGB matrix and load font."""
    options = RGBMatrixOptions()
    options.rows = MATRIX_CONFIG["rows"]
    options.cols = MATRIX_CONFIG["cols"]
    options.chain_length = MATRIX_CONFIG["chain_length"]
    options.parallel = MATRIX_CONFIG["parallel"]
    options.hardware_mapping = MATRIX_CONFIG["hardware_mapping"]
    options.gpio_slowdown = MATRIX_CONFIG["gpio_slowdown"]

    matrix = RGBMatrix(options=options)

    # Load font
    font = graphics.Font()
    font.LoadFont(str(DEFAULT_FONT))

    return matrix, font


def calculate_centered_x(text: str, width: int, char_width: int = 5) -> int:
    """
    Calculate the x position to center text on the display.

    Args:
        text: The text to center
        width: The width of the display
        char_width: Average width per character in pixels (default 5 for 5x7 font)

    Returns:
        The x position to start drawing the text
    """
    text_width = len(text) * char_width
    return (width - text_width) // 2
