import os
from dotenv import load_dotenv

load_dotenv()

# Force set for langchain's internal validation
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from agent.tools import fetch_all_orders, fetch_order_by_id

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:exacto",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

SYSTEM_PROMPT = SystemMessage(content="""You are an order-data agent. When given a natural language query:
1. Use tools to fetch raw order data from the API.
2. Parse the unstructured text carefully.
3. Filter results according to the user's query.
4. Return ONLY valid JSON in this exact shape:
{"orders": [{"orderId": "...", "buyer": "...", "state": "...", "total": 0.0}]}
Never hallucinate orders. If none match, return {"orders": []}.
""")

agent = create_react_agent(llm, tools=[fetch_all_orders, fetch_order_by_id],
                           prompt=SYSTEM_PROMPT)