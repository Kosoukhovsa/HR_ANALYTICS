from hh_analysis.pipelines.extract_vacancies_new import main as extract_vacancies_new
from hh_analysis.pipelines.transform_vacancies import main as transform_vacancies
from hh_analysis.pipelines.load_vacancies_raw import main as load_vacancies_raw


def main():
    # Загрузка json файлов с вакансиями
    extract_vacancies_new()
    # Загрузка вакансий изфайлов в raw слой БД
    load_vacancies_raw()
    # Загрузка и преобразование данных из raw в stg слой БД 
    transform_vacancies()
  

if __name__ == '__main__':
    main()