from dotenv import load_dotenv
from langflow.load import run_flow_from_json
import os
import requests
import pprint
from typing import Optional

load_dotenv() 

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "c7285561-d445-465e-8705-6d9fc7d5ec9d"
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = "content-planner-flow"

def ask_ai(profile, question):
    TWEAKS = {
        "TextInput-2mzUW": {
            "input_value": question
        },
        "TextOutput-wyIr6": {
            "input_value": profile
        },
    }

    result = run_flow_from_json(
        flow="ASKAI.json",
        input_value="message",
        session_id="",
        fallback_to_env_vars=True, 
        tweaks=TWEAKS
    )

    for output in result[0].outputs:
        msg = output.results["text"].text
        if msg:
            response_text = msg
            break

    return response_text

# -------------------------
# ------ MAIN FLOW --------
# -------------------------

def run_main_flow(goals, profile, notes):
    TWEAKS = {
        "TextInput-dmFn6": {
            "input_value": goals
        },
        "TextInput-NiTSR": {
            "input_value": profile
        },
        "TextInput-C5PH0": {
            "input_value": notes,
        },
    }

    return run_flow(
        "",
        tweaks=TWEAKS,
        application_token=APPLICATION_TOKEN,
    )

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    # Flow endpoint
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)

    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]