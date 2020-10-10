CREATE USER galleryadmin WITH encrypted password 'pass123';
GRANT all privileges ON DATABASE postgres TO galleryadmin;

DROP TABLE photos;
CREATE TABLE IF NOT EXISTS photos (
	id SERIAL PRIMARY KEY,
    name VARCHAR(100),
	description VARCHAR(1000),
	small_data BYTEA,
    medium_data BYTEA
);

GRANT all privileges ON TABLE photos TO galleryadmin;
GRANT all privileges ON TABLE photos_id_seq TO galleryadmin;
