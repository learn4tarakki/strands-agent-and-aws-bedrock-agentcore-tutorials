import boto3
import json

from strands import Agent, tool

# Configuration
S3_VECTOR_BUCKET_NAME = "tutorial-02-expenses-vector-store"
VECTOR_INDEX_NAME = "expenses-index"
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
AWS_REGION = "us-east-1"

QUERIES = [
    "Which month did I spend the most money overall?",
    "How much did I spend on electricity across all months?",
]


@tool
def search_journal(query: str) -> str:
    """Search the S3 vector store for expense journal entries relevant to the query.

    Args:
        query: The question or search string to look up.

    Returns:
        Formatted string containing the top matching journal passages.
    """
    bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    s3vectors_client = boto3.client("s3vectors", region_name=AWS_REGION)

    # Embed the query
    body = json.dumps({"inputText": query, "dimensions": 1024, "normalize": True})
    response = bedrock_client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    embedding = json.loads(response["body"].read())["embedding"]

    # Query the vector store — text is stored in metadata so it comes back in results
    response = s3vectors_client.query_vectors(
        vectorBucketName=S3_VECTOR_BUCKET_NAME,
        indexName=VECTOR_INDEX_NAME,
        queryVector={"float32": embedding},
        topK=3,
        returnMetadata=True,
    )

    results = response.get("vectors", [])
    if not results:
        return "No matching journal entries found."

    parts = []
    for r in results:
        score = r.get("score", 0)
        metadata = r.get("metadata", {})
        text = metadata.get("text", "[text not found]")
        parts.append(f"[score={score:.4f} | month={metadata.get('month')} | year={metadata.get('year')}]\n{text}")

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
        model="us.anthropic.claude-sonnet-4-6-20251001-v2:0",
        tools=[search_journal],
        system_prompt=(
            "You are a helpful personal finance assistant. The user is asking about their own "
            "expense journal. Always use the search_journal tool to find relevant journal entries "
            "before answering. Refer to the user as 'you' and base your answer strictly on what "
            "the tool returns."
        ),
    )

    print(f"\nQuery: {query}\n")
    print("--- Agent response ---\n")
    response = agent(query)
    print(response)


if __name__ == "__main__":
    main()
