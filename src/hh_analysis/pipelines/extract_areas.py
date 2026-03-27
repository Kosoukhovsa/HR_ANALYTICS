from datetime import date

from hh_analysis.api.hh_client import get_areas
from hh_analysis.config.settings import RAW_DATA_DIR
from hh_analysis.storage.files import save_json


def main() -> None:
    areas = get_areas()
    file_path = RAW_DATA_DIR / f"areas_{date.today()}.json"
    save_json(areas, file_path)
    print(f"Saved areas to: {file_path}")
    print(f"Top-level items: {len(areas)}")


if __name__ == "__main__":
    main()
