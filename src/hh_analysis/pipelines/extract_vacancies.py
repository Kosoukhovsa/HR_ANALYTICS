"""Vacancy loading pipeline will live here."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Iterable

from hh_analysis.api.hh_client import get_vacancies_page
from hh_analysis.config.settings import RAW_DATA_DIR
from hh_analysis.storage.files import save_json


# ------------------------------------------------------------
# Temporary pilot settings.
# For the first stage it is simpler to define them here directly.
# Later they can be moved to config, CLI arguments, database, etc.
# ------------------------------------------------------------
SEARCH_TEXT = "data engineer"
AREA_IDS = [1]  # Example: 1 = Moscow. Later you can load area ids from Postgres.
PER_PAGE = 100
MAX_PAGES_PER_AREA = 3
PERIOD_DAYS = 30
ONLY_WITH_SALARY = False
REQUEST_PAUSE_SECONDS = 0.5


def build_page_file_path(
    load_dt: datetime,
    area_id: int,
    search_text: str,
    page: int,
) -> Path:
    """
    Build path for one raw vacancies page.

    Example:
    data/raw/vacancies/load_date=2026-03-30/text=data_engineer/area_id=1/page_000.json
    """
    safe_text = search_text.strip().lower().replace(" ", "_")
    return (
        RAW_DATA_DIR
        / "vacancies"
        / f"load_date={load_dt.date().isoformat()}"
        / f"text={safe_text}"
        / f"area_id={area_id}"
        / f"page_{page:03d}.json"
    )


def save_vacancies_page(
    page_data: dict,
    file_path: Path,
    *,
    area_id: int,
    search_text: str,
    page: int,
    per_page: int,
    loaded_at: str,
) -> None:
    """
    Save one API response page together with technical metadata.
    """
    payload = {
        "meta": {
            "loaded_at": loaded_at,
            "area_id": area_id,
            "search_text": search_text,
            "page": page,
            "per_page": per_page,
            "found": page_data.get("found"),
            "pages": page_data.get("pages"),
            "items_on_page": len(page_data.get("items", [])),
        },
        "response": page_data,
    }
    save_json(payload, file_path)


def extract_area_vacancies(
    *,
    area_id: int,
    search_text: str,
    load_dt: datetime,
    per_page: int = 100,
    max_pages: int = 1,
    period_days: int | None = None,
    only_with_salary: bool = False,
    pause_seconds: float = 0.0,
) -> None:
    """
    Extract vacancies for one area and save each page as raw JSON.
    """
    print(f"\n=== Area {area_id} | query='{search_text}' ===")

    for page in range(max_pages):
        page_data = get_vacancies_page(
            text=search_text,
            area=area_id,
            page=page,
            per_page=per_page,
            period=period_days,
            only_with_salary=only_with_salary,
        )

        total_pages = page_data.get("pages", 0)
        items_count = len(page_data.get("items", []))

        file_path = build_page_file_path(
            load_dt=load_dt,
            area_id=area_id,
            search_text=search_text,
            page=page,
        )

        save_vacancies_page(
            page_data=page_data,
            file_path=file_path,
            area_id=area_id,
            search_text=search_text,
            page=page,
            per_page=per_page,
            loaded_at=load_dt.isoformat(timespec="seconds"),
        )

        print(
            f"Saved page {page} "
            f"(items={items_count}, total_pages={total_pages}) -> {file_path}"
        )

        # Stop if API says there are no more pages.
        if total_pages == 0:
            print("No pages returned by API. Stop.")
            break

        if page >= total_pages - 1:
            print("Last available page reached. Stop.")
            break

        if pause_seconds > 0:
            sleep(pause_seconds)


def extract_vacancies(
    *,
    area_ids: Iterable[int],
    search_text: str,
    per_page: int = 100,
    max_pages_per_area: int = 1,
    period_days: int | None = None,
    only_with_salary: bool = False,
    pause_seconds: float = 0.0,
) -> None:
    """
    Extract vacancies for several areas.
    """
    load_dt = datetime.now()

    for area_id in area_ids:
        extract_area_vacancies(
            area_id=area_id,
            search_text=search_text,
            load_dt=load_dt,
            per_page=per_page,
            max_pages=max_pages_per_area,
            period_days=period_days,
            only_with_salary=only_with_salary,
            pause_seconds=pause_seconds,
        )


def main() -> None:
    extract_vacancies(
        area_ids=AREA_IDS,
        search_text=SEARCH_TEXT,
        per_page=PER_PAGE,
        max_pages_per_area=MAX_PAGES_PER_AREA,
        period_days=PERIOD_DAYS,
        only_with_salary=ONLY_WITH_SALARY,
        pause_seconds=REQUEST_PAUSE_SECONDS,
    )


if __name__ == "__main__":
    main()
