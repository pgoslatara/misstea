import os
from pathlib import Path

AGENT_MODEL = "gemini-2.5-flash"  # https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-preview
MEETING_ROOMS = [
    {"name": "Airflow", "screen": True},
    {"name": "Arcus", "screen": False},
    {"name": "Kafka", "screen": True},
    {"name": "Nimbus", "screen": True},
    {"name": "Python", "screen": True},
    {"name": "PyTorch", "screen": True},
]
MY_EMAIL_ADDRESS = os.environ["MY_EMAIL_ADDRESS"]
OUTLOOK_TOKEN_PATH = Path(
    __file__
).parent.parent.parent  # i.e in root directory of this repo
