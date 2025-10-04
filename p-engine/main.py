from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from .models import Item

app = FastAPI()

# Load the sentence-transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/get_vector/")
def get_vector(text: str):
    """
    Generates a 384-dimension vector embedding for the given text.
    """
    embedding = model.encode(text)
    return {"text": text, "vector": embedding.tolist()}
