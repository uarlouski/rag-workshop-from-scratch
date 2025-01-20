# rag-demo

A bare bones RAG application for educational purposes.

DISCLAIMER: There are several concepts in this repository that can be implemented in much better ways.  The point of this repository is to remove unfamiliar terms and abstractions as much as possible to demonstrate the essential concepts of a RAG application.

You should get acquainted first with RAG and [when to use it and when not to.](https://www.anthropic.com/news/contextual-retrieval)
Also, feel free to check out the [BGE family of models](https://huggingface.co/BAAI/bge-small-en-v1.5) a series of API accessible models for many RAG pieces such as embeddings, retrieval, reranking, etc. 

## Sample output
```
Cleaning database...
Creating embedding for chunk: ize
human priors to ...
Creating embedding for chunk: odifications, ensuri...
Creating embedding for chunk: u et al., 2023; Qian...
Creating embedding for chunk: ned agents and meta-...
Creating embedding for chunk: n Hendrycks, Collin ...

Total index time: 11.419859999790788ms

Enter question: what are the main contributions from the godel agents paper?
scores:  [46.2205144035501, 45.83206449938195, 44.91440161297333, 44.8048227792767, 44.57226661278396]

Using 5 chunks in answer. Answer:

Compiling declarative language model calls into self-improving pipelines
```

## Setup:

This setup works for my WSL installation of Ubuntu with root access.

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
*Troubleshoot*: 
```
sudo apt update
sudo apt install postgresql-client-common
sudo apt install postgresql-client
```


Export your Hugging Face API Key environment variable:
```
source .env
```

Poetry install:
```
poetry install
```
*Troubleshoot*: 
```
sudo apt update
curl -fsSL https://pyenv.run | bash
pyenv install 3.12.0
pyenv local 3.12.0
```

### Running

`poetry run python -m rag_demo`

You can skip the embedding step if you already have a database and want to experiment with different models. 
`poetry run python -m rag_demo --skip-embedding-step`

### Check chunks table first 5 rows
```
psql -h localhost -p 6432 -U postgres rag_demo -c "SELECT * FROM chunks LIMIT 5;"
```