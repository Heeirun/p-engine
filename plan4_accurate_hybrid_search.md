# Plan for Improving Hybrid Search Accuracy

This document analyzes why the initial hybrid search returned a semantically similar but contextually incorrect result, and proposes concrete steps to improve its accuracy.

## 1. Analysis of the Inaccuracy

The query "removing access to financials" returned a top result for "granting access to a file." This occurred because a general-purpose sentence-transformer model like `all-MiniLM-L6-v2` prioritizes **topical similarity** over **specific intent**.

-   **High Topical Similarity**: Both the query and the result share the core concepts of "access" and "financials."
-   **Low Intent Differentiation**: The model understands that "removing" and "granting" are both actions related to "access," but it doesn't weigh their opposing nature heavily enough without more explicit context. It correctly identified the "what" (access to financials) but missed the crucial "how" (the direction of the action).

To fix this, we need to provide the model with a clearer, more explicit signal that emphasizes the importance of the action itself.

## 2. Proposed Solutions to Improve Accuracy

Here are three strategies, from most practical to most advanced, to make the hybrid search more accurate.

### Strategy 1: (Recommended) Data-Centric Improvement: Create a Dedicated Embedding Field

The most effective and practical approach is to change the text we are embedding. Instead of just using the `summary` and `description`, we will create a new, dedicated text field specifically for the embedding. This field will be structured to give the action word more prominence.

**Current text for embedding (implicit):**
`A user granted access to a file. User Alice granted read access to the file 'financials_q3.docx' to user Bob.`

**Proposed new text for embedding:**
We will combine the `action` field with the `description` to create a more precise input for the model.

`Action: file.grant_access. Details: User Alice granted read access to the file 'financials_q3.docx' to user Bob.`

This structure explicitly tells the model that the `file.grant_access` action is the most important part of the text, making it much easier to distinguish from `file.revoke_access`.

#### Implementation Steps:

1.  **Update the Seeding Script (`seed.sh`):** Modify the `jq` command in `seed.sh` to create this new combined field in the `bulk_data.json` file.
2.  **Update the Elasticsearch Mapping:** Add a new field, e.g., `embedding_text`, to the index mapping.
3.  **Update the Hybrid Search Query:** Change the `knn` part of the query to use the embedding generated from this new field.

### Strategy 2: Model-Centric Improvement: Fine-Tuning the Embedding Model

For the highest possible accuracy, we can fine-tune the sentence-transformer model on our own audit log data. This teaches the model the specific nuances of our domain, including which actions are opposites.

This involves creating a training dataset of queries and relevant/irrelevant documents. For example:

-   **Query**: "who took away file permissions?"
-   **Positive (Relevant) Example**: "Action: file.revoke_access. Details: User Alice revoked access..."
-   **Negative (Irrelevant) Example**: "Action: file.grant_access. Details: User Alice granted access..."

This is a powerful but more complex solution that requires creating a labeled dataset and a model training pipeline.

### Strategy 3: Query-Time Improvement: Adjusting RRF Tuning

Reciprocal Rank Fusion (RRF) combines the keyword and semantic search scores. We can tune its parameters to change the balance between them. If we find that user queries often contain very specific keywords (like "revoke" or "grant"), we could give more weight to the keyword search results.

This is a tuning step that is best performed after implementing Strategy 1, as improving the data quality will have the most significant impact.

## 3. Recommended Next Steps

1.  **Implement Strategy 1**: Modify the data ingestion process to create the new `embedding_text` field. This is the "low-hanging fruit" and is likely to provide a significant accuracy boost with moderate effort.
2.  **Evaluate**: Re-run the search queries to measure the improvement.
3.  **Consider Strategy 2/3**: If further accuracy is needed, consider the more advanced options of fine-tuning the model or adjusting the RRF query parameters.
