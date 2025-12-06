#!/usr/bin/env python3
"""Utility functions for downloading and caching images."""

import hashlib
from pathlib import Path

import requests


def get_or_download_image(url: str, save_dir: Path) -> Path | None:
    """
    Download an image from URL and save it to the specified directory.
    If will return the existing file if already downloaded.
    Uses URL hash as filename to avoid duplicates.

    Args:
        url: The URL of the image to download
        save_dir: Directory to save the image

    Returns:
        Path to the downloaded image, or None if download failed
    """
    if not url:
        return None

    # Create directory if it doesn't exist
    save_dir.mkdir(parents=True, exist_ok=True)

    # Create filename from URL hash + extension
    url_hash = hashlib.md5(url.encode()).hexdigest()
    extension = url.split(".")[-1].split("?")[0]  # Handle query params
    if extension not in ["png", "jpg", "jpeg", "gif", "bmp"]:
        extension = "png"  # Default extension

    filepath = save_dir / f"{url_hash}.{extension}"

    # Return existing file if already downloaded
    if filepath.exists():
        return filepath

    # Download the image
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filepath

    except requests.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
        return None
