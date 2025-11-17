# p-engine

A FastAPI-based hybrid search engine for audit logs using Elasticsearch and semantic embeddings. The system combines traditional keyword search with semantic vector search using Reciprocal Rank Fusion (RRF) to provide accurate and relevant results.

## Features

- **Hybrid Search**: Combines keyword and semantic search for better accuracy
- **Semantic Embeddings**: Uses sentence-transformers (`all-MiniLM-L6-v2`) for vector embeddings
- **Elasticsearch Integration**: Leverages Elasticsearch for indexing and search
- **FastAPI Backend**: Production-ready async API with CORS support

## Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose (for Elasticsearch)
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

## Setup

1.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Configure environment variables:**
    ```bash
    cp .env_template .env
    # Edit .env if you need to customize settings
    ```

4.  **Start Elasticsearch cluster:**
    ```bash
    docker-compose up -d
    ```

    Wait for Elasticsearch to be ready (this may take a minute). The cluster will be available at:
    - **URL**: `http://localhost:9200`
    - **Username**: `elastic`
    - **Password**: `b1V4R0Re` (configurable in `.env`)

5.  **Seed test data** (optional, for development):
    ```bash
    chmod +x seed.sh
    ./seed.sh
    ```

    This script will:
    - Create the `audit_logs` index with proper mappings
    - Generate semantic embeddings for test data
    - Ingest sample audit log entries

6.  **Run the application:**
    ```bash
    uv run uvicorn p-engine.main:app --reload
    ```

    The API will be available at `http://localhost:8000`
    - API docs: `http://localhost:8000/docs`
    - Health check: `http://localhost:8000/`

## Development

### Code Quality

We use `ruff` for linting and formatting:

```bash
# Check code
uv run ruff check .

# Format code
uv run ruff format .
```

### Generating Models from JSON Schemas

To regenerate Pydantic models from JSON schemas:

```bash
datamodel-codegen --input p-engine/schemas/item.schema.json --output p-engine/models.py
```

### Monitoring Docker Containers

For monitoring Docker containers (including Elasticsearch):

```bash
# Install ctop (if not already installed)
brew install ctop

# Run ctop to monitor containers
ctop
```

## Project Structure

```
p-engine/
├── p-engine/              # Main application package
│   ├── config/           # Configuration and settings
│   ├── controllers/      # API route handlers
│   ├── models/           # Pydantic models
│   ├── schemas/          # JSON schemas
│   ├── services/         # Business logic (search, embeddings)
│   └── main.py          # FastAPI application entry point
├── plans/                # Project planning documents
├── docker-compose.yml    # Elasticsearch container setup
├── seed.sh              # Database seeding script
├── generate_embeddings.py # Embedding generation utility
└── pyproject.toml       # Project dependencies

```

## API Endpoints

- `GET /` - Health check
- `POST /items` - Create audit log entry
- `GET /items/{item_id}` - Retrieve audit log entry
- `POST /search/keyword` - Keyword search
- `POST /search/semantic` - Semantic vector search
- `POST /search/hybrid` - Hybrid search (keyword + semantic with RRF)

See the interactive API documentation at `http://localhost:8000/docs` for detailed endpoint information and testing.