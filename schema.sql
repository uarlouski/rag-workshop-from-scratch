CREATE EXTENSION vector;

CREATE TABLE chunks (id bigserial PRIMARY KEY, embedding vector(3072), chunk TEXT);
