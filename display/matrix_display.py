#!/usr/bin/env python3
"""Display module for showing sports scores."""

import time
from collections import defaultdict

from config import DISPLAY_MODE, EVENT_DISPLAY_TIME, LEAGUE_DISPLAY_TIME
from models import SportsData


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

    # Determine which display method to use
    if DISPLAY_MODE == "matrix":
        _display_on_matrix(data)
    else:
        _display_on_console(data)


def _display_on_console(data: SportsData) -> None:
    """Display scores to console for testing."""
    # Group events by league
    leagues = defaultdict(list)
    for event in data.events:
        leagues[event.league].append(event)

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


def _display_on_matrix(data: SportsData) -> None:
    """Display scores on RGB matrix."""
    # TODO: Implement RGB matrix display logic
    # This will use the rgbmatrix library to render to the LED matrix
    print("Matrix display not yet implemented - falling back to console")
    _display_on_console(data)


if __name__ == "__main__":
    from api.sports_api import fetch_scores

    print("Testing display module...")
    data = fetch_scores()

    if data:
        display_scores(data)
    else:
        print("Failed to fetch data")
