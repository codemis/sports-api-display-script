#!/usr/bin/env python3
"""Display module for showing sports scores."""

import contextlib
import time  # noqa: I001
from collections import defaultdict
from pathlib import Path

from PIL import Image

with contextlib.suppress(ImportError):
    from rgbmatrix import graphics

from config import DISPLAY_MODE, EVENT_DISPLAY_TIME, LEAGUE_DISPLAY_TIME
from models import SportsData
from utils import calculate_centered_x, initialize_matrix, is_sleep_time


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
            # Check if sleep time has been reached
            if is_sleep_time():
                print("\nSleep time reached, stopping display...")
                return

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
    matrix, font = initialize_matrix()
    canvas = matrix.CreateFrameCanvas()

    try:
        # Iterate through each league
        for league_name, events in leagues.items():
            # Check if sleep time has been reached
            if is_sleep_time():
                print("\nSleep time reached, stopping display...")
                matrix.Clear()
                return

            league_badge_path = events[0].league_badge_path if events else None

            # Display league header
            _show_league_screen(canvas, matrix, font, league_name, league_badge_path)
            time.sleep(LEAGUE_DISPLAY_TIME)

            # Display each game in this league
            for event in events:
                # Check if sleep time has been reached
                if is_sleep_time():
                    print("\nSleep time reached, stopping display...")
                    matrix.Clear()
                    return

                _show_game_screen(canvas, matrix, font, event)
                time.sleep(EVENT_DISPLAY_TIME)
    except KeyboardInterrupt:
        print("\n\nShutting down display...")
    finally:
        matrix.Clear()


def _show_league_screen(
    canvas, matrix, font, league_name: str, badge_path: Path | None
) -> None:
    """Display league badge on left and name on right, vertically centered."""
    canvas.Clear()

    # Matrix dimensions
    width = canvas.width  # 64
    height = canvas.height  # 32

    # Load and display league badge if available
    if badge_path and badge_path.exists():
        image = Image.open(badge_path).convert("RGB")

        # Resize image to fit on left side (max 28x28 to leave room for text)
        max_size = min(28, height - 4)
        aspect_ratio = image.width / image.height

        if aspect_ratio > 1:  # Wider than tall
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:  # Taller than wide
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Place image on left side, vertically centered
        x_pos = 2
        y_pos = (height - new_height) // 2

        canvas.SetImage(image, x_pos, y_pos)

        # Calculate text position (right of image)
        text_x = x_pos + new_width + 4  # 4 pixels padding
    else:
        # No image, display text in center
        text_x = (width - len(league_name) * 6) // 2

    # Draw league name on right side, vertically centered
    text_color = graphics.Color(255, 255, 255)
    text_y = height // 2 + 4  # Adjust for font baseline

    graphics.DrawText(canvas, font, text_x, text_y, text_color, league_name)

    canvas = matrix.SwapOnVSync(canvas)


def _show_game_screen(canvas, matrix, font, event) -> None:
    """Display game info with team badges and scores."""
    canvas.Clear()

    # Matrix dimensions
    width = canvas.width  # 64

    # Text colors
    white = graphics.Color(255, 255, 255)
    green = graphics.Color(0, 255, 0)

    # Display team badges on top row
    badge_size = 16  # Max size for badges
    y_badge = 1

    # Team 1 badge on left
    if event.team_one.badge_path and event.team_one.badge_path.exists():
        image1 = Image.open(event.team_one.badge_path).convert("RGB")
        aspect_ratio = image1.width / image1.height

        if aspect_ratio > 1:
            new_width = badge_size
            new_height = int(badge_size / aspect_ratio)
        else:
            new_height = badge_size
            new_width = int(badge_size * aspect_ratio)

        image1 = image1.resize((new_width, new_height), Image.Resampling.LANCZOS)
        canvas.SetImage(image1, 2, y_badge)

    # Team 2 badge on right
    if event.team_two.badge_path and event.team_two.badge_path.exists():
        image2 = Image.open(event.team_two.badge_path).convert("RGB")
        aspect_ratio = image2.width / image2.height

        if aspect_ratio > 1:
            new_width = badge_size
            new_height = int(badge_size / aspect_ratio)
        else:
            new_height = badge_size
            new_width = int(badge_size * aspect_ratio)

        image2 = image2.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Position on right side
        x_pos_right = width - new_width - 2
        canvas.SetImage(image2, x_pos_right, y_badge)

    # Display scores or date/time on second line (centered)
    y_text = 24
    last_line_text = ""
    if event.status_type == "STATUS_SCHEDULED":
        # Display date and time for scheduled games
        # Format: "Dec 7 7:30P" or similar compact format
        info_text = f"{event.formatted_date}"
        last_line_text = f"{event.time}"
        info_x = calculate_centered_x(info_text, width)
        graphics.DrawText(canvas, font, info_x, y_text, white, info_text)
    else:
        # Display scores for live/completed games
        score1_text = str(event.team_one.score)
        score2_text = str(event.team_two.score)
        full_score_text = f"{score1_text} - {score2_text}"

        # Center the entire score text
        char_width = 5
        start_x = calculate_centered_x(full_score_text, width, char_width)

        # Draw team 1 score
        graphics.DrawText(canvas, font, start_x, y_text, green, score1_text)

        # Calculate position for dash (after score1)
        dash_x = start_x + len(score1_text) * char_width
        graphics.DrawText(canvas, font, dash_x, y_text, white, " - ")

        # Calculate position for score2 (after dash)
        score2_x = dash_x + 3 * char_width  # " - " is 3 characters
        graphics.DrawText(canvas, font, score2_x, y_text, green, score2_text)

        # Determine last line text based on status
        if event.status_type == "STATUS_FINAL":
            last_line_text = event.winner_text
        else:
            last_line_text = event.status[:10]  # Truncate if too long

    # Display status on third line, centered
    y_status = 31
    last_line_x = calculate_centered_x(last_line_text, width)
    graphics.DrawText(canvas, font, last_line_x, y_status, white, last_line_text)

    canvas = matrix.SwapOnVSync(canvas)


if __name__ == "__main__":
    from api.sports_api import fetch_scores

    print("Testing display module...")
    data = fetch_scores()

    if data:
        display_scores(data)
    else:
        print("Failed to fetch data")
