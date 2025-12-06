#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Team:
    """Represents a team in a sports event."""

    id: str
    badge: str
    location: str
    name: str
    score: int

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


@dataclass
class SportsData:
    """Container for all sports events."""

    events: list[Event]
