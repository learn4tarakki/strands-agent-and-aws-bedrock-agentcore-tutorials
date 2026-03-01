# Strands Agent + AWS Bedrock — Tutorial Series

Code for the YouTube tutorial series on building AI agents with [Strands Agents](https://github.com/strands-agents/sdk-python) and AWS Bedrock.

---

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- AWS account with Bedrock access (us-east-1 recommended)
- AWS credentials configured (`aws configure` or environment variables)

---

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd strands-agent-and-aws-bedrock-agentcore-tutorials

# Install dependencies
uv sync
```

For **file 03** only, you also need an Anthropic API key:

```bash
# Create a .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

---

## Files — Run in Order

### 01 — Default Agent
```bash
uv run 01_default_agent.py
```
Creates the simplest possible agent. Uses AWS Bedrock with Claude Sonnet 4 by default — no configuration needed.

---

### 02 — Explicit Bedrock Model
```bash
uv run 02_bedrock_explicit_model.py
```
Shows how to choose a specific model (Claude Haiku) and set parameters like `temperature` and `max_tokens`.

---

### 03 — Claude API Direct (no Bedrock)
```bash
uv run 03_claude_api_direct.py
```
Uses the Anthropic API directly instead of Bedrock. Requires `ANTHROPIC_API_KEY` in your `.env` file.

---

### 04 — Expense Tracker Agent (Custom Tools)
```bash
uv run 04_expense_tracker_agent.py
```
Builds a real agent with custom tools using the `@tool` decorator. The agent can add expenses, summarize spending, and find the largest expense — all through natural language.

---

## Troubleshooting

**AWS credentials error** — Run `aws configure` or set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` as environment variables.

**Model access denied** — Enable the model in AWS Bedrock console → Model access.

**`ANTHROPIC_API_KEY` not found** — Make sure `.env` exists in the project root with your key (file 03 only).
