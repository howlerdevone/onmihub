-- migrate:up

ALTER TABLE auth.users
DROP COLUMN display_name,
ADD COLUMN firstname TEXT,
ADD COLUMN lastname TEXT;

-- migrate:down

ALTER TABLE auth.users
DROP COLUMN firstname,
DROP COLUMN lastname,
ADD COLUMN display_name TEXT;