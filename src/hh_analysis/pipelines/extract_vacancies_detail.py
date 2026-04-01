from datetime import datetime
import time
from typing import Any

from psycopg2.extras import Json, execute_values

from hh_analysis.api.hh_client import get_vacancy_detail
from hh_analysis.storage.postgres import get_connection


BATCH_SIZE = 40
SLEEP_SECONDS = 0.5


def fetch_vacancy_ids(cur) -> list[int]:
    """
    Get vacancy_ids that are not yet loaded into raw.hh_vacancy_detail.
    """
    sql = """
    select distinct r.vacancy_id
    from raw.hh_vacancy r
    left join raw.hh_vacancy_detail d
        on d.vacancy_id = r.vacancy_id
    where d.vacancy_id is null
    order by r.vacancy_id
    limit %s
    """
    cur.execute(sql, (BATCH_SIZE,))
    rows = cur.fetchall()
    return [row[0] for row in rows]


def insert_vacancy_details_batch(cur, rows: list[tuple]) -> None:
    """
    Insert batch of vacancy details into raw.hh_vacancy_detail.
    """
    if not rows:
        return

    sql = """
    insert into raw.hh_vacancy_detail (
        loaded_at,
        vacancy_id,
        vacancy_detail_json
    )
    values %s
    on conflict (vacancy_id) do nothing
    """

    execute_values(cur, sql, rows, page_size=100)


def run_extract() -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            vacancy_ids = fetch_vacancy_ids(cur)

        if not vacancy_ids:
            print("Нет новых вакансий для загрузки.")
            return

        print(f"Загружаем {len(vacancy_ids)} вакансий...")

        rows_to_insert = []

        for vacancy_id in vacancy_ids:
            try:
                vacancy_json = get_vacancy_detail(vacancy_id)

                rows_to_insert.append(
                    (
                        datetime.now(),
                        vacancy_id,
                        Json(vacancy_json),
                    )
                )

                print(f"OK vacancy_id={vacancy_id}")
                time.sleep(SLEEP_SECONDS)

            except Exception as e:
                print(f"ERROR vacancy_id={vacancy_id}: {e}")

        with conn.cursor() as cur:
            insert_vacancy_details_batch(cur, rows_to_insert)

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