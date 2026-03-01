from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-east-1",
    temperature=0.7,
    max_tokens=1024,
)

agent = Agent(model=model)
print("Using model:", model.config.get("model_id"))
agent("What are the top 3 benefits of serverless architecture? Be concise.")
