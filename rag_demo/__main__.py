### Utility libraries
import os
import time

### PostgreSQL adapter for Python
import psycopg

### PyPDF for text extraction
from PyPDF2 import PdfReader

### Embeddings model
import torch
import torch.nn.functional as F
from transformers import AutoModel

### Text generation model
from transformers import pipeline

### Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CHUNK_SIZE = 512
MODEL_ID = "meta-llama/Llama-3.2-3B"

### PostgreSQL database url and connection
database_url = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:6432/rag_demo"
)
db = psycopg.Connection.connect(database_url)


# This is very naive chunking, just to show the concept. LangChain/LlamaIndex have excellent chunking libraries.  Do not use
# this technique in production as it will yield very bad results.
def split_string_by_length(input_string, length):
    return [input_string[i : i + length] for i in range(0, len(input_string), length)]


# Loop through chunks from the pdf and create embeddings in the database

print("Cleaning database...")
db.execute("TRUNCATE TABLE chunks")

# load model with tokenizer
model = AutoModel.from_pretrained('nvidia/NV-Embed-v2', trust_remote_code=True)

tic = time.perf_counter()
for filename in os.listdir(DATA_DIR):
    file_path = os.path.join(DATA_DIR, filename)

    reader = PdfReader(file_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text()

    for chunk in split_string_by_length(content, CHUNK_SIZE):
        print(f"Creating embedding for chunk: {chunk[20]}...")
        
        db.execute(
            f"INSERT INTO items (embedding, chunk) VALUES ({model.encode(chunk)}, {chunk})",
        )

    print(f"\nTotal index time: {time.perf_counter() - tic}ms")
    db.commit()

question = input("\nEnter question: ")

# Create embedding from question.  Many RAG applications use a query rewriter before querying
# the vector database.  For more information on query rewriting, see this whitepaper:
#    https://arxiv.org/abs/2305.14283
question_embedding = model.encode(question)

result = db.execute(
    f"""SELECT (embedding <=> {question_embedding})*100 as score, chunk 
    FROM items 
    ORDER BY score DESC
    LIMIT 5"""
)
rows = list(result)

print("scores: ", [row[0] for row in rows])
context = "\n\n".join([row[1] for row in rows])

prompt = f"""
Answer the question using only the following context:

{context}

Question: {question}
"""

pipe = pipeline(
    "text-generation", 
    model=MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

answer = pipe(prompt)

print(f"\nUsing {len(rows)} chunks in answer. Answer:\n")
print(answer[0]['generated_text'])

view_prompt = input("\nWould you like to see the raw prompt? [Y/N] ")
if view_prompt == "Y":
    print("\n" + prompt)
