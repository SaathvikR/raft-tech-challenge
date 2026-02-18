import requests
from langchain_core.tools import tool

@tool
def fetch_all_orders(limit: int = 10) -> str:
    """Fetch raw orders from the customer API."""
    resp = requests.get(f"http://localhost:5001/api/orders?limit={limit}")
    resp.raise_for_status()
    return str(resp.json().get("raw_orders", []))

@tool
def fetch_order_by_id(order_id: str) -> str:
    """Fetch a single order by ID."""
    resp = requests.get(f"http://localhost:5001/api/order/{order_id}")
    return resp.json().get("raw_order", "not found")