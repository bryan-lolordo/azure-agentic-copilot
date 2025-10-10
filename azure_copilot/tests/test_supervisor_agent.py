from app.agents.supervisor_agent import SupervisorAgent

if __name__ == "__main__":
    supervisor = SupervisorAgent()

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = supervisor.handle_query(query)
        print("\n💬 Final response:\n", response)
