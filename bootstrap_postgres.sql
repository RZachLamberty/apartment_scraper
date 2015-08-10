-- make sure the user exists
DO
$body$
BEGIN
IF NOT EXISTS (
SELECT *
FROM pg_catalog.pg_user
WHERE usename = 'apartments'
) THEN
CREATE ROLE apartments LOGIN PASSWORD 'apartments';
END IF;
END
$body$
;

-- create the database
CREATE DATABASE apartments OWNER apartments;

-- connect to the database we just created
\c apartments

-- create the raw_data table
BEGIN;
CREATE TABLE raw_data (
  title text,
  city text,
  url text PRIMARY KEY,
  price money,
  bedrooms real,
  maplink text,
  longitude real,
  latitude real,
  updated_on timestamptz,
  content text,
  image_links text[],
  attributes text[],
  size text,
  parsed_on timestamp
);
COMMIT;

BEGIN;
GRANT ALL PRIVILEGES ON TABLE raw_data TO apartments;
COMMIT;
