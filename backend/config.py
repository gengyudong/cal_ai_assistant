import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_KEY")
CAL_API_KEY = os.getenv("CAL_API_KEY")
CAL_BASE_URL = os.getenv("CAL_BASE_URL")
CAL_EMAIL = os.getenv("CAL_EMAIL")
CAL_EVENT_TYPE_ID_FILEPATH = "event_type_id.json"

# Load CAL_EVENT_TYPE_ID from event_type_id.json
with open(CAL_EVENT_TYPE_ID_FILEPATH, "r") as f:
    CAL_EVENT_TYPE_ID = json.load(f)