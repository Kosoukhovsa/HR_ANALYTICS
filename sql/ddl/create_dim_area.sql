create table if not exists dim_area (
    area_id           integer primary key,
    area_name         text not null,
    area_type         text,
    parent_area_id    integer,
    parent_area_name  text,
    country_id        integer,
    country_name      text,
    region_id         integer,
    region_name       text,
    path_text         text,
    level_num         integer
);
