
create schema if not exists mart;

CREATE TABLE IF NOT EXISTS mart.dim_area (
    area_id INTEGER PRIMARY KEY,
    parent_area_id INTEGER,
    area_name TEXT NOT NULL,
    area_level INTEGER NOT NULL
);

create table if not exists mart.professional_role (
    professional_role_id integer primary key,
    professional_role_name text not null,
    category_id integer,
    category_name text
);

comment on table mart.professional_role is
'Справочник профессиональных ролей HH';

comment on column mart.professional_role.professional_role_id is
'Идентификатор профессиональной роли HH';

comment on column mart.professional_role.professional_role_name is
'Название профессиональной роли';

comment on column mart.professional_role.category_id is
'Идентификатор категории профессиональных ролей';

comment on column mart.professional_role.category_name is
'Название категории профессиональных ролей';




