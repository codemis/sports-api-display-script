#!/usr/bin/env python3
"""
Main program for displaying sports scores in a continuous loop.
"""

import time

from api.sports_api import fetch_scores
from config import TRY_AGAIN_INTERVAL
from display import display_scores
from utils import is_sleep_time, time_until_wake


def main():
    """
    Main function to execute the program.
    Continuously fetches and displays sports scores.
    Respects sleep schedule configuration.
    """
    print("Starting sports score display...")

    while True:
        try:
            # Check if we're in sleep mode
            if is_sleep_time():
                sleep_seconds = time_until_wake()
                hours = sleep_seconds // 3600
                minutes = (sleep_seconds % 3600) // 60
                print("\n💤 Sleep mode - Display off until wake time")
                print(f"Sleeping for {hours}h {minutes}m...")
                time.sleep(sleep_seconds)
                print("🌅 Wake time - Resuming display...")
                continue

            # Fetch current scores
            print("\n\nFetching latest scores...")
            sports_data = fetch_scores()

            if sports_data:
                # Display all scores (organized by league)
                display_scores(sports_data)
            else:
                print("Failed to fetch scores. Retrying in 5 minutes...")
                time.sleep(TRY_AGAIN_INTERVAL)

        except KeyboardInterrupt:
            print("\n\nShutting down...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Retrying in 5 minutes...")
            time.sleep(TRY_AGAIN_INTERVAL)


if __name__ == "__main__":
    """
    Entry point of the program.
    """
    main()
