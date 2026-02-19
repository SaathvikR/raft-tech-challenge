import requests
from langchain_core.tools import tool


@tool
def fetch_all_orders(limit: int = 25) -> str:
    """Fetch all raw orders from the customer API. Returns unstructured text orders."""
    resp = requests.get("http://localhost:5001/api/orders?limit=25")
    resp.raise_for_status()
    return str(resp.json().get("raw_orders", []))


@tool
def fetch_order_by_id(order_id: str) -> str:
    """Fetch a single order by its ID from the customer API."""
    resp = requests.get(f"http://localhost:5001/api/order/{order_id}")
    return resp.json().get("raw_order", "not found")