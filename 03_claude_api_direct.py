import os
from dotenv import load_dotenv
from strands import Agent
from strands.models import AnthropicModel

load_dotenv()

model = AnthropicModel(
    model_id="claude-opus-4-20250514",
    max_tokens=2048,
    params={"temperature": 0.5},
    client_args={"api_key": os.environ["ANTHROPIC_API_KEY"]},
)

agent = Agent(model=model)
print("Using Anthropic API directly (not Bedrock)")
agent("Describe the difference between RAG and fine-tuning for LLMs.")
