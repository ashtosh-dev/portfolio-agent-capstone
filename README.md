# Portfolio Agent Capstone

This repository contains a professional multi-agent portfolio strategist system built using the **Google Agent Development Kit (ADK) 2.0**.

The system utilizes three specialized agents to fetch live ETF data, perform quantitative mathematical analyses, and synthesize client-ready portfolio reports.

## System Architecture

The workflow is modeled as a directed graph:
```
[START] ──> [Context Agent] ──> [Quant Agent] ──> [Strategist Agent] ──> [END]
                (Research)        (Calculations)       (Orchestrator)
```

- **Context Agent (Researcher):** Uses the MCP Client tool to fetch live/simulated ETF profiles, holdings, and performance statistics.
- **Quant Agent (Number Cruncher):** Uses the Python Executor tool to write and execute scripts calculating portfolio-level metrics (weighted returns, expense ratios, asset splits).
- **Strategist Agent (Orchestrator):** Gathers information from both upstream agents to compile a final investment recommendation report.

---

## Folder Structure

```
portfolio-agent-capstone/
├── agents/
│   ├── strategist_agent.py    # The Orchestrator: Synthesizes data into the final report
│   ├── context_agent.py       # The Researcher: Uses MCP to pull live financial data
│   └── quant_agent.py         # The Number Cruncher: The system prompt we just drafted
├── tools/
│   ├── python_executor.py     # Sandbox code execution tool for the Quant Agent
│   └── mcp_client.py          # Connects to external APIs to fetch ETF/Market data
├── data/                      # Local storage for mutual fund prospectuses or CSVs
├── requirements.txt           # google-adk[extensions], pandas, numpy, etc.
├── README.md                  # Kaggle setup instructions and writeup
└── main_workflow.py           # The ADK graph definition that links the agents together
```

---

## Setup & Installation

### 1. Conda Environment
Activate the environment dedicated for this project:
```bash
conda activate agent-dev
```

### 2. Install Dependencies
Install all required libraries from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. API Credentials
Export your Gemini API Key before running the workflow:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### 4. Environment Variables (Alternative to Export)
For local development, you can create a `.env` file in the root directory. Copy the provided `.env.example` file, rename it to `.env`, and insert your API keys. (Ensure `.env` is added to your `.gitignore`).

---

## Running the Workflow

### Running Programmatically
To run the default workflow with sample inputs:
```bash
python main_workflow.py
```

To run with custom target allocations:
```bash
python main_workflow.py "Create a portfolio with 50% QQQ, 30% VOO, and 20% BND. Compute weighted returns and cost."
```

### Running with ADK CLI / Web UI
You can run agents individually using the ADK CLI:
```bash
adk run agents/context_agent.py
```

Or view and debug the execution graph visually:
```bash
adk web .
```

---

## Kaggle Integration Setup

If running this system in a Kaggle notebook or environment:
1. **Secrets Configuration:**
   Add your API Key as a Kaggle Secret with the label `GEMINI_API_KEY`.
2. **Retrieve Secret in Notebook:**
   ```python
   from kaggle_secrets import UserSecretsClient
   import os
   user_secrets = UserSecretsClient()
   os.environ["GEMINI_API_KEY"] = user_secrets.get_secret("GEMINI_API_KEY")
   ```
3. **Data Mounting:**
   Place any local mutual fund prospectuses or CSVs in the `data/` directory or upload them as a Kaggle Dataset, then access them via `/kaggle/input/...` or copy them to the local workspace.
