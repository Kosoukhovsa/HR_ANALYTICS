from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hh_analysis.config.settings import RAW_DATA_DIR
from hh_analysis.storage.postgres import get_connection


VACANCIES_RAW_DIR = RAW_DATA_DIR / "vacancies"


def find_vacancy_page_files(base_dir: Path) -> list[Path]:
    """
    Find all vacancy page JSON files under the given directory.
    """
    return sorted(base_dir.rglob("page_*.json"))


def read_json_file(file_path: Path) -> dict[str, Any]:
    """
    Read one JSON file and return parsed payload.
    """
    return json.loads(file_path.read_text(encoding="utf-8"))


def build_raw_rows(payload: dict[str, Any], source_file: Path) -> list[tuple]:
    """
    Convert one saved page JSON into rows for raw.hh_vacancy.

    One vacancy = one row.
    """
    meta = payload["meta"]
    response = payload["response"]
    items = response.get("items", [])

    loaded_at = meta["loaded_at"]
    area_id = meta["area_id"]
    search_text = meta["search_text"]
    page = meta["page"]
    per_page = meta["per_page"]

    rows: list[tuple] = []

    for vacancy in items:
        vacancy_id = int(vacancy["id"])

        rows.append(
            (
                loaded_at,
                area_id,
                search_text,
                page,
                per_page,
                vacancy_id,
                json.dumps(vacancy, ensure_ascii=False),
                str(source_file),
            )
        )

    return rows


def insert_raw_rows(conn, rows: list[tuple]) -> int:
    """
    Insert rows into raw.hh_vacancy.

    Returns number of inserted rows.
    """
    if not rows:
        return 0

    insert_sql = """
        insert into raw.hh_vacancy (
            loaded_at,
            area_id,
            search_text,
            page,
            per_page,
            vacancy_id,
            vacancy_json,
            source_file
        )
        values (
            %s, %s, %s, %s, %s, %s, %s::jsonb, %s
        )
    """

    with conn.cursor() as cur:
        cur.executemany(insert_sql, rows)

    return len(rows)


def load_vacancy_files_to_raw(conn, base_dir: Path) -> None:
    """
    Load all vacancy page files from base_dir into raw.hh_vacancy.
    """
    files = find_vacancy_page_files(base_dir)

    if not files:
        print(f"No files found in: {base_dir}")
        return

    print(f"Found {len(files)} files")

    total_inserted = 0

    for file_path in files:
        payload = read_json_file(file_path)
        rows = build_raw_rows(payload, file_path)
        inserted = insert_raw_rows(conn, rows)
        total_inserted += inserted

        print(f"Loaded {inserted} vacancies from {file_path}")

    conn.commit()
    print(f"\nDone. Total inserted rows: {total_inserted}")


def main() -> None:
    conn = get_connection()

    try:
        load_vacancy_files_to_raw(
            conn=conn,
            base_dir=VACANCIES_RAW_DIR,
        )
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()