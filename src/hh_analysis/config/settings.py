from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DIR = DATA_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

HH_API_BASE_URL = "https://api.hh.ru"
REQUEST_TIMEOUT = 30

HH_AREAS_URL = "https://api.hh.ru/areas"

# Параметры поиска
SEARCH_TEXT = "postgresql"
AREA_IDS = [2]  # Example: 1 = Moscow. Later you can load area ids from Postgres.
PER_PAGE = 100
MAX_PAGES_PER_AREA = 20
PERIOD_DAYS = None
ONLY_WITH_SALARY = False
REQUEST_PAUSE_SECONDS = 0.5
PERIOD_DATE_FROM = datetime(2026, 3, 26)
PERIOD_DATE_TO = datetime(2026, 3, 31)

