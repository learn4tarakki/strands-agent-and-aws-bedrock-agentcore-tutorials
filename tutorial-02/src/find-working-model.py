import boto3

CANDIDATES = [
    "us.anthropic.claude-sonnet-4-6",
    "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "us.anthropic.claude-3-5-haiku-20241022-v1:0",
]

client = boto3.client("bedrock-runtime", region_name="us-east-1")

for model_id in CANDIDATES:
    try:
        client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "hi"}]}],
        )
        print(f"OK      {model_id}")
    except Exception as e:
        print(f"FAILED  {model_id} — {e}")
