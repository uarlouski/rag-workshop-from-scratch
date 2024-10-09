# rag-demo

A bare bones RAG application for educational purposes.

DISCLAIMER: There are several concepts in this repository that can be implemented in much better ways.  The point of this repository is to remove unfamiliar terms and abstractions as much as possible to demonstrate the essential concepts of a RAG application.

## Setup:

Start a pgvector docker container:

```
docker run -p 6432:5432  --name pgvector -e POSTGRES_PASSWORD=postgres -d pgvector/pgvector:pg17
```

Note: The host port for the docker container is 6432 instead of the normal 5432 to avoid port collisions

Setup the database:
```
psql -h localhost -p 6432 -U postgres -c "CREATE DATABASE rag_demo;"
psql -h localhost -p 6432 -U postgres rag_demo < schema.sql
```

Export your OPENAI_API_KEY environment variable:
```
export OPENAI_API_KEY=sk-...
```

Poetry install:
```
poetry install
```

### Running

`poetry run python -m rag_demo`

