#!/usr/bin/env python3
"""Display module for showing sports scores."""

import time  # noqa: I001
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

from PIL import Image

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


from config import (
    DEFAULT_FONT,
    DISPLAY_MODE,
    EVENT_DISPLAY_TIME,
    LEAGUE_DISPLAY_TIME,
    MATRIX_CONFIG,
)
from models import SportsData


def _initialize_matrix() -> tuple[Any, Any]:
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


def display_scores(data: SportsData) -> None:
    """
    Display sports scores organized by league.
    Shows league info first, then iterates through each game.

    Uses DISPLAY_MODE from config to determine console or matrix output.

    Args:
        data: SportsData object containing events to display
    """
    if not data or not data.events:
        print("No events to display")
        return

    # Group events by league
    leagues = defaultdict(list)
    for event in data.events:
        leagues[event.league].append(event)

    # Determine which display method to use
    if DISPLAY_MODE == "matrix":
        _display_on_matrix(leagues)
    else:
        _display_on_console(leagues)


def _display_on_console(leagues: defaultdict) -> None:
    """Display scores to console for testing."""
    # Iterate through each league
    for league_name, events in leagues.items():
        # Display league header
        league_badge_path = events[0].league_badge_path if events else None
        print("\n" + "=" * 60)
        print(f"LEAGUE: {league_name}")
        if league_badge_path:
            print(f"Badge: {league_badge_path}")
        print("=" * 60)

        # Wait on first display of league
        print("Displaying league info...")
        time.sleep(LEAGUE_DISPLAY_TIME)

        # Display each game in this league
        for event in events:
            print("\n" + "-" * 60)
            print(f"{event.team_one.full_name} vs {event.team_two.full_name}")
            print(f"Status: {event.status}")
            print(f"Score: {event.team_one.score} - {event.team_two.score}")
            print(f"Date/Time: {event.date} at {event.time}")

            if event.team_one.badge_path:
                print(f"Team 1 Badge: {event.team_one.badge_path}")
            if event.team_two.badge_path:
                print(f"Team 2 Badge: {event.team_two.badge_path}")

            print("-" * 60)

            # Wait for each game
            print("Displaying game...")
            time.sleep(EVENT_DISPLAY_TIME)


def _display_on_matrix(leagues: defaultdict) -> None:
    """Display scores on RGB matrix."""
    matrix, font = _initialize_matrix()
    canvas = matrix.CreateFrameCanvas()

    try:
        # Iterate through each league
        for league_name, events in leagues.items():
            league_badge_path = events[0].league_badge_path if events else None

            # Display league header
            _show_league_screen(canvas, matrix, font, league_name, league_badge_path)
            time.sleep(LEAGUE_DISPLAY_TIME)

            # Display each game in this league
            for event in events:
                _show_game_screen(canvas, matrix, font, event)
                time.sleep(EVENT_DISPLAY_TIME)
    except KeyboardInterrupt:
        print("\n\nShutting down display...")
    finally:
        matrix.Clear()


def _show_league_screen(
    canvas, matrix, font, league_name: str, badge_path: Path | None
) -> None:
    """Display league name and badge centered on screen."""
    canvas.Clear()

    # Matrix dimensions
    width = canvas.width  # 64
    height = canvas.height  # 32

    # Load and display league badge if available
    if badge_path and badge_path.exists():
        image = Image.open(badge_path).convert("RGB")

        # Resize image to fit (max 32x20 to leave room for text)
        max_img_height = 20
        aspect_ratio = image.width / image.height
        new_height = min(max_img_height, height - 12)  # Leave room for text
        new_width = int(new_height * aspect_ratio)

        # Limit width to matrix width
        if new_width > width:
            new_width = width
            new_height = int(new_width / aspect_ratio)

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center the image horizontally, place near top
        x_pos = (width - new_width) // 2
        y_pos = 2

        canvas.SetImage(image, x_pos, y_pos)

        # Display league name below image
        text_y = y_pos + new_height + 8
    else:
        # No image, display text in center
        text_y = height // 2

    # Draw league name centered
    text_color = graphics.Color(255, 255, 255)
    text_width = len(league_name) * 6  # Approximate width
    text_x = (width - text_width) // 2

    graphics.DrawText(canvas, font, text_x, text_y, text_color, league_name)

    canvas = matrix.SwapOnVSync(canvas)


def _show_game_screen(canvas, matrix, font, event) -> None:
    """Display game info on screen."""
    canvas.Clear()

    # Text colors
    white = graphics.Color(255, 255, 255)
    green = graphics.Color(0, 255, 0)

    # Display team names and scores
    y_pos = 8

    # Team 1
    team1_text = f"{event.team_one.location[:3].upper()}"
    graphics.DrawText(canvas, font, 2, y_pos, white, team1_text)
    score1_text = str(event.team_one.score)
    graphics.DrawText(canvas, font, 25, y_pos, green, score1_text)

    # VS or status
    y_pos += 10
    graphics.DrawText(canvas, font, 2, y_pos, white, "VS")

    # Team 2
    y_pos += 10
    team2_text = f"{event.team_two.location[:3].upper()}"
    graphics.DrawText(canvas, font, 2, y_pos, white, team2_text)
    score2_text = str(event.team_two.score)
    graphics.DrawText(canvas, font, 25, y_pos, green, score2_text)

    # Status on right side
    status_text = event.status[:8]  # Truncate if too long
    graphics.DrawText(canvas, font, 35, 8, white, status_text)

    canvas = matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    from api.sports_api import fetch_scores

    print("Testing display module...")
    data = fetch_scores()

    if data:
        display_scores(data)
    else:
        print("Failed to fetch data")
