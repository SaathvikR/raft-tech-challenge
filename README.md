# Raft AI Engineer Coding Challenge

An AI agent that accepts natural language queries about orders, fetches raw unstructured data from a local API, parses it using an LLM, and returns clean structured JSON — all inside an interactive terminal UI.

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
        │
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

- Python 3.10+
- An [OpenRouter](https://openrouter.ai) API key

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SaathvikR/raft-tech-challenge.git
cd raft-tech-challenge
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Create your `.env` file

Create a file called `.env` in the root of the project:

```bash
touch .env
```

Open it and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_openrouter_key_here
```

To get an API key:
- Go to [https://openrouter.ai](https://openrouter.ai)
- Sign up and navigate to **Keys**
- Create a new key and paste it above

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## Running the App

You need two terminals running at the same time.

### Terminal 1 — Start the order API

```bash
source .venv/bin/activate
python3 dummy_customer_api.py
```

You should see:
```
* Running on http://0.0.0.0:5001
```

### Terminal 2 — Start the agent UI

```bash
source .venv/bin/activate
python3 main.py
```

A terminal UI will launch. Type your query in the input box at the bottom and press **Enter** or click **Submit**.

---

## Example Queries

```
Show me all orders where the buyer was located in Ohio and total value was over 500
Show me all orders from Texas
Which orders have a total over 1000?
Find orders for Rachel Kim
Show me all orders under $200
```

---

## Example Output

```json
{
  "orders": [
    { "orderId": "1001", "buyer": "John Davis", "state": "OH", "total": 742.1 },
    { "orderId": "1003", "buyer": "Mike Turner", "state": "OH", "total": 1299.99 },
    { "orderId": "1005", "buyer": "Chris Myers", "state": "OH", "total": 512.0 }
  ]
}
```

---

## Project Structure

```
raft-tech-challenge/
├── agent/
│   ├── __init__.py        # marks agent/ as a Python package
│   ├── graph.py           # LangGraph ReAct agent setup
│   └── tools.py           # API call tools (fetch_all_orders, fetch_order_by_id)
├── dummy_customer_api.py  # local Flask API serving fake order data
├── main.py                # Textual terminal UI + agent runner
├── requirements.txt       # Python dependencies
├── .env                   # your API key (never committed)
└── .gitignore
```

---

## Controls

| Action | How |
|--------|-----|
| Submit query | Type and press `Enter` or click **Submit** |
| Clear log | Click **Clear** |
| Quit | Press `Ctrl+C` |

---

## Dependencies

All installed via `requirements.txt`:

| Package | Purpose |
|---------|---------|
| `flask` | Runs the dummy order API |
| `langgraph` | Agent graph orchestration |
| `langchain` | LLM tooling and abstractions |
| `langchain-openai` | OpenAI-compatible LLM client |
| `requests` | HTTP calls to the local API |
| `python-dotenv` | Loads `.env` file |
| `textual` | Terminal UI framework |
