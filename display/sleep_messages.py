#!/usr/bin/env python3
"""Display sleep and wake messages on the RGB matrix."""

import time

from PIL import Image

try:
    from rgbmatrix import graphics

    HAS_MATRIX = True
except ImportError:
    HAS_MATRIX = False

from config import IMAGES_DIR
from utils import initialize_matrix


def show_goodnight_message() -> None:
    """Display goodnight message with moon icon for 15 seconds."""
    if not HAS_MATRIX:
        print("Goodnight! 🌙")
        return

    matrix, font = initialize_matrix()
    canvas = matrix.CreateFrameCanvas()

    try:
        canvas.Clear()

        # Matrix dimensions
        height = canvas.height  # 32

        # Load and display moon image on the left
        moon_path = IMAGES_DIR / "other" / "moon.png"
        text_color = graphics.Color(255, 255, 255)

        if moon_path.exists():
            image = Image.open(moon_path).convert("RGB")

            # Resize image to fit on left side (max 28x28)
            max_size = min(28, height - 4)
            aspect_ratio = image.width / image.height

            if aspect_ratio > 1:  # Wider than tall
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:  # Taller than wide
                new_height = max_size
                new_width = int(max_size * aspect_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Place image on left, vertically centered
            x_pos = 2
            y_pos = (height - new_height) // 2

            canvas.SetImage(image, x_pos, y_pos)

            # Calculate text starting position (right of image with padding)
            text_start_x = x_pos + new_width + 4
        else:
            # No image, start text from left
            text_start_x = 2

        # Draw two-line message on the right, vertically centered
        line1 = "Good"
        line2 = "Night!"

        # Font height is 7 pixels, with some spacing between lines
        line_height = 8
        total_text_height = line_height * 2

        # Calculate vertical center position for both lines
        text_start_y = (height - total_text_height) // 2 + 7  # +7 for font baseline

        # Draw first line
        graphics.DrawText(canvas, font, text_start_x, text_start_y, text_color, line1)

        # Draw second line
        graphics.DrawText(
            canvas, font, text_start_x, text_start_y + line_height, text_color, line2
        )

        canvas = matrix.SwapOnVSync(canvas)

        # Display for 15 seconds
        time.sleep(15)

        # Clear display
        matrix.Clear()
    except Exception as e:
        print(f"Error displaying goodnight message: {e}")
        matrix.Clear()


def show_goodmorning_message() -> None:
    """Display good morning message with sun icon for 15 seconds."""
    if not HAS_MATRIX:
        print("Hello! ☀️")
        return

    matrix, font = initialize_matrix()
    canvas = matrix.CreateFrameCanvas()

    try:
        canvas.Clear()

        # Matrix dimensions
        height = canvas.height  # 32

        # Load and display sun image on the left
        sun_path = IMAGES_DIR / "other" / "sun.png"
        text_color = graphics.Color(255, 255, 255)

        if sun_path.exists():
            image = Image.open(sun_path).convert("RGB")

            # Resize image to fit on left side (max 28x28)
            max_size = min(28, height - 4)
            aspect_ratio = image.width / image.height

            if aspect_ratio > 1:  # Wider than tall
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:  # Taller than wide
                new_height = max_size
                new_width = int(max_size * aspect_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Place image on left, vertically centered
            x_pos = 2
            y_pos = (height - new_height) // 2

            canvas.SetImage(image, x_pos, y_pos)

            # Calculate text starting position (right of image with padding)
            text_start_x = x_pos + new_width + 4
        else:
            # No image, start text from left
            text_start_x = 2

        # Draw "Hello!" text on the right, vertically centered
        text = "Hello!"

        # Calculate vertical center position
        text_y = height // 2 + 4  # +4 for font baseline

        # Draw text
        graphics.DrawText(canvas, font, text_start_x, text_y, text_color, text)

        canvas = matrix.SwapOnVSync(canvas)

        # Display for 15 seconds
        time.sleep(15)

        # Clear display
        matrix.Clear()
    except Exception as e:
        print(f"Error displaying good morning message: {e}")
        matrix.Clear()
