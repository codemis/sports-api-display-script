#!/usr/bin/env python3
"""Utilities for managing display sleep schedule."""

from datetime import datetime
from datetime import time as dt_time
from zoneinfo import ZoneInfo

from config import SLEEP_END_TIME, SLEEP_START_TIME, TIMEZONE


def parse_military_time(time_str: str) -> dt_time:
    """
    Parse military time string (HH:MM) to time object.

    Args:
        time_str: Time in military format (e.g., "23:00", "07:30")

    Returns:
        time object
    """
    hour, minute = map(int, time_str.split(":"))
    return dt_time(hour, minute)


def is_sleep_time() -> bool:
    """
    Check if current time falls within the sleep schedule.
    Handles overnight sleep periods (e.g., 23:00 to 07:00).
    Uses configured timezone with automatic daylight savings handling.

    Returns:
        True if display should be sleeping, False otherwise
    """
    tz = ZoneInfo(TIMEZONE)
    current_time = datetime.now(tz).time()

    sleep_start = parse_military_time(SLEEP_START_TIME)
    sleep_end = parse_military_time(SLEEP_END_TIME)

    # Handle overnight sleep period (e.g., 23:00 to 07:00)
    if sleep_start > sleep_end:
        return current_time >= sleep_start or current_time < sleep_end
    # Handle same-day sleep period (e.g., 14:00 to 16:00)
    else:
        return sleep_start <= current_time < sleep_end


def time_until_wake() -> int:
    """
    Calculate seconds until the display should wake up.

    Returns:
        Number of seconds to sleep
    """
    tz = ZoneInfo(TIMEZONE)
    now = datetime.now(tz)

    sleep_end = parse_military_time(SLEEP_END_TIME)
    wake_time = now.replace(
        hour=sleep_end.hour, minute=sleep_end.minute, second=0, microsecond=0
    )

    # If wake time is earlier today, it must be tomorrow
    if wake_time <= now:
        from datetime import timedelta

        wake_time += timedelta(days=1)

    seconds = int((wake_time - now).total_seconds())
    return seconds


if __name__ == "__main__":
    print(f"Timezone: {TIMEZONE}")
    print(f"Sleep schedule: {SLEEP_START_TIME} to {SLEEP_END_TIME}")
    print(f"Is sleep time? {is_sleep_time()}")

    if is_sleep_time():
        seconds = time_until_wake()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        print(f"Time until wake: {hours}h {minutes}m ({seconds} seconds)")

    tz = ZoneInfo(TIMEZONE)
    current_time_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"Current time ({TIMEZONE}): {current_time_str}")
