------------------------------------------------------------
-- SCHEMA RAW
-- Слой хранения сырых данных из источников
------------------------------------------------------------

create schema if not exists raw;

------------------------------------------------------------
-- TABLE raw.hh_vacancy
-- Сырые вакансии из HH API
-- 1 строка = 1 вакансия
------------------------------------------------------------

create table if not exists raw.hh_vacancy (

    raw_vacancy_id bigserial primary key,

    loaded_at timestamp not null,

    area_id integer not null,

    search_text text not null,

    page integer not null,

    per_page integer not null,

    vacancy_id bigint not null,

    vacancy_json jsonb not null,

    source_file text not null
);

------------------------------------------------------------
-- COMMENTS
------------------------------------------------------------

comment on table raw.hh_vacancy is
'Сырые данные вакансий HH API. Хранит JSON вакансии без преобразований.';

comment on column raw.hh_vacancy.raw_vacancy_id is
'Технический surrogate ключ записи raw слоя';

comment on column raw.hh_vacancy.loaded_at is
'Дата и время загрузки страницы вакансий из API';

comment on column raw.hh_vacancy.area_id is
'Код региона поиска вакансий в HH API';

comment on column raw.hh_vacancy.search_text is
'Поисковый запрос (например: data engineer)';

comment on column raw.hh_vacancy.page is
'Номер страницы результата поиска HH API';

comment on column raw.hh_vacancy.per_page is
'Количество вакансий на странице ответа API';

comment on column raw.hh_vacancy.vacancy_id is
'Уникальный идентификатор вакансии в HH';

comment on column raw.hh_vacancy.vacancy_json is
'Полный JSON объект вакансии, полученный из API HH';

comment on column raw.hh_vacancy.source_file is
'Имя JSON файла-источника, из которого была загружена запись';

------------------------------------------------------------
-- INDEXES
------------------------------------------------------------

create index if not exists ix_raw_hh_vacancy_vacancy_id
on raw.hh_vacancy(vacancy_id);

create index if not exists ix_raw_hh_vacancy_loaded_at
on raw.hh_vacancy(loaded_at);

create index if not exists ix_raw_hh_vacancy_area_id
on raw.hh_vacancy(area_id);

------------------------------------------------------------
-- Табдица hh_vacancy_detail для детальных вакансий
------------------------------------------------------------

create table if not exists raw.hh_vacancy_detail (
    raw_vacancy_detail_id bigserial primary key,
    loaded_at timestamp not null,
    vacancy_id bigint not null,
    vacancy_detail_json jsonb not null,
    source_system text not null default 'hh_api'
);

comment on table raw.hh_vacancy_detail is
'Сырые детальные вакансии HH API. 1 строка = 1 детальная вакансия.';

comment on column raw.hh_vacancy_detail.raw_vacancy_detail_id is
'Технический surrogate key записи raw detail слоя';

comment on column raw.hh_vacancy_detail.loaded_at is
'Дата и время загрузки детальной вакансии';

comment on column raw.hh_vacancy_detail.vacancy_id is
'Идентификатор вакансии HH';

comment on column raw.hh_vacancy_detail.vacancy_detail_json is
'Полный JSON детальной вакансии, полученный из endpoint /vacancies/{id}';

comment on column raw.hh_vacancy_detail.source_system is
'Источник данных';

create unique index if not exists ux_raw_hh_vacancy_detail_vacancy_id
on raw.hh_vacancy_detail(vacancy_id);

create index if not exists ix_raw_hh_vacancy_detail_loaded_at
on raw.hh_vacancy_detail(loaded_at);

------------------------------------------------------------
-- Табдица hh_employer_detail для детальных данных по работодателю
------------------------------------------------------------

create table if not exists raw.hh_employer_detail (
    raw_employer_detail_id bigserial primary key,
    loaded_at timestamp not null,
    employer_id bigint not null,
    employer_detail_json jsonb not null,
    source_system text not null default 'hh_api'
);

comment on table raw.hh_employer_detail is
'Сырые детальные работодателей HH API. 1 строка = 1 работодатель.';

comment on column raw.hh_employer_detail.raw_employer_detail_id is
'Технический surrogate key записи raw detail слоя';

comment on column raw.hh_employer_detail.loaded_at is
'Дата и время загрузки';

comment on column raw.hh_employer_detail.employer_id is
'Идентификатор работодателя HH';

comment on column raw.hh_employer_detail.employer_detail_json is
'Полный JSON работодателя, полученный из endpoint /employers/{id}';

comment on column raw.hh_employer_detail.source_system is
'Источник данных';

create unique index if not exists ux_raw_hh_employer_detail_employer_id
on raw.hh_employer_detail(employer_id);