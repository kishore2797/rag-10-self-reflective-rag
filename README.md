# RAG Tutorial 10 — Self-Reflective RAG

<p align="center">
  <a href="https://github.com/BellaBe/mastering-rag"><img src="https://img.shields.io/badge/Series-Mastering_RAG-blue?style=for-the-badge" /></a>
  <img src="https://img.shields.io/badge/Part-10_of_16-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Difficulty-Advanced-orange?style=for-the-badge" />
</p>

> **Part of the [Mastering RAG](https://github.com/BellaBe/mastering-rag) tutorial series**  
> Previous: [09 — Re-ranking Pipeline](https://github.com/BellaBe/rag-09-reranking-pipeline) | Next: [11 — Multi-Modal RAG](https://github.com/BellaBe/rag-11-multi-modal-rag)

---

## Real-World Scenario

> A patient asks a healthcare chatbot: "Can I take ibuprofen with my blood pressure medication?" Standard RAG retrieves some vaguely related drug information and generates a confident-sounding (but potentially dangerous) answer. **Self-reflective RAG** evaluates the retrieved chunks and realizes the context doesn't specifically mention the queried drug interaction. Instead of guessing, it says: *"I don't have reliable information about this specific drug interaction. Please consult your pharmacist or doctor."* Self-reflection is the difference between a helpful bot and a liability.

---

## What You'll Build

A RAG system with a built-in **quality gate**: after retrieval, an LLM evaluates whether the chunks are actually relevant. Based on the score, the agent decides to **answer**, **rewrite the query and retry**, or **refuse** gracefully.

```
Query ──→ Retrieve ──→ Evaluate Relevance
                            │
                  ┌─────────┼──────────┐
                  ▼         ▼          ▼
              Relevant   Partial    Irrelevant
                  │         │          │
              Answer    Rewrite &    Refuse
                        Retry        "I don't have enough info"
```

## Key Concepts

- **Relevance evaluation**: LLM scores each retrieved chunk for query relevance
- **Agent decision loop**: answer / re-retrieve / refuse based on evidence quality
- **Query rewriting on failure**: when first retrieval fails, rewrite and try again
- **Graceful refusal**: admitting uncertainty is better than hallucinating

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+ · FastAPI · ChromaDB · OpenAI · Sentence-Transformers |
| Frontend | React 19 · Vite · Tailwind CSS |

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Set OPENAI_API_KEY
uvicorn app.main:app --reload --port 8004
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5178 — ingest docs, query with self-reflection toggle, see agent decisions.

## What You'll Learn

1. Why standard RAG answers even when it shouldn't
2. How to build a relevance evaluation step
3. Agent decision logic: when to answer, retry, or refuse
4. Query rewriting as a retry mechanism
5. How self-reflection dramatically reduces hallucination

## Prerequisites

- Python 3.11+ and Node.js 18+
- Concepts from [Tutorial 05](https://github.com/BellaBe/rag-05-basic-rag-pipeline) (basic RAG pipeline)
- OpenAI API key (for the evaluator LLM)

## Exercises

1. **Hallucination test suite**: Create 10 questions that are definitely NOT answerable from your documents. Does the system correctly refuse every time?
2. **Threshold tuning**: Adjust the relevance score threshold. At what score does the system optimally balance between answering and refusing?
3. **Retry effectiveness**: Track how many queries succeed on the first retrieval vs. after rewrite-and-retry. What percentage of retries actually improve the result?
4. **Evaluator prompt engineering**: Change the evaluation prompt to be stricter or more lenient. How does this affect the answer/refuse ratio?
5. **Multi-hop stress test**: Ask a question that requires information from 2–3 different documents. Does self-reflection handle partial matches well?

## Common Mistakes

| Mistake | Why It Happens | How to Fix |
|---------|---------------|------------|
| System refuses too many valid queries | Relevance threshold is set too high | Lower the threshold; analyze refused queries to find the right balance |
| Retry loop never converges | Rewritten query is no better than the original | Limit retries to 1–2; use a different rewriting strategy for each retry |
| Evaluation LLM is slower than the generation LLM | Both use the same expensive model | Use a faster/cheaper model for evaluation (it's a classification task, not generation) |
| Self-reflection adds 3-5 seconds per query | Extra LLM call for evaluation + possible retry | Evaluate in parallel with generation; only block the response if relevance is below threshold |

## Further Reading

- [Self-RAG: Learning to Retrieve, Generate, and Critique](https://arxiv.org/abs/2310.11511) — The original Self-RAG paper (Asai et al., 2023)
- [Corrective RAG (CRAG)](https://arxiv.org/abs/2401.15884) — A related approach that corrects retrieval before generation
- [LangGraph Self-Reflective RAG](https://blog.langchain.dev/agentic-rag-with-langgraph/) — LangChain's agentic RAG implementation
- [Reducing Hallucination in RAG](https://www.rungalileo.io/blog/mastering-rag-reducing-hallucination) — Practical hallucination mitigation techniques

## Next Steps

Head to **[Tutorial 11 — Multi-Modal RAG](https://github.com/BellaBe/rag-11-multi-modal-rag)** to extend RAG beyond text into images and tables.

---

<p align="center">
  <sub>Part of <a href="https://github.com/BellaBe/mastering-rag">Mastering RAG — From Zero to Production</a></sub>
</p>
