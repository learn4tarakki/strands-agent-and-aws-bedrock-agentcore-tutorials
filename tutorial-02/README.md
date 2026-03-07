# Tutorial 02 — RAG with AWS Strands Agents and S3 Vector Store

Five monthly expense journal entries (Jan–May 2024) are embedded with **Amazon Bedrock Titan Embeddings V2** and stored as vectors in an **Amazon S3 Vector Store**. A **Strands Agent** receives a user-selected query, retrieves the most relevant entries via a custom `search_journal` tool, and passes them as context to Claude for a grounded answer.

## Prerequisites

- AWS credentials configured (`aws configure` or environment variables)
- Bedrock model access enabled in `us-east-1`:
  - `amazon.titan-embed-text-v2:0` (embeddings)
  - A working Claude inference profile (see troubleshooting below)
- IAM permissions for `bedrock:InvokeModel` and `s3vectors:*`

## Run

```bash
# Step 1 — embed journal entries and store vectors (run once)
uv run src/01-store-vectors.py

# Step 2 — launch the Strands RAG agent and pick a query
uv run src/02-strands-rag-agent.py

# Optional — list all vectors stored in the index
uv run src/list-vectors.py
```

Script 1 creates the S3 vector bucket and index if needed, then stores 5 vectors (one per month). Re-running skips entries that already exist.

Script 2 presents 2 example queries. Enter 1 or 2 to select — the agent retrieves the most relevant monthly entries before generating an answer.

## Troubleshooting — model not working?

AWS marks older Claude models as Legacy if you haven't used them recently, causing `ResourceNotFoundException`. Run this script to find which models are active in your account:

```bash
uv run src/find-working-model.py
```

Then update the `model=` value in `02-strands-rag-agent.py` to any model that prints `OK`.
