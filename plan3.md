# Plan for Implementing a Vector Generation Endpoint

This document outlines the plan to add a new API endpoint to the FastAPI application for generating sentence embeddings, which are required for the hybrid search functionality.

## 1. Add New Dependency

To generate vector embeddings, the `sentence-transformers` library is required. This dependency will be added to the `pyproject.toml` file.

**File: `pyproject.toml`** (Addition)
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.29.0"}
pydantic = "^2.7.1"
sentence-transformers = "^2.2.2"
```

## 2. Create Vector Generation Endpoint

A new endpoint, `/get_vector/`, will be added to `p-engine/main.py`. This endpoint will be responsible for creating a vector from a given text query.

### Endpoint Details:

-   **Path**: `/get_vector/`
-   **Method**: `GET`
-   **Query Parameter**: `text` (string)
-   **Functionality**:
    1.  Load the `all-MiniLM-L6-v2` sentence-transformer model.
    2.  Take the input `text` and encode it into a 384-dimension vector.
    3.  Return the vector as a JSON array of floating-point numbers.

### Implementation in `p-engine/main.py`:

```python
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

```

## 3. How to Use the Endpoint

Once implemented, you can get a query vector by making a `curl` request to the new endpoint.

### Example `curl` Command:

```bash
curl -X GET "http://localhost:8000/get_vector/?text=removing%20access%20to%20financials"
```

This will return a JSON response containing the vector needed for the hybrid search query.

This plan provides a clear path to implementing the missing vector generation functionality.
