-- Заполнить таблицу ключевых навыков для вакансий

insert into stg.vacancy_skill (
    vacancy_id,
    skill_name
)
select
    d.vacancy_id,
    trim(ks.value->>'name') as skill_name
from raw.hh_vacancy_detail d
cross join lateral jsonb_array_elements(d.vacancy_detail_json->'key_skills') as ks(value)
where d.vacancy_detail_json ? 'key_skills'
  and jsonb_typeof(d.vacancy_detail_json->'key_skills') = 'array'
  and nullif(trim(ks.value->>'name'), '') is not null
on conflict do nothing;

-- Заполнить таблицу профессиональных ролей для вакансий

insert into stg.vacancy_professional_role (
    vacancy_id,
    professional_role_id,
    professional_role_name
)
select
    d.vacancy_id,
    nullif(pr.value->>'id', '')::integer as professional_role_id,
    pr.value->>'name' as professional_role_name
from raw.hh_vacancy_detail d
cross join lateral jsonb_array_elements(d.vacancy_detail_json->'professional_roles') as pr(value)
where d.vacancy_detail_json ? 'professional_roles'
  and jsonb_typeof(d.vacancy_detail_json->'professional_roles') = 'array'
  and nullif(pr.value->>'id', '') is not null
on conflict do nothing;

-- Заполнить таблицу с описанием вакансий

insert into