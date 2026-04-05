-- Заполнение подробного описания работодателей
-- Из таблицы вакансий raw.hh_vacancy

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

-- Заполнение типа работодателя из таблицы raw.hh_employer_detail 

insert into stg.employer (
	employer_id,
	"type"
)
select 
employer_id,
employer_detail_json ->> 'type' as type
from raw.hh_employer_detail
where nullif( trim( employer_detail_json ->> 'type'), '') is not null 
on conflict(employer_id) 
do update set 
 	"type" = excluded."type"
;

-- Заполнить таблицу отраслей для работодателей

insert into stg.employer_industry (
    employer_id,
    industry_name
)
select
    d.employer_id,
    trim(ks.value->>'name') as industry_name
from raw.hh_employer_detail d
cross join lateral jsonb_array_elements(d.employer_detail_json->'industries') as ks(value)
where d.employer_detail_json ? 'industries'
  and jsonb_typeof(d.employer_detail_json->'industries') = 'array'
  and nullif(trim(ks.value->>'name'), '') is not null
on conflict do nothing
;




