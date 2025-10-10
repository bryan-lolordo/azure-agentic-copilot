import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

class ReportAgent:
    """Generates summaries, insights, or executive reports from given context."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

    def run(self, context: str, query: str = None) -> str:
        """Takes context text and generates a concise, analytical summary."""
        prompt = f"""
        You are a Report Agent that writes professional summaries and extracts insights.
        Read the following information and produce a short executive-style summary.

        Context:
        {context}

        {'User request: ' + query if query else ''}

        Focus on clarity, accuracy, and key points.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
