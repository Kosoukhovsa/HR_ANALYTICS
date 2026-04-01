from hh_analysis.api.hh_client import get_vacancy_detail
""" Это тестовый скрипт для проверки загрузки детальной вакансии
Запуск в терминале: 
PYTHONPATH=src python -m hh_analysis.pipelines.test_vacancy_detail
"""

def main() -> None:
    vacancy_id = 131646127
    vacancy = get_vacancy_detail(vacancy_id)

    print("id:", vacancy.get("id"))
    print("name:", vacancy.get("name"))
    print("key_skills:", vacancy.get("key_skills"))
    print("description exists:", "description" in vacancy)


if __name__ == "__main__":
    main()