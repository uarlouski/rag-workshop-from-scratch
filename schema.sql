-- Drop the chunks table if it exists
DROP TABLE IF EXISTS chunks;

-- Drop the vector extension if it exists
DROP EXTENSION IF EXISTS vector;

-- Create the vector extension
CREATE EXTENSION vector;

-- Create the chunks table
CREATE TABLE chunks (
    id bigserial PRIMARY KEY,
    embedding vector(384),
    chunk TEXT
);