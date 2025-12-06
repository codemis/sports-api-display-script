#!/usr/bin/env python3

#  To test this code run `python3 -m api.sports_api` from the project root directory.
import requests

from config import API_URL
from models import Event, SportsData, Team


def fetch_scores() -> SportsData | None:
    """
    Fetch sports scores from the API.
    Returns:
        SportsData object containing events, or None if request fails.
    """
    if not API_URL:
        print("Error: API_URL not configured in .env file")

        return None

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Parse events from API response
        events = []
        for event_data in data.get("events", []):
            # Parse team data
            team_one_data = event_data.get("team_one", {})
            team_two_data = event_data.get("team_two", {})
            team_one = Team(
                id=team_one_data.get("id", ""),
                badge=team_one_data.get("badge", ""),
                location=team_one_data.get("location", ""),
                name=team_one_data.get("name", ""),
                score=team_one_data.get("score", 0),
            )
            team_two = Team(
                id=team_two_data.get("id", ""),
                badge=team_two_data.get("badge", ""),
                location=team_two_data.get("location", ""),
                name=team_two_data.get("name", ""),
                score=team_two_data.get("score", 0),
            )
            # Parse event data
            event = Event(
                id=event_data.get("id", ""),
                date=event_data.get("date", ""),
                time=event_data.get("time", ""),
                status=event_data.get("status", ""),
                status_type=event_data.get("status_type", ""),
                league=event_data.get("league", ""),
                league_badge=event_data.get("league_badge", ""),
                team_one=team_one,
                team_two=team_two,
            )
            events.append(event)

        return SportsData(events=events)

    except requests.Timeout:
        print("Error: API request timed out")
        return None

    except requests.RequestException as e:
        print(f"Error fetching scores from API: {e}")
        return None

    except (KeyError, ValueError, TypeError) as e:
        print(f"Error parsing API response data: {e}")
        return None


if __name__ == "__main__":
    # Test the API fetch
    print("Testing API fetch...")
    data = fetch_scores()
    if data:
        print(f"\nSuccessfully fetched {len(data.events)} event(s)")
        for event in data.events:
            print(
                f"\n{event.league}: {event.team_one.full_name} vs "
                f"{event.team_two.full_name}"
            )
            print(f"Status: {event.status}")
            print(f"Score: {event.team_one.score} - {event.team_two.score}")
            print(f"Date: {event.date} at {event.time}")
    else:
        print("Failed to fetch data")
