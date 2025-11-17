# Plan for Hybrid Search on Audit Logs in Elasticsearch

This document outlines a high-level plan for implementing hybrid search on audit logs using Elasticsearch, based on the provided `@audit_log_model.txt`.

## 1. Audit Log Model

The following model, based on `@audit_log_model.txt`, will be used for an audit log entry:

-   `id`: Unique identifier for the log entry (UUID).
-   `action`: The action performed (e.g., `user.login`, `document.create`).
-   `description`: A detailed, human-readable description of the event, with identifiers resolved to names (e.g., "User Alice" instead of "user-a").
-   `ip_address`: IP address of the requestor.
-   `occured_at`: ISO 8601 timestamp of when the event occurred.
-   `summary`: A concise, generic summary of the event, without any specific identifiers (e.g., "A user uploaded a file.").
-   `target_entities`: An array of objects representing the resources affected by the action.
    -   `id`: Unique identifier of the entity.
    -   `type`: The type of the entity (e.g., `user`, `document`).
-   `created_at`: ISO 8601 timestamp of when the log entry was created.
-   `actor_id`: The identifier of the user or service that performed the action.
-   `organization_id`: The identifier of the organization the actor belongs to.

## 2. Elasticsearch Index Mapping

An Elasticsearch index named `audit_logs` will be created with a mapping designed for hybrid search.

### Key Mapping Features:

-   **Text Fields**: `description` and `summary` will be mapped as `text` for optimal full-text search.
-   **Keyword Fields**: `id`, `action`, `actor_id`, and `organization_id` will be `keyword` fields for exact matching, filtering, and aggregations.
-   **Specialized Fields**: `ip_address` will be mapped as `ip`, and `occured_at` and `created_at` will be `date` fields.
-   **Nested Objects**: `target_entities` will be mapped as a `nested` field to allow for precise querying on individual entities within the array.
-   **Vector Field**: A single `dense_vector` field named `embedding_vector` will store the semantic embedding. This embedding will be generated from a combination of the `summary` and `description` fields to provide a rich vector for semantic search.

### Example Mapping:

```json
{
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "action": { "type": "keyword" },
      "description": { "type": "text" },
      "ip_address": { "type": "ip" },
      "occured_at": { "type": "date" },
      "summary": { "type": "text" },
      "target_entities": {
        "type": "nested",
        "properties": {
          "id": { "type": "keyword" },
          "type": { "type": "keyword" }
        }
      },
      "created_at": { "type": "date" },
      "actor_id": { "type": "keyword" },
      "organization_id": { "type": "keyword" },
      "embedding_vector": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  }
}
```

## 3. Data Ingestion and Enrichment

A data pipeline will be established to process and index audit logs.

### Pipeline Steps:

1.  **Collect**: Gather audit logs from various services.
2.  **Enrich**: For each log entry, create a combined text field from the `summary` and `description`. Generate a vector embedding from this combined text using a sentence-transformer model (e.g., `all-MiniLM-L6-v2`).
3.  **Index**: Ingest the log entry, including the new `embedding_vector`, into the `audit_logs` index in Elasticsearch.

## 4. Hybrid Search Strategy

The search functionality will combine traditional keyword search with semantic vector search.

### Query Approach:

-   A user's natural language query (e.g., "user tried to access a restricted file") will be used for both parts of the search.
-   **Keyword Search**: The query string will be used in a `multi_match` query against the `summary` and `description` fields.
-   **Semantic Search**: The query string will be converted into a vector embedding, which will then be used in a `knn` (k-Nearest Neighbor) search on the `embedding_vector` field.
-   **Result Combination**: The results from both queries will be combined using Reciprocal Rank Fusion (RRF) to produce a single, relevance-ranked list.

### Example Hybrid Query:

```json
{
  "query": {
    "multi_match": {
      "query": "user tried to access a restricted file",
      "fields": ["summary", "description"]
    }
  },
  "knn": {
    "field": "embedding_vector",
    "query_vector": [ ... ], 
    "k": 10,
    "num_candidates": 100
  },
  "rank": {
    "rrf": {}
  }
}
```

This updated plan provides a comprehensive overview tailored to your specific audit log model.
