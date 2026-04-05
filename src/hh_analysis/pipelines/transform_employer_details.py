from pathlib import Path

from hh_analysis.storage.postgres import get_connection
from hh_analysis.config.settings import BASE_DIR


def run_transform() -> None:
    """
    Execute SQL transformation for vacancy details.
    """

    sql_path = BASE_DIR / "sql" / "dml" / "transform_employer_details.sql"

    sql = sql_path.read_text()

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(sql)

        conn.commit()

        print("Transform completed successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def main() -> None:
    run_transform()


if __name__ == "__main__":
    main()