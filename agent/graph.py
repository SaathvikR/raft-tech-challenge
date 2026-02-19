import os
from dotenv import load_dotenv

load_dotenv()

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

SYSTEM_PROMPT = SystemMessage(content="""You are an order-data agent.
Rules:
- Call fetch_all_orders ONCE with limit=10. Do not call it multiple times.
- Parse the raw text and filter based on the user query.
- Respond with ONLY a valid JSON object. No explanation, no analysis, no extra text.
- Use exactly this format:
{"orders": [{"orderId": "...", "buyer": "...", "state": "...", "total": 0.0}]}
- If no orders match, return: {"orders": []}
""")

agent = create_react_agent(llm, tools=[fetch_all_orders, fetch_order_by_id],
                           prompt=SYSTEM_PROMPT)