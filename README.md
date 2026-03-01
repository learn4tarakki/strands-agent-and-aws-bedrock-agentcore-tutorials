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

## Deploying to AWS AgentCore

`main.py` is the AgentCore entrypoint that wraps the expense tracker agent.

### Additional Prerequisites

- Docker not required (CodeBuild handles container builds in the cloud)
- IAM permissions for CodeBuild to push to ECR (see Troubleshooting below)

### Install AgentCore packages

```bash
uv add bedrock-agentcore bedrock-agentcore-starter-toolkit
```

### Configure

```bash
uv run agentcore configure --name expense_tracker_agent --entrypoint main.py
```

> Use underscores in the agent name — dashes are not allowed.

The CLI will interactively ask the following:

| Prompt | Recommended choice |
|---|---|
| **Dependency file** | Press Enter to use auto-detected `pyproject.toml` |
| **Deployment type** | `1` Direct Code Deploy (no Docker) or `2` Container |
| **Execution role** | Press Enter to auto-create |
| **ECR Repository URI** | Press Enter to auto-create, or paste an existing ECR URI |
| **Authorization** | Press Enter to use default IAM authorization |
| **Request header allowlist** | Press Enter to skip (default) |
| **Memory setup** | Press Enter to create new short-term memory |
| **Long-term memory** | `no` unless you need cross-session memory (adds ~2 min processing) |

### Test locally before deploying

```bash
uv run agentcore deploy --local
```

Then invoke locally:

```bash
uv run agentcore invoke '{"prompt": "Add ₹500 on groceries, ₹150 on coffee at Starbucks, ₹800 on AWS bill, ₹300 on Ola to airport, ₹4500 on flight ticket. Show spending summary and largest expense."}'
```

### Deploy to cloud

```bash
uv run agentcore deploy
```

This builds an ARM64 container via AWS CodeBuild, pushes it to ECR, and provisions an AgentCore Runtime endpoint — no local Docker required.

### Invoke the deployed agent

```bash
uv run agentcore invoke '{"prompt": "Add ₹500 on groceries, ₹150 on coffee at Starbucks, ₹800 on AWS bill, ₹300 on Ola to airport, ₹4500 on flight ticket. Show spending summary and largest expense."}'
```

---

## Troubleshooting

**AWS credentials error** — Run `aws configure` or set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` as environment variables.

**Model access denied** — Enable the model in AWS Bedrock console → Model access.

**`ANTHROPIC_API_KEY` not found** — Make sure `.env` exists in the project root with your key (file 03 only).

**AgentCore ECR push denied** — The CodeBuild role needs ECR push permissions. Add an inline policy to the role `AmazonBedrockAgentCoreSDKCodeBuild-us-east-1-*`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage"
      ],
      "Resource": "arn:aws:ecr:<region>:<account-id>:repository/<your-repo>"
    }
  ]
}
```

## Resources

- [Strands Bedrock model source](https://github.com/strands-agents/sdk-python/blob/main/src/strands/models/bedrock.py) — code to find the default model in Strands Agent
- [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview) — choosing Anthropic models