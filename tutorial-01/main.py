import importlib

from bedrock_agentcore import BedrockAgentCoreApp

expense_module = importlib.import_module("04_expense_tracker_agent")
agent = expense_module.agent

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: dict):
    response = agent(payload.get("prompt", ""))
    return {"response": str(response)}


if __name__ == "__main__":
    app.run()
