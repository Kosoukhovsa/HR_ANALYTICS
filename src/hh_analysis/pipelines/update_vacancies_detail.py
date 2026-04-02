from hh_analysis.pipelines.extract_vacancies_detail import main as extract_vacancies_detail
from hh_analysis.pipelines.transform_vacancy_details import main as transform_vacancy_details


def main():
    # Загрузка детальных вакансий в raw.hh_vacancy_detail
    extract_vacancies_detail()
    # Загрузка из raw.hh_vacancy_detail в:
    # stg.vacancy_detail
    # stg.vacancy_professional_role
    # stg.vacancy_skill 

    transform_vacancy_details()
  

if __name__ == '__main__':
    main()