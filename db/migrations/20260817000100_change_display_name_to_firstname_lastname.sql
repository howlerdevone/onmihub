-- migrate:up

ALTER TABLE identity.users
DROP COLUMN display_name,
ADD COLUMN firstname TEXT,
ADD COLUMN lastname TEXT;

-- migrate:down

ALTER TABLE identity.users
DROP COLUMN firstname,
DROP COLUMN lastname,
ADD COLUMN display_name TEXT;