# Strands Agents + AWS Bedrock AgentCore — Tutorial Series

Code for the YouTube tutorial series on building AI agents with [Strands Agents](https://github.com/strands-agents/sdk-python) and AWS Bedrock.

Each tutorial is self-contained with its own dependencies and setup instructions.

---

## Tutorials

### [Tutorial 01 — Strands Agents + AWS Bedrock AgentCore](./tutorial-01/)
Build AI agents with Strands Agents using AWS Bedrock, then deploy to AWS AgentCore.
- Default agent with Bedrock
- Explicit model selection
- Claude API direct (no Bedrock)
- Expense tracker agent with custom tools
- Deploying to AgentCore via CodeBuild

### [Tutorial 02 — RAG with AWS Strands Agents and S3 Vector Store](./tutorial-02/)
Retrieval Augmented Generation using AWS Strands Agents and Amazon S3 Vector Store.
- Embed monthly expense journal entries with Bedrock Titan Embeddings V2
- Store and retrieve vectors from S3 Vector Store
- Custom Strands tool for semantic search
- Strands Agent answers questions grounded in retrieved journal context
