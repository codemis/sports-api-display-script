#!/usr/bin/env python3
"""
Main program for displaying sports scores in a continuous loop.
"""

import time

from api.sports_api import fetch_scores
from config import TRY_AGAIN_INTERVAL
from display import display_scores


def main():
    """
    Main function to execute the program.
    Continuously fetches and displays sports scores.
    """
    print("Starting sports score display...")

    while True:
        try:
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
