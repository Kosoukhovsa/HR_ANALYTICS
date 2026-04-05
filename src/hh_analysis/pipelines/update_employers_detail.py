from hh_analysis.pipelines.extract_employers_detail import main as extract_employers_detail
from hh_analysis.pipelines.transform_employer_details import main as transform_employer_details


def main():
    # Загрузка детальных данных работодателя в raw.hh_employer_detail
    extract_employers_detail()
    # Загрузка из raw.hh_employer_detail в:
    # stg.employer_industry
    # Обновление поля type в таблице stg.employer 
    transform_employer_details()
  

if __name__ == '__main__':
    main()