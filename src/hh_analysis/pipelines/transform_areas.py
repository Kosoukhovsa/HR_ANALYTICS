import json
from pathlib import Path

from hh_analysis.config.settings import RAW_DATA_DIR, INTERIM_DATA_DIR
from hh_analysis.transform.areas import flatten_areas
from hh_analysis.storage.files import save_json


def main():

    raw_file = sorted(RAW_DATA_DIR.glob("areas_*.json"))[-1]

    with open(raw_file, encoding="utf-8") as f:
        areas = json.load(f)

    flat = flatten_areas(areas)

    output_path = INTERIM_DATA_DIR / "areas_flat.json"

    save_json(flat, output_path)

    print(f"Flattened areas saved to {output_path}")
    print(f"Total areas: {len(flat)}")


if __name__ == "__main__":
    main()