import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

load_dotenv()

class RetrievalAgent:
    """Handles retrieval-augmented Q&A using Azure Search + GPT-4o."""
    def __init__(self):
        self.search_client = SearchClient(
            os.getenv("AZURE_SEARCH_ENDPOINT"),
            os.getenv("AZURE_SEARCH_INDEX"),
            AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

    def run(self, query: str) -> str:
        # --- Create embedding for query ---
        embedding_response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_vector = embedding_response.data[0].embedding

        # --- Vector search ---
        vector_query = VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=3,
            fields="embedding"
        )
        results = self.search_client.search(
            search_text="",
            vector_queries=[vector_query],
            select=["id", "content", "category"]
        )

        docs = [r["content"] for r in results]
        context = "\n".join(docs)

        # --- Ask GPT-4o-mini to answer ---
        prompt = f"""
        Use the following context to answer the user's question.

        Context:
        {context}

        Question: {query}
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
