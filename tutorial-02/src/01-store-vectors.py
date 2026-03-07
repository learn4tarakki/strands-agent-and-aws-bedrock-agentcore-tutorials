import boto3
import json

S3_VECTOR_BUCKET_NAME = "tutorial-02-expenses-vector-store"
VECTOR_INDEX_NAME = "expenses-index"
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
AWS_REGION = "us-east-1"

JOURNAL_ENTRIES = [
    {
        "key": "expenses-jan-2024",
        "month": "january",
        "year": "2024",
        "text": "January 2024: My rent was ₹25,000 as usual. Groceries cost me ₹6,200 — I stocked up on dal and rice in bulk. My electricity bill spiked to ₹3,100 because of the heater. I splurged ₹4,500 on a new pair of running shoes. My total spend this month: ₹38,800.",
    },
    {
        "key": "expenses-feb-2024",
        "month": "february",
        "year": "2024",
        "text": "February 2024: Rent ₹25,000. My food spending was lighter this month at ₹5,400 — I ate out only twice. I bought a birthday gift for a friend, ₹2,200. Internet and mobile came to ₹1,800. I renewed my gym membership for ₹3,000. My total spend this month: ₹37,400.",
    },
    {
        "key": "expenses-mar-2024",
        "month": "march",
        "year": "2024",
        "text": "March 2024: Rent ₹25,000. I had a nasty cold — a doctor visit plus medicines set me back ₹3,800. Groceries ₹5,900. I treated myself to a nice dinner out, ₹2,100. My electricity bill was lower at ₹2,200 now that winter is gone. My total spend this month: ₹39,000.",
    },
    {
        "key": "expenses-apr-2024",
        "month": "april",
        "year": "2024",
        "text": "April 2024: Rent ₹25,000. Groceries ₹5,600. I signed up for an online Python course — ₹4,999. My cab rides were heavy this month because of project deadlines, ₹3,200. Electricity ₹2,400. My total spend this month: ₹41,199.",
    },
    {
        "key": "expenses-may-2024",
        "month": "may",
        "year": "2024",
        "text": "May 2024: Rent ₹25,000. Groceries ₹5,800. My AC started running all day — electricity jumped to ₹4,600. I bought new office headphones for ₹6,500. Dining out ₹3,100. I also put ₹10,000 into my SIP this month, felt good about that. My total spend this month: ₹55,000.",
    },
]


def generate_embedding(text: str, bedrock_client) -> list[float]:
    body = json.dumps({"inputText": text, "dimensions": 1024, "normalize": True})
    response = bedrock_client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    return json.loads(response["body"].read())["embedding"]


def create_vector_store_if_not_exists(s3vectors_client, dimension: int):
    try:
        s3vectors_client.create_vector_bucket(vectorBucketName=S3_VECTOR_BUCKET_NAME)
        print(f"Created vector bucket: {S3_VECTOR_BUCKET_NAME}")
    except s3vectors_client.exceptions.ConflictException:
        print(f"Vector bucket already exists: {S3_VECTOR_BUCKET_NAME}")

    try:
        s3vectors_client.create_index(
            vectorBucketName=S3_VECTOR_BUCKET_NAME,
            indexName=VECTOR_INDEX_NAME,
            dataType="float32",
            dimension=dimension,
            distanceMetric="cosine",
        )
        print(f"Created vector index: {VECTOR_INDEX_NAME}")
    except s3vectors_client.exceptions.ConflictException:
        print(f"Vector index already exists: {VECTOR_INDEX_NAME}")


def get_existing_keys(s3vectors_client) -> set:
    try:
        response = s3vectors_client.list_vectors(
            vectorBucketName=S3_VECTOR_BUCKET_NAME,
            indexName=VECTOR_INDEX_NAME,
        )
        keys = {v["key"] for v in response.get("vectors", [])}
        print(f"Found {len(keys)} existing vector(s) in the index.\n")
        return keys
    except Exception:
        return set()


def main():
    bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    s3vectors_client = boto3.client("s3vectors", region_name=AWS_REGION)

    existing_keys = get_existing_keys(s3vectors_client)

    index_created = False
    for entry in JOURNAL_ENTRIES:
        if entry["key"] in existing_keys:
            print(f"Skipping (already exists): {entry['key']}")
            continue

        print(f"Generating embedding for: {entry['key']}")
        embedding = generate_embedding(entry["text"], bedrock_client)

        if not index_created:
            create_vector_store_if_not_exists(s3vectors_client, dimension=len(embedding))
            index_created = True

        metadata = {"month": entry["month"], "year": entry["year"], "text": entry["text"]}
        s3vectors_client.put_vectors(
            vectorBucketName=S3_VECTOR_BUCKET_NAME,
            indexName=VECTOR_INDEX_NAME,
            vectors=[{"key": entry["key"], "data": {"float32": embedding}, "metadata": metadata}],
        )
        print(f"Stored vector: {entry['key']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
