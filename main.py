#!/usr/bin/env python3
"""    
    This is the main module of the program.
"""
from api import fetch_scores

def main():
    """
        Main function to execute the program.
    """
    # Get sports scores
    sports_data = fetch_scores()
    if sports_data:
        for event in sports_data.events:
            print(f"{event.team_one.full_name} vs {event.team_two.full_name} - Status: {event.status}")

if __name__ == "__main__":
    """
        Entry point of the program.
    """
    main()
