# Raft AI Engineer Coding Challenge

A terminal-based AI agent that takes natural language queries about orders, hits a local REST API, parses the raw unstructured response using an LLM, and returns clean structured JSON. Built with LangGraph, LangChain, and a Textual TUI.

---

## What it does

You type something like:

```
Show me all orders from Ohio where the total was over $500
```

The agent calls the local order API, feeds the messy text response to the LLM, filters it based on your query, and returns:

```json
{
  "orders": [
    { "orderId": "1005", "buyer": "Chris Myers", "state": "OH", "total": 512.0 },
    { "orderId": "1009", "buyer": "David Okafor", "state": "OH", "total": 649.0 }
  ]
}
```

It also shows a live stats panel with a linear regression prediction of the next order value, trend direction, and average order total.

---

## Architecture

```
User Query (Terminal UI)
        │
        ▼
  [ main.py — Textual TUI ]
        │
        ▼
  [ LangGraph ReAct Agent ]
        │
        ├──► Tool: fetch_all_orders  ──► GET /api/orders
        ├──► Tool: fetch_order_by_id ──► GET /api/order/<id>
        │
        ▼
  LLM parses + filters raw text
  (openai/gpt-oss-120b:exacto via OpenRouter)
        │
        ▼
  Clean JSON Output
  { "orders": [ { "orderId", "buyer", "state", "total" } ] }
```

---

## Requirements

- Python 3.10 or higher
- An OpenRouter API key (free at [openrouter.ai](https://openrouter.ai))

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/SaathvikR/raft-tech-challenge.git
cd raft-tech-challenge
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> On Windows use: `.venv\Scripts\activate`

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

This installs everything needed — Flask, LangGraph, LangChain, Textual, scikit-learn, and all supporting packages.

### 4. Add your API key

Create a `.env` file in the project root:

```bash
touch .env
```

Add your OpenRouter key to it:

```
OPENAI_API_KEY=your_openrouter_key_here
```

To get a key:
- Go to [https://openrouter.ai](https://openrouter.ai)
- Sign up and go to **Keys**
- Create a new key and paste it above

> ⚠️ The `.env` file is in `.gitignore` and will never be committed. Don't share your key.

---

## Running the app

You need two terminals open at the same time.

**Terminal 1 — start the order API:**

```bash
source .venv/bin/activate
python3 dummy_customer_api.py
```

**Terminal 2 — start the agent UI:**

```bash
source .venv/bin/activate
python3 main.py
```

---

## Example queries to try

```
Show me all orders from Ohio over $500
Show all orders from Texas
Which orders have a total over $1000?
Find orders for Rachel Kim
Show me all orders under $200
Show orders from the West Coast
```

---

## Project structure

```
raft-tech-challenge/
├── agent/
│   ├── __init__.py          # marks agent/ as a Python package
│   ├── graph.py             # LangGraph ReAct agent + system prompt
│   └── tools.py             # API call tools
├── dummy_customer_api.py    # Flask API with 25 fake orders
├── prediction.py            # linear regression on order totals
├── main.py                  # Textual TUI — entry point
├── requirements.txt         # all dependencies
├── .env                     # your API key (never committed)
└── .gitignore
```

---

## UI controls

| Action | How |
|--------|-----|
| Submit a query | Type and press `Enter` or click **Submit** |
| Clear the log | Click **Clear** |
| Quit | Press `Ctrl+C` |

---

## Stats panel

The right-hand panel runs a linear regression model over all 25 order totals and shows:

- **Predicted next order value** — what the model expects order 1026 to be
- **Trend** — whether order values are trending up or down
- **Average order total** — mean across all 25 orders
- **R² score** — how well the regression fits the data

---

## Key dependencies

| Package | Purpose |
|---------|---------|
| `flask` | local order API |
| `langgraph` | agent graph orchestration |
| `langchain` + `langchain-openai` | LLM tooling |
| `requests` | HTTP calls to the API |
| `python-dotenv` | loads the `.env` file |
| `textual` | terminal UI |
| `scikit-learn` + `numpy` | linear regression model |