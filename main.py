import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from agent.graph import agent

logging.basicConfig(level=logging.INFO)

def run(query: str):
    logging.info(f"Query: {query}")
    result = agent.invoke({"messages": [("user", query)]})

    # Debug: print all messages to see what came back
    for msg in result["messages"]:
        logging.info(f"Message type: {type(msg).__name__}, content: {msg.content[:200] if msg.content else 'EMPTY'}")

    # Get the last non-empty AI message
    output = ""
    for msg in reversed(result["messages"]):
        if msg.content and msg.content.strip():
            output = msg.content
            break

    logging.info(f"Raw output: {output}")

    if not output:
        return {"orders": [], "error": "No response from model"}

    # Try direct parse
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block
    import re
    match = re.search(r'\{.*\}', output, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {"orders": [], "error": output}

if __name__ == "__main__":
    query = input("Enter your order query: ")
    print(json.dumps(run(query), indent=2))