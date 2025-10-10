from app.agents.retrieval_agent import RetrievalAgent
from app.agents.supervisor_agent import SupervisorAgent

if __name__ == "__main__":
    retrieval_agent = RetrievalAgent()
    supervisor = SupervisorAgent(retrieval_agent)

    while True:
        query = input("\nAsk me something (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = supervisor.handle_query(query)
        print("\n💬 Final response:\n", response)
