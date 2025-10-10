import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AutomationAgent:
    """Handles workflow or action requests such as sending emails or triggering flows."""

    def __init__(self):
        self.flow_url = os.getenv("POWER_AUTOMATE_URL")

    def run(self, message: str) -> str:
        """Simulates triggering a workflow or calls Power Automate."""
        if not self.flow_url:
            # Simulate success for demo/testing
            return f"✅ (Simulated) Automation triggered: {message}"
        
        try:
            response = requests.post(self.flow_url, json={"message": message})
            if response.status_code == 200:
                return "✅ Automation triggered successfully."
            else:
                return f"⚠️ Automation failed: {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ Error triggering automation: {e}"
