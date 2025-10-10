from app.agents.retrieval_agent import RetrievalAgent

if __name__ == "__main__":
    agent = RetrievalAgent()
    answer = agent.run("What’s our onboarding policy?")
    print("\n💬 Agent response:\n", answer)
