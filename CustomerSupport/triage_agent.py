import json
import ollama
from prompts import TRIAGE_PROMPT

def run_triage(message: str):

    # ----------------------
    # Rule-based override
    # ----------------------
    text = message.lower()

    if "refund" in text:
        return {
            "intent": "refund",
            "urgency": "high"
        }

    if "where is my order" in text or "order status" in text:
        return {
            "intent": "order_status",
            "urgency": "medium"
        }

    prompt = TRIAGE_PROMPT.format(message=message)

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    output = response["message"]["content"]

    try:
        return json.loads(output)
    except:
        return {
            "intent": "other",
            "urgency": "low",
            "raw": output
        }
