from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-opus-4-6-v1",
    region_name="us-east-1",
    temperature=0.7,
    max_tokens=1024,
)

agent = Agent(model=model)
print("Using model:", model.config.get("model_id"))
agent("What are the top 3 benefits of serverless architecture? Be concise.")
