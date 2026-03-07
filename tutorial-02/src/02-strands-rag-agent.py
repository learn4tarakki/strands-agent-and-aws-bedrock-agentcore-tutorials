import boto3
import json

from strands import Agent, tool

S3_VECTOR_BUCKET_NAME = "tutorial-02-expenses-vector-store"
VECTOR_INDEX_NAME = "expenses-index"
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
AWS_REGION = "us-east-1"

# To swap to Amazon reranker: "arn:aws:bedrock:us-east-1::foundation-model/amazon.rerank-v1"
RERANKER_MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/cohere.rerank-v3-5:0"

# Entries scoring below this after reranking are dropped before sending to the LLM
RELEVANCE_THRESHOLD = 0.10

QUERIES = [
    "Which month did I spend the most money overall?",
    "When did I spend money on fitness or physical health?",
]


def rerank(query: str, results: list) -> list:
    """Rerank retrieved results using Bedrock reranker.

    To swap to Cohere reranker hosted on Bedrock, change RERANKER_MODEL_ARN above.
    To swap to Cohere's direct API, replace this function body with the Cohere SDK call
    keeping the same signature: rerank(query, results) -> list.
    """
    bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

    texts = [r.get("metadata", {}).get("text", "") for r in results]

    response = bedrock_agent_runtime.rerank(
        queries=[{"type": "TEXT", "textQuery": {"text": query}}],
        sources=[
            {
                "type": "INLINE",
                "inlineDocumentSource": {"type": "TEXT", "textDocument": {"text": text}},
            }
            for text in texts
        ],
        rerankingConfiguration={
            "type": "BEDROCK_RERANKING_MODEL",
            "bedrockRerankingConfiguration": {
                "modelConfiguration": {"modelArn": RERANKER_MODEL_ARN},
                "numberOfResults": len(results),
            },
        },
    )

    reranked = sorted(response["results"], key=lambda x: x["relevanceScore"], reverse=True)
    return [(results[r["index"]], r["relevanceScore"]) for r in reranked]


@tool
def search_journal(query: str) -> str:
    """Search the S3 vector store for expense journal entries relevant to the query.

    Args:
        query: The question or search string to look up.

    Returns:
        Formatted string containing journal passages reranked by relevance.
    """
    bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    s3vectors_client = boto3.client("s3vectors", region_name=AWS_REGION)

    body = json.dumps({"inputText": query, "dimensions": 1024, "normalize": True})
    response = bedrock_client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    embedding = json.loads(response["body"].read())["embedding"]

    response = s3vectors_client.query_vectors(
        vectorBucketName=S3_VECTOR_BUCKET_NAME,
        indexName=VECTOR_INDEX_NAME,
        queryVector={"float32": embedding},
        topK=5,
        returnMetadata=True,
    )

    results = response.get("vectors", [])
    if not results:
        return "No matching journal entries found."

    print(f"  Vector search returned {len(results)} entries, reranking...")
    reranked = rerank(query, results)

    parts = []
    for rank, (r, score) in enumerate(reranked, start=1):
        metadata = r.get("metadata", {})
        text = metadata.get("text", "[text not found]")
        if score >= RELEVANCE_THRESHOLD:
            print(f"  Reranked #{rank}: {r['key']} (relevance={score:.4f})")
            parts.append(f"[rank={rank} | relevance={score:.4f} | month={metadata.get('month')} | year={metadata.get('year')}]\n{text}")
        else:
            print(f"  Reranked #{rank}: {r['key']} (relevance={score:.4f}) — dropped (below threshold)")

    if not parts:
        return "No sufficiently relevant journal entries found."

    return "\n\n---\n\n".join(parts)


def main():
    print("=== S3 Vector Store RAG — Strands Agent ===\n")
    print("Select a query (enter 1 or 2):\n")
    for i, q in enumerate(QUERIES, start=1):
        print(f"  {i}. {q}")

    print()
    choice = input("Your choice: ").strip()
    if choice not in {"1", "2"}:
        print("Invalid choice. Please enter 1 or 2.")
        return

    query = QUERIES[int(choice) - 1]

    agent = Agent(
        model="us.anthropic.claude-sonnet-4-6",
        tools=[search_journal],
        system_prompt=(
            "You are a helpful personal finance assistant. The user is asking about their own "
            "expense journal. Call the search_journal tool exactly once, then answer based strictly "
            "on what it returns. Refer to the user as 'you'."
        ),
    )

    print(f"\nQuery: {query}\n")
    print("--- Agent response ---\n")
    response = agent(query)
    print(response)


if __name__ == "__main__":
    main()
