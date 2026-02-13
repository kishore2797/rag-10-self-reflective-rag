#!/usr/bin/env python3
"""
RAG Tutorial 10 — Self-Reflective RAG
Minimal example: retrieve chunks, evaluate relevance (simple heuristic), then answer or refuse.
Run: pip install -r requirements.txt && python example.py
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def is_relevant(query: str, chunk: str, min_overlap: int = 2) -> bool:
    """Simple relevance: query words must appear in chunk (proxy for LLM-as-judge)."""
    q_words = set(w.lower() for w in query.split() if len(w) > 2)
    c_lower = chunk.lower()
    return sum(1 for w in q_words if w in c_lower) >= min_overlap


def main():
    docs = [
        "RAG combines retrieval with LLM generation.",
        "Chunking splits documents for embedding.",
        "The capital of France is Paris.",
    ]
    client = chromadb.Client(Settings(anonymized_telemetry=False))
    coll = client.get_or_create_collection("self_reflective_example")
    coll.add(
        ids=[f"d_{i}" for i in range(len(docs))],
        embeddings=model.encode(docs).tolist(),
        documents=docs,
    )
    query = "What is the capital of France?"
    results = coll.query(
        query_embeddings=model.encode([query]).tolist(),
        n_results=3,
        include=["documents"],
    )
    chunks = results["documents"][0]
    relevant = [c for c in chunks if is_relevant(query, c)]
    if not relevant:
        print("Query:", query)
        print("Decision: REFUSE — No relevant context found.")
        print("→ In production, you might rewrite the query and retry.")
        return
    context = " ".join(relevant)
    print("Query:", query)
    print("Relevant chunks:", relevant)
    print("Answer (mock): Based on context:", context[:80] + "...")
    print("→ Self-reflective RAG refuses or retries when context is irrelevant.")


if __name__ == "__main__":
    main()
