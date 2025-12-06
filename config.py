#!/usr/bin/env python3
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# API Configuration
API_URL = os.getenv("API_URL")
# Display Settings
# The number of seconds to display league info and each event (seconds)
LEAGUE_DISPLAY_TIME = int(os.getenv("LEAGUE_DISPLAY_TIME", 60))
EVENT_DISPLAY_TIME = int(os.getenv("EVENT_DISPLAY_TIME", 60))
# The interval to wait before retrying a failed API request (seconds)
TRY_AGAIN_INTERVAL = int(os.getenv("TRY_AGAIN_INTERVAL", 120))
# Sleep Schedule (PDT/PST - automatically handles daylight savings)
TIMEZONE = os.getenv("TIMEZONE", "America/Los_Angeles")
SLEEP_START_TIME = os.getenv("SLEEP_START_TIME", "23:00")
SLEEP_END_TIME = os.getenv("SLEEP_END_TIME", "07:00")

# Matrix Configuration
MATRIX_CONFIG = {
    "rows": 32,
    "cols": 64,
    "chain_length": 1,
    "parallel": 1,
    "hardware_mapping": "adafruit-hat-pwm",
    "gpio_slowdown": 2,
}

# Paths
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images"
# DEFAULT_FONT = FONTS_DIR / "7x13.bdf"
