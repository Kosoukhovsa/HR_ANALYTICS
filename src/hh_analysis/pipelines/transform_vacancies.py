from pathlib import Path

from hh_analysis.storage.postgres import get_connection
from hh_analysis.config.settings import BASE_DIR


SQL_FILE = BASE_DIR / "sql/dml/transform_vacancies.sql"


def run_transform():

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            sql = SQL_FILE.read_text(encoding="utf-8")

            cur.execute(sql)

        conn.commit()

        print("Transformation completed")

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


def main():

    run_transform()


if __name__ == "__main__":
    main()