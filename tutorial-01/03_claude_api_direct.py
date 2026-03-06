import os
from dotenv import load_dotenv
from strands import Agent
from strands.models import AnthropicModel
import anthropic

load_dotenv()

model = AnthropicModel(
    model_id="claude-opus-4-6",
    max_tokens=2048,
    params={"temperature": 0.5},
    client_args={"api_key": os.environ["ANTHROPIC_API_KEY"]},
)

agent = Agent(model=model)
print("Using Anthropic API directly (not Bedrock)")

try:
    agent("Describe the difference between RAG and fine-tuning for LLMs.")
except anthropic.AuthenticationError:
    print("Error: Invalid API key. Check your ANTHROPIC_API_KEY in the .env file.")
except anthropic.BadRequestError as e:
    print(f"Error: Bad request — {e}")
    print("Tip: If your credit balance is too low, add credits at https://console.anthropic.com/settings/billing")
except anthropic.APIConnectionError:
    print("Error: Could not connect to Anthropic API. Check your internet connection.")
except anthropic.APIStatusError as e:
    print(f"Anthropic API error {e.status_code}: {e.message}")