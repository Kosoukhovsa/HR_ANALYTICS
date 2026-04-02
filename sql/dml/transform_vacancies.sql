-- EMPLOYEES
with ranked as (
    select
        vacancy_json,
        row_number() over (
            partition by vacancy_json->'employer'->>'id'
            order by loaded_at desc) as rn
    from raw.hh_vacancy    
)

insert into stg.employer (
    employer_id,
    employer_name,
    employer_url,
    employer_alternate_url,
    vacancies_url,
    country_id,
    accredited_it_employer,
    trusted
)

select distinct

    nullif(vacancy_json->'employer'->>'id','')::bigint,
    vacancy_json->'employer'->>'name',
    vacancy_json->'employer'->>'url',
    vacancy_json->'employer'->>'alternate_url',
    vacancy_json->'employer'->>'vacancies_url',

    nullif(vacancy_json->'employer'->>'country_id','')::integer,
    (vacancy_json->'employer'->>'accredited_it_employer')::boolean,
    (vacancy_json->'employer'->>'trusted')::boolean

from ranked
where rn = 1 and
    vacancy_json->'employer' is not null and
    nullif(vacancy_json->'employer'->>'id','') is not null

on conflict (employer_id)
do update set
    employer_name = excluded.employer_name,
    employer_url = excluded.employer_url,
    employer_alternate_url = excluded.employer_alternate_url,
    vacancies_url = excluded.vacancies_url,
    country_id = excluded.country_id,
    accredited_it_employer = excluded.accredited_it_employer,
    trusted = excluded.trusted;

-- VACANCIES
with ranked as (
    select
        vacancy_id,
        vacancy_json,
        loaded_at,
        area_id,
        search_text,
        page,
        source_file,
        row_number() over (
            partition by vacancy_id
            order by loaded_at desc
        ) as rn
    from raw.hh_vacancy
)

insert into stg.vacancy (

    vacancy_id,
    vacancy_name,
    premium,
    has_test,
    response_letter_required,

    area_id,
    area_name,

    salary_from,
    salary_to,
    salary_currency,
    salary_gross,

    published_at,
    created_at,
    archived,

    alternate_url,
    apply_alternate_url,

    snippet_requirement,
    snippet_responsibility,

    schedule_id,
    schedule_name,

    experience_id,
    experience_name,

    employment_id,
    employment_name,

    employment_form_id,
    employment_form_name,

    internship,
    accept_temporary,
    accept_labor_contract,
    accept_incomplete_resumes,
    night_shifts,

    employer_id,

    raw_loaded_at,
    raw_area_id,
    raw_search_text,
    raw_page,
    raw_source_file
)

select

    vacancy_id,

    vacancy_json->>'name',
    (vacancy_json->>'premium')::boolean,
    (vacancy_json->>'has_test')::boolean,
    (vacancy_json->>'response_letter_required')::boolean,

    nullif(vacancy_json->'area'->>'id','')::integer,
    vacancy_json->'area'->>'name',

    nullif(vacancy_json->'salary'->>'from','')::numeric,
    nullif(vacancy_json->'salary'->>'to','')::numeric,
    vacancy_json->'salary'->>'currency',
    (vacancy_json->'salary'->>'gross')::boolean,

    nullif(vacancy_json->>'published_at','')::timestamptz,
    nullif(vacancy_json->>'created_at','')::timestamptz,
    (vacancy_json->>'archived')::boolean,

    vacancy_json->>'alternate_url',
    vacancy_json->>'apply_alternate_url',

    vacancy_json->'snippet'->>'requirement',
    vacancy_json->'snippet'->>'responsibility',

    vacancy_json->'schedule'->>'id',
    vacancy_json->'schedule'->>'name',

    vacancy_json->'experience'->>'id',
    vacancy_json->'experience'->>'name',

    vacancy_json->'employment'->>'id',
    vacancy_json->'employment'->>'name',

    vacancy_json->'employment_form'->>'id',
    vacancy_json->'employment_form'->>'name',

    (vacancy_json->>'internship')::boolean,
    (vacancy_json->>'accept_temporary')::boolean,
    (vacancy_json->>'accept_labor_contract')::boolean,
    (vacancy_json->>'accept_incomplete_resumes')::boolean,
    (vacancy_json->>'night_shifts')::boolean,

    nullif(vacancy_json->'employer'->>'id','')::bigint,

    loaded_at,
    area_id,
    search_text,
    page,
    source_file

from ranked
where rn = 1

on conflict (vacancy_id)
do update set
    vacancy_name = excluded.vacancy_name,
    premium = excluded.premium,
    has_test = excluded.has_test,
    response_letter_required = excluded.response_letter_required,
    area_id = excluded.area_id,
    area_name = excluded.area_name,
    salary_from = excluded.salary_from,
    salary_to = excluded.salary_to,
    salary_currency = excluded.salary_currency,
    salary_gross = excluded.salary_gross,
    published_at = excluded.published_at,
    created_at = excluded.created_at,
    archived = excluded.archived,
    alternate_url = excluded.alternate_url,
    apply_alternate_url = excluded.apply_alternate_url,
    snippet_requirement = excluded.snippet_requirement,
    snippet_responsibility = excluded.snippet_responsibility,
    schedule_id = excluded.schedule_id,
    schedule_name = excluded.schedule_name,
    experience_id = excluded.experience_id,
    experience_name = excluded.experience_name,
    employment_id = excluded.employment_id,
    employment_name = excluded.employment_name,
    employment_form_id = excluded.employment_form_id,
    employment_form_name = excluded.employment_form_name,
    internship = excluded.internship,
    accept_temporary = excluded.accept_temporary,
    accept_labor_contract = excluded.accept_labor_contract,
    accept_incomplete_resumes = excluded.accept_incomplete_resumes,
    night_shifts = excluded.night_shifts,
    employer_id = excluded.employer_id,
    raw_loaded_at = excluded.raw_loaded_at,
    raw_area_id = excluded.raw_area_id,
    raw_search_text = excluded.raw_search_text,
    raw_page = excluded.raw_page,
    raw_source_file = excluded.raw_source_file;