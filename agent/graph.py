import os
from dotenv import load_dotenv

load_dotenv()

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from agent.tools import fetch_all_orders, fetch_order_by_id

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:exacto",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

SYSTEM_PROMPT = SystemMessage(content="""You are an order-data agent.

Rules:
- Call fetch_all_orders ONCE. Do not call it multiple times.
- Filter the results based on what the user asked for.
- Return ONLY a JSON object, no explanation, no extra text.
- Format: {"orders": [{"orderId": "...", "buyer": "...", "state": "...", "total": 0.0}]}
- If nothing matches, return: {"orders": []}
""")

agent = create_react_agent(llm, tools=[fetch_all_orders, fetch_order_by_id], prompt=SYSTEM_PROMPT)