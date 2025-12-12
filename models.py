#!/usr/bin/env python3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Team:
    """Represents a team in a sports event."""

    id: str
    badge: str
    location: str
    name: str
    abbreviation: str
    score: int
    badge_path: Path | None = field(default=None, repr=False)

    @property
    def full_name(self) -> str:
        """Returns the full team name (location + name)."""
        return f"{self.location} {self.name}"


@dataclass
class Event:
    """Represents a sports event/game."""

    id: str
    date: str
    time: str
    status: str
    status_type: str
    league: str
    league_badge: str
    team_one: Team
    team_two: Team
    league_badge_path: Path | None = field(default=None, repr=False)

    @property
    def is_scheduled(self) -> bool:
        """Check if event is scheduled."""
        return self.status_type == "STATUS_SCHEDULED"

    @property
    def is_in_progress(self) -> bool:
        """Check if event is currently in progress."""
        return self.status_type == "STATUS_IN_PROGRESS"

    @property
    def is_final(self) -> bool:
        """Check if event is finished."""
        return self.status_type == "STATUS_FINAL"

    @property
    def formatted_date(self) -> str:
        """
        Convert date from 'Dec 07 2025' format to 'Dec 7' format.

        Returns:
            Formatted date string without leading zeros and year
        """
        try:
            # Parse the date string
            date_obj = datetime.strptime(self.date, "%b %d %Y")
            # Format without leading zero in day
            return date_obj.strftime("%b %-d")
        except ValueError:
            # If parsing fails, return original date
            return self.date

    @property
    def winner_text(self) -> str:
        """
        Get the winner text for a final game.

        Returns:
            Text displaying the winner's name or "Tie!" if scores are equal
        """
        if self.team_one.score > self.team_two.score:
            return f"{self.team_one.name} win!"
        elif self.team_two.score > self.team_one.score:
            return f"{self.team_two.name} win!"
        else:
            return "Tie!"


@dataclass
class SportsData:
    """Container for all sports events."""

    events: list[Event]
