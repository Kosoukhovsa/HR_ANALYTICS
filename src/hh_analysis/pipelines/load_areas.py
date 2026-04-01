import json

from hh_analysis.config.settings import INTERIM_DATA_DIR
from hh_analysis.storage.postgres import get_connection


def load_data():
    file_path = INTERIM_DATA_DIR / "areas_flat.json"

    with open(file_path, encoding="utf-8") as f:
        areas = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO mart.dim_area (area_id, parent_area_id, area_name, area_level)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (area_id) DO NOTHING
    """

    rows = [
        (
            a["area_id"],
            a["parent_area_id"],
            a["area_name"],
            a["level"]
        )
        for a in areas
    ]

    cur.executemany(query, rows)

    conn.commit()

    cur.close()
    conn.close()

    print(f"Inserted {len(rows)} areas")


def main():
    load_data()


if __name__ == "__main__":
    main()