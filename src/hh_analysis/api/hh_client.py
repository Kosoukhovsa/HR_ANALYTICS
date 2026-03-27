import requests

from hh_analysis.config.settings import HH_API_BASE_URL, REQUEST_TIMEOUT


def get_areas() -> list:
    """Fetch HH areas reference."""
    response = requests.get(f"{HH_API_BASE_URL}/areas", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()
