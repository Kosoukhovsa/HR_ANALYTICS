------------------------------------------------------------
-- SCHEMA STG
-- Слой нормализованных данных
------------------------------------------------------------

create schema if not exists stg;

------------------------------------------------------------
-- TABLE stg.vacancy
-- Нормализованные данные вакансий
------------------------------------------------------------

create table if not exists stg.vacancy (

    vacancy_id bigint primary key,

    vacancy_name text,

    premium boolean,
    has_test boolean,
    response_letter_required boolean,

    area_id integer,
    area_name text,

    salary_from numeric,
    salary_to numeric,
    salary_currency text,
    salary_gross boolean,

    published_at timestamptz,
    created_at timestamptz,
    archived boolean,

    alternate_url text,
    apply_alternate_url text,

    snippet_requirement text,
    snippet_responsibility text,

    schedule_id text,
    schedule_name text,

    experience_id text,
    experience_name text,

    employment_id text,
    employment_name text,

    employment_form_id text,
    employment_form_name text,

    internship boolean,
    accept_temporary boolean,
    accept_labor_contract boolean,
    accept_incomplete_resumes boolean,
    night_shifts boolean,

    employer_id bigint,

    raw_loaded_at timestamp,
    raw_area_id integer,
    raw_search_text text,
    raw_page integer,
    raw_source_file text
);

------------------------------------------------------------
-- COMMENTS vacancy
------------------------------------------------------------

comment on table stg.vacancy is
'Нормализованные данные вакансий, извлеченные из raw JSON';

comment on column stg.vacancy.vacancy_id is
'Уникальный идентификатор вакансии HH';

comment on column stg.vacancy.vacancy_name is
'Название вакансии';

comment on column stg.vacancy.premium is
'Флаг премиальной вакансии';

comment on column stg.vacancy.has_test is
'Требуется ли тестовое задание';

comment on column stg.vacancy.response_letter_required is
'Требуется ли сопроводительное письмо';

comment on column stg.vacancy.area_id is
'Идентификатор региона вакансии';

comment on column stg.vacancy.area_name is
'Название региона вакансии';

comment on column stg.vacancy.salary_from is
'Минимальная зарплата';

comment on column stg.vacancy.salary_to is
'Максимальная зарплата';

comment on column stg.vacancy.salary_currency is
'Валюта зарплаты';

comment on column stg.vacancy.salary_gross is
'Флаг: зарплата до вычета налогов';

comment on column stg.vacancy.published_at is
'Дата публикации вакансии';

comment on column stg.vacancy.created_at is
'Дата создания вакансии в системе HH';

comment on column stg.vacancy.archived is
'Флаг архивной вакансии';

comment on column stg.vacancy.alternate_url is
'URL страницы вакансии на сайте HH';

comment on column stg.vacancy.apply_alternate_url is
'URL отклика на вакансию';

comment on column stg.vacancy.snippet_requirement is
'Фрагмент текста требований к кандидату';

comment on column stg.vacancy.snippet_responsibility is
'Фрагмент текста обязанностей';

comment on column stg.vacancy.schedule_id is
'Идентификатор типа графика работы';

comment on column stg.vacancy.schedule_name is
'Название графика работы';

comment on column stg.vacancy.experience_id is
'Идентификатор уровня опыта';

comment on column stg.vacancy.experience_name is
'Описание уровня опыта';

comment on column stg.vacancy.employment_id is
'Идентификатор типа занятости';

comment on column stg.vacancy.employment_name is
'Описание типа занятости';

comment on column stg.vacancy.employment_form_id is
'Идентификатор формы занятости';

comment on column stg.vacancy.employment_form_name is
'Описание формы занятости';

comment on column stg.vacancy.internship is
'Флаг стажировки';

comment on column stg.vacancy.accept_temporary is
'Допускается временная работа';

comment on column stg.vacancy.accept_labor_contract is
'Допускается работа по трудовому договору';

comment on column stg.vacancy.accept_incomplete_resumes is
'Разрешены неполные резюме';

comment on column stg.vacancy.night_shifts is
'Возможны ночные смены';

comment on column stg.vacancy.employer_id is
'Идентификатор работодателя';

comment on column stg.vacancy.raw_loaded_at is
'Дата загрузки записи в raw слой';

comment on column stg.vacancy.raw_area_id is
'Регион поиска вакансий';

comment on column stg.vacancy.raw_search_text is
'Поисковый запрос';

comment on column stg.vacancy.raw_page is
'Номер страницы выдачи';

comment on column stg.vacancy.raw_source_file is
'Имя файла источника JSON';

------------------------------------------------------------
-- TABLE stg.employer - работодатели
------------------------------------------------------------

create table if not exists stg.employer (

    employer_id bigint primary key,

    employer_name text,

    employer_url text,
    employer_alternate_url text,
    vacancies_url text,

    country_id integer,
    accredited_it_employer boolean,
    trusted boolean
);

------------------------------------------------------------
-- COMMENTS employer
------------------------------------------------------------

comment on table stg.employer is
'Справочник работодателей из HH API';

comment on column stg.employer.employer_id is
'Уникальный идентификатор работодателя';

comment on column stg.employer.employer_name is
'Название работодателя';

comment on column stg.employer.employer_url is
'API URL работодателя';

comment on column stg.employer.employer_alternate_url is
'URL страницы работодателя на сайте HH';

comment on column stg.employer.vacancies_url is
'URL списка вакансий работодателя';

comment on column stg.employer.country_id is
'Код страны работодателя';

comment on column stg.employer.accredited_it_employer is
'Флаг аккредитованной IT компании';

comment on column stg.employer.trusted is
'Флаг проверенного работодателя';

------------------------------------------------------------
-- vacancy_professional_role - профессиональные роли вакансий
------------------------------------------------------------

create table if not exists stg.vacancy_professional_role (
    vacancy_id bigint not null,
    professional_role_id integer not null,
    professional_role_name text,
    primary key (vacancy_id, professional_role_id)
);

comment on table stg.vacancy_professional_role is
'Связь вакансии и профессиональной роли HH';

comment on column stg.vacancy_professional_role.vacancy_id is
'Идентификатор вакансии';

comment on column stg.vacancy_professional_role.professional_role_id is
'Идентификатор профессиональной роли';

comment on column stg.vacancy_professional_role.professional_role_name is
'Название профессиональной роли из вакансии';

------------------------------------------------------------
-- vacancy_skill - ключевые навыки вакансий
------------------------------------------------------------

create table if not exists stg.vacancy_skill (
    vacancy_id bigint not null,
    skill_name text not null,
    primary key (vacancy_id, skill_name)
);

comment on table stg.vacancy_skill is
'Связь вакансии и ключевого навыка из детальной вакансии HH';

comment on column stg.vacancy_skill.vacancy_id is
'Идентификатор вакансии';

comment on column stg.vacancy_skill.skill_name is
'Название ключевого навыка';

------------------------------------------------------------
-- vacancy_detail - подробное описание вакансии
------------------------------------------------------------

create table if not exists stg.vacancy_detail (
    vacancy_id bigint primary key,
    vacancy_description text 
);

comment on table stg.vacancy_detail is
'Детальное описание вакансии';

comment on column stg.vacancy_detail.vacancy_id is
'Идентификатор вакансии';

comment on column stg.vacancy_detail.vacancy_description is
'Описание вакансии';

------------------------------------------------------------
-- html_to_text - функция для преобразования HTML в текст
------------------------------------------------------------

create schema if not exists utils; 


CREATE OR REPLACE FUNCTION html_to_text(html_text text)
RETURNS text AS $$
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text("\n")
$$ LANGUAGE plpython3u;
