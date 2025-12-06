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

# Display Settings
# The number of seconds to display league info and each event
LEAGUE_DISPLAY_TIME = 2  # seconds
EVENT_DISPLAY_TIME = 2  # seconds
# The interval to wait before retrying a failed API request
TRY_AGAIN_INTERVAL = 60  # seconds

# Sleep Schedule (PDT/PST - automatically handles daylight savings)
TIMEZONE = "America/Los_Angeles"  # PDT/PST timezone
SLEEP_START_TIME = "20:30"  # Military time
SLEEP_END_TIME = "07:00"  # Military time
