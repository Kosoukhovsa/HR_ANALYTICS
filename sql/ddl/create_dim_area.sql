CREATE TABLE IF NOT EXISTS dim_area (
    area_id INTEGER PRIMARY KEY,
    parent_area_id INTEGER,
    area_name TEXT NOT NULL,
    area_level INTEGER NOT NULL
);
