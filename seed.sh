#!/bin/bash

ES_HOST="http://localhost:9200"
INDEX_NAME="audit_logs"
ES_CREDS="elastic:b1V4R0Re"

# 1. Delete the existing index (optional, for a clean start)
echo "Deleting existing index..."
curl -u $ES_CREDS -X DELETE "${ES_HOST}/${INDEX_NAME}"

# 2. Create the index with the correct mapping
echo "Creating index with mapping..."
curl -u $ES_CREDS -X PUT "${ES_HOST}/${INDEX_NAME}" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "action": { "type": "keyword" },
      "summary": { "type": "text" },
      "description": { "type": "text" },
      "embedding_text": { "type": "text" },
      "ip_address": { "type": "ip" },
      "occured_at": { "type": "date" },
      "created_at": { "type": "date" },
      "actor_id": { "type": "keyword" },
      "organization_id": { "type": "keyword" },
      "target_entities": {
        "type": "nested",
        "properties": {
          "id": { "type": "keyword" },
          "type": { "type": "keyword" }
        }
      },
      "embedding_vector": {
        "type": "dense_vector",
        "dims": 384
      }
    }
  }
}
'

# 3. Ingest the test data using the Bulk API
echo "Creating bulk data file..."
jq -c '.[] | . + {"embedding_text": ("Action: " + .action + ". Details: " + .description)} | del(.embedding_vector)' test_data.json | while read -r line; do
    id=$(echo "$line" | jq -r '.id')
    echo "{\"index\": {\"_index\": \"$INDEX_NAME\", \"_id\": \"$id\"}}"
    echo "$line"
done > bulk_data.json

echo "Generating embeddings for bulk data..."
uv run python generate_embeddings.py

echo "Ingesting data..."
curl -u $ES_CREDS -s -X POST "${ES_HOST}/_bulk" -H "Content-Type: application/x-ndjson" --data-binary "@bulk_data.json"

echo "Seeding complete."
