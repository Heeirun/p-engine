# p-engine

A new FastAPI project created with Cookiecutter. We use `uv` for dependency management. For more information, see the [documentation](https://docs.astral.sh/uv/). We use `datamodel-code-generator` to generate Pydantic models from JSON schemas. For more information, see the [documentation](https://koxudaxi.github.io/datamodel-code-generator/).

## Setup

1.  **Install `uv`:** See the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) for details.
    

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -r pyproject.toml -e ".[dev]"
    ```

4.  **Generate models:**
    ```bash
    datamodel-codegen --input schemas/item.schema.json --output app/models.py
    ```

5.  **Run the application:**
    ```bash
    uv run uvicorn p-engine.main:app --reload
    ```

## Linting

To ensure code quality, we use `ruff` as a linter. To run the linter, use the following command:

```bash
uv run ruff check .
uv run ruff format .
```

Installed ctop 
add docs to spinning up elasticsearch cluster
brew install ctop