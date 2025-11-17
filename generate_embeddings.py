#!/usr/bin/env python3

import json
from sentence_transformers import SentenceTransformer

def generate_embeddings():
    # Load the sentence-transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Read the bulk data file
    with open('bulk_data.json', 'r') as f:
        lines = f.readlines()
    
    # Process each document in the bulk file
    updated_lines = []
    for i in range(0, len(lines), 2):
        # Lines come in pairs: index directive and document
        index_line = lines[i]
        doc_line = lines[i + 1]
        
        # Parse the document
        doc = json.loads(doc_line)
        
        # Generate embedding from the embedding_text field
        if 'embedding_text' in doc:
            embedding = model.encode(doc['embedding_text']).tolist()
            doc['embedding_vector'] = embedding
        
        # Add back to lines
        updated_lines.append(index_line)
        updated_lines.append(json.dumps(doc) + '\n')
    
    # Write the updated bulk data back
    with open('bulk_data.json', 'w') as f:
        f.writelines(updated_lines)
    
    print("Embeddings generated and added to bulk_data.json")

if __name__ == "__main__":
    generate_embeddings()