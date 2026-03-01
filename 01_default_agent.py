from strands import Agent

# Default: AWS Bedrock, us.anthropic.claude-sonnet-4-20250514-v1:0
agent = Agent()

print("Model config:", agent.model.config)
agent("Explain what agentic AI is in 2-3 sentences.")
