from hh_analysis.api.hh_client import get_vacancies_page
from datetime import datetime


def main():
    search_text = 'аналитик'
    area_id = 2
    page_0 = get_vacancies_page(
                text=search_text,
                area=area_id,
                page=0,
                per_page=100,
                period=None,                
                only_with_salary=0,
                date_from=datetime(2026, 3, 25),
                date_to=datetime(2026, 4, 2),
                )

    total_pages = page_0.get("pages", 0)
    found_items = page_0.get("found", 0)

    print(f"Всего страниц {total_pages}")
    print(f"Всего вакансий {found_items}")

if __name__ == "__main__":
    main()