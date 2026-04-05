from hh_analysis.pipelines.update_areas import main as update_areas
from hh_analysis.pipelines.update_vacancies import main as update_vacancies
from hh_analysis.pipelines.update_vacancies_detail import main as update_vacancies_detail
from hh_analysis.pipelines.update_employers_detail import main as update_employers_detail
from hh_analysis.config.settings import (SEARCH_TEXT, 
                                            AREA_IDS, 
                                            PER_PAGE, 
                                            MAX_PAGES_PER_AREA,
                                            PERIOD_DAYS,
                                            ONLY_WITH_SALARY,
                                            REQUEST_PAUSE_SECONDS)


def main():

    print('*'*50)
    print(f'Обновление данных HH.RU c параметрами: SEARCH_TEXT: {SEARCH_TEXT}')
    print(f'\t\t\tAREA_IDS: {AREA_IDS}')
    print(f'\t\t\tPER_PAGE: {PER_PAGE}')
    print(f'\t\t\tMAX_PAGES_PER_AREA: {MAX_PAGES_PER_AREA}')
    print(f'\t\t\tPERIOD_DAYS: {PERIOD_DAYS}')
    print(f'\t\t\tONLY_WITH_SALARY: {ONLY_WITH_SALARY}')
    print(f'\t\t\tREQUEST_PAUSE_SECONDS: {REQUEST_PAUSE_SECONDS}')
    print('*'*50)


    # Обновить регионы
    update_areas()
    # Обновить вакансии
    update_vacancies()
    # Обновить детальные данные по вакансиям
    update_vacancies_detail()
    # Обновить данные работодателей 
    update_employers_detail()
  
    print('Обновление завершено')

if __name__ == '__main__':
    main()