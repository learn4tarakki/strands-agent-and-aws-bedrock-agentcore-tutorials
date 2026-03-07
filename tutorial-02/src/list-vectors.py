import boto3

# Configuration
S3_VECTOR_BUCKET_NAME = "tutorial-02-expenses-vector-store"
VECTOR_INDEX_NAME = "expenses-index"
AWS_REGION = "us-east-1"


def main():
    s3vectors_client = boto3.client("s3vectors", region_name=AWS_REGION)

    response = s3vectors_client.list_vectors(
        vectorBucketName=S3_VECTOR_BUCKET_NAME,
        indexName=VECTOR_INDEX_NAME,
        returnMetadata=True,
        returnData=True,
    )

    vectors = response.get("vectors", [])
    print(f"Total vectors in index: {len(vectors)}\n")

    for v in vectors:
        metadata = v.get("metadata", {})
        values = v.get("data", {}).get("float32", [])
        preview = [round(x, 6) for x in values[:3]]
        print(f"Key    : {v['key']}")
        print(f"Month  : {metadata.get('month')}")
        print(f"Year   : {metadata.get('year')}")
        print(f"Vector : {preview} ... (first 3 of {len(values)} dimensions)")
        print(f"Text   : {metadata.get('text')}")
        print()


if __name__ == "__main__":
    main()
