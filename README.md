# hh_analysis

Проект для загрузки, хранения и анализа вакансий HH.ru.

hh_analysis/
│
├── README.md                # описание проекта
├── requirements.txt         # зависимости Python
├── .env                     # переменные окружения
├── .gitignore               # правила игнорирования Git
│
├── notebooks/               # Jupyter notebooks для анализа
│   └── .gitkeep
│
├── data/                    # данные проекта
│   ├── raw/                 # сырые данные из API
│   ├── interim/             # промежуточные данные
│   ├── processed/           # готовые для анализа данные
│   └── exports/             # выгрузки результатов
│
├── logs/                    # логи ETL процессов
│   └── .gitkeep
│
├── sql/                     # SQL скрипты
│   ├── ddl/                 # создание таблиц
│   ├── dml/                 # загрузка данных
│   └── queries/             # аналитические SQL запросы
│
├── scripts/                 # вспомогательные скрипты
│   └── .gitkeep
│
├── tests/                   # тесты проекта
│   └── .gitkeep
│
└── src/                     # исходный код Python
    └── hh_analysis/         # основной Python пакет
        │
        ├── __init__.py
        │
        ├── config/          # настройки проекта
        │   └── settings.py
        │
        ├── api/             # работа с HH API
        │   └── hh_client.py
        │
        ├── storage/         # работа с хранилищами
        │   ├── files.py
        │   └── postgres.py
        │
        ├── transform/       # преобразование данных
        │   ├── areas.py
        │   └── vacancies.py
        │
        ├── pipelines/       # ETL пайплайны
        │   ├── load_areas.py
        │   └── load_vacancies.py
        │
        ├── models/          # модели данных
        │   └── schemas.py
        │
        └── utils/           # вспомогательные функции
            └── logger.py



| Папка                        | Назначение               | Что хранится                                         | Пример содержимого                               |
| ---------------------------- | ------------------------ | ---------------------------------------------------- | ------------------------------------------------ |
| `data/`                      | Хранилище данных проекта | Все данные, полученные и обработанные в проекте      | JSON, CSV, parquet                               |
| `data/raw/`                  | Сырые данные             | Данные из API без изменений                          | `areas_2026-03-26.json`, `vacancies_page_1.json` |
| `data/interim/`              | Промежуточные данные     | Частично обработанные данные                         | `areas_flat.csv`                                 |
| `data/processed/`            | Готовые данные           | Данные, готовые для анализа                          | `vacancies_clean.parquet`                        |
| `data/exports/`              | Экспорт результатов      | Итоговые выгрузки для пользователя                   | `skills_statistics.csv`                          |
| `notebooks/`                 | Исследовательский анализ | Jupyter notebooks для анализа данных                 | `vacancy_skill_analysis.ipynb`                   |
| `logs/`                      | Логи работы ETL          | Журналы выполнения скриптов                          | `load_vacancies.log`                             |
| `sql/`                       | SQL-скрипты проекта      | Скрипты для создания таблиц и аналитических запросов | `.sql`                                           |
| `sql/ddl/`                   | DDL-скрипты              | Создание структуры БД                                | `create_dim_area.sql`                            |
| `sql/dml/`                   | DML-скрипты              | Загрузка и изменение данных                          | `insert_dim_area.sql`                            |
| `sql/queries/`               | Аналитические SQL        | Запросы для анализа данных                           | `top_skills.sql`                                 |
| `scripts/`                   | Вспомогательные скрипты  | Скрипты для администрирования и запуска задач        | `init_db.sh`                                     |
| `tests/`                     | Тесты проекта            | Unit и integration тесты                             | `test_api.py`                                    |
| `src/`                       | Исходный код проекта     | Основной Python-код                                  | Python-модули                                    |
| `src/hh_analysis/`           | Python-пакет проекта     | Основная логика приложения                           | API, ETL, трансформации                          |
| `src/hh_analysis/config/`    | Конфигурация             | Настройки проекта                                    | `settings.py`                                    |
| `src/hh_analysis/api/`       | Работа с API             | Клиент для HH API                                    | `hh_client.py`                                   |
| `src/hh_analysis/storage/`   | Работа с хранилищами     | Сохранение и загрузка данных                         | `files.py`, `postgres.py`                        |
| `src/hh_analysis/transform/` | Трансформация данных     | Подготовка данных для анализа                        | `areas.py`, `vacancies.py`                       |
| `src/hh_analysis/pipelines/` | ETL-пайплайны            | Скрипты загрузки и обработки данных                  | `load_areas.py`                                  |
| `src/hh_analysis/models/`    | Модели данных            | Схемы и структуры данных                             | `schemas.py`                                     |
| `src/hh_analysis/utils/`     | Утилиты                  | Общие вспомогательные функции                        | `logger.py`                                      |

## Назначение основных уровней архитектуры

| Уровень       | Назначение                             |
| ------------- | -------------------------------------- |
| **api**       | Получение данных из внешних источников |
| **pipelines** | Управление процессом загрузки данных   |
| **storage**   | Сохранение данных в файлы или БД       |
| **transform** | Очистка и преобразование данных        |
| **analysis**  | Анализ и визуализация                  |


## Поток данных в проекте

HH API
   ↓
api (запросы)
   ↓
pipelines (управление загрузкой)
   ↓
data/raw
   ↓
transform
   ↓
data/interim
   ↓
database / processed
   ↓
notebooks / sql/queries

## Куда добавлять новые компоненты

| Тип кода                | Куда добавлять                  |
| ----------------------- | ------------------------------- |
| Новый запрос к API      | `src/hh_analysis/api/`          |
| Новый ETL процесс       | `src/hh_analysis/pipelines/`    |
| Преобразование данных   | `src/hh_analysis/transform/`    |
| Работа с файлами или БД | `src/hh_analysis/storage/`      |
| Аналитический код       | `notebooks/` или `sql/queries/` |
