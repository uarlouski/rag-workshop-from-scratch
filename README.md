# rag-demo

A bare bones RAG application for educational purposes.

DISCLAIMER: There are several concepts in this repository that can be implemented in much better ways.  The point of this repository is to remove unfamiliar terms and abstractions as much as possible to demonstrate the essential concepts of a RAG application.

You should get acquainted first with RAG and [when to use it and when not to.](https://www.anthropic.com/news/contextual-retrieval)
Also, feel free to check out the [BGE family of models](https://huggingface.co/BAAI/bge-small-en-v1.5) a series of API accessible models for many RAG pieces such as embeddings, retrieval, reranking, etc. 

## Sample output
```
Cleaning database...
Creating embedding... 2048
Creating embedding... 2048
Creating embedding... 2048

Total index time: 11.419859999790788ms

Enter question: What are the main contributions from the paper?
scores:  [0.4631096466649033, 0.4358613307724073, 0.4234167246123255, 0.41794766951856144, 0.4139573872089386]

Using 5 chunks in answer. Answer:

Query reranking is considered better than regular semantic search in this context because it involves the adaptation of search queries themselves to bridge the gap between the input text and the needed knowledge. The use of a trainable rewriter, as described, helps in refining the search query to better align it with the context needed by a large language model (LLM) reader. This process results in a higher snippet hit rate and improved retrieval effectiveness compared to standard retrieval methods. The usage of techniques like BM25 for content selection is shown to recall better documents than just relying on snippets. Furthermore, query rewriting significantly enhances the retriever's performance compared to the reader, suggesting that refining the search query can lead to more accurate and relevant retrievals, hence proving more effective than traditional semantic search methods.

Would you like to see the raw prompt? [Y/n]
```

## Setup:

This setup works for my WSL installation of Ubuntu with root access.

Start a pgvector docker container:

```
docker run -p 6432:5432  --name pgvector -e POSTGRES_PASSWORD=postgres -d pgvector/pgvector:pg17
```

Note: The host port for the docker container is 6432 instead of the normal 5432 to avoid port collisions

Optional:


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
`poetry run python -m rag_demo`

### Check chunks table first 5 rows
```
psql -h localhost -p 6432 -U postgres rag_demo -c "SELECT * FROM chunks LIMIT 5;"
```