from app.agents.retrieval_agent import RetrievalAgent
from app.agents.report_agent import ReportAgent
from app.agents.automation_agent import AutomationAgent
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class SupervisorAgent:
    """Routes user queries to the appropriate sub-agent."""

    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.report_agent = ReportAgent()
        self.automation_agent = AutomationAgent()
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

    def handle_query(self, query: str) -> str:
        routing_prompt = f"""
        You are the Supervisor Agent. Choose which agent should handle this query:
        - RetrievalAgent (factual or document-based)
        - ReportAgent (summaries or insights)
        - AutomationAgent (tasks, actions, or sending results)

        Respond with only one word: Retrieval, Report, or Automation.

        Query: {query}
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": routing_prompt}],
        )

        decision = response.choices[0].message.content.strip().lower()
        print(f"🧭 Supervisor decided: {decision}")

        if "report" in decision:
            return self.report_agent.run("Summary request received.", query)
        elif "automation" in decision:
            return self.automation_agent.run(query)
        else:
            return self.retrieval_agent.run(query)
