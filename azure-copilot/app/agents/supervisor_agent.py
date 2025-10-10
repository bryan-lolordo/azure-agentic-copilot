import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

class SupervisorAgent:
    """
    Routes user queries to the correct sub-agent.
    For now, only RetrievalAgent is implemented.
    """

    def __init__(self, retrieval_agent):
        self.retrieval_agent = retrieval_agent
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

    def handle_query(self, query: str) -> str:
        # Ask GPT-4o-mini which agent should handle this
        routing_prompt = f"""
        You are the Supervisor Agent.
        Decide which sub-agent should handle this query:
        - RetrievalAgent  → factual or document-based
        - ReportAgent     → summaries or analytics
        - AutomationAgent → workflow or follow-up actions

        Respond with one word only: Retrieval, Report, or Automation.

        Query: {query}
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": routing_prompt}],
        )

        decision = response.choices[0].message.content.strip().lower()
        print(f"🧭 Supervisor decided: {decision}")

        if "report" in decision:
            return "ReportAgent not implemented yet."
        elif "automation" in decision:
            return "AutomationAgent not implemented yet."
        else:
            return self.retrieval_agent.run(query)
