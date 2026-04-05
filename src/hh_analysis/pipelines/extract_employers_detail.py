from datetime import datetime
import time
from typing import Any
from psycopg2.extras import Json, execute_values
from hh_analysis.api.hh_client import get_employer_detail
from hh_analysis.storage.postgres import get_connection

BATCH_SIZE = 10000
SLEEP_SECONDS = 0.5

def fetch_employer_ids(cur) -> list[int]:
    """
    Получить список работодателей из вакансий.
    """
    sql = """
    select
    distinct v.employer_id 
    from stg.vacancy v 
    left join stg.employer e on 
    v.employer_id = e.employer_id 
    where e.employer_id  is null
    limit %s
    """
    cur.execute(sql, (BATCH_SIZE,))
    rows = cur.fetchall()
    return [row[0] for row in rows if row[0] is not None]


def insert_employer_details_batch(cur, rows: list[tuple]) -> None:
    """
    Insert batch of employers details into raw.hh_employer_detail.
    """
    if not rows:
        return

    sql = """
    insert into raw.hh_employer_detail (
        loaded_at,
        employer_id,
        employer_detail_json
    )
    values %s
    on conflict (employer_id) do update
    set 
        loaded_at = excluded.loaded_at,
        employer_id = excluded.employer_id,
        employer_detail_json = excluded.employer_detail_json
    """

    execute_values(cur, sql, rows, page_size=100)


def run_extract() -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            employer_ids = fetch_employer_ids(cur)

        if not employer_ids:
            print("Нет работодателей для загрузки.")
            return

        print(f"Загружаем {len(employer_ids)} работодателей...")

        rows_to_insert = []

        for employer_id in employer_ids:
            try:
                employer_json = get_employer_detail(employer_id)

                rows_to_insert.append(
                    (
                        datetime.now(),
                        employer_id,
                        Json(employer_json),
                    )
                )

                print(f"OK employer_id={employer_id}")
                time.sleep(SLEEP_SECONDS)

            except Exception as e:
                print(f"ERROR vacancy_id={employer_id}: {e}")

        with conn.cursor() as cur:
            insert_employer_details_batch(cur, rows_to_insert)

        conn.commit()
        print(f"Вставлено строк: {len(rows_to_insert)}")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def main() -> None:
    run_extract()


if __name__ == "__main__":
    main()