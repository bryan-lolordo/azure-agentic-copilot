import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

load_dotenv()

# --- Load env variables ---
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# --- Create clients ---
search_client = SearchClient(search_endpoint, index_name, AzureKeyCredential(search_key))
openai_client = AzureOpenAI(
    api_key=openai_key,
    azure_endpoint=openai_endpoint,
    api_version=api_version
)

# --- Step 1: Get query from user ---
query = input("Enter your question: ")

# --- Step 2: Generate query embedding ---
embedding_response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)
query_vector = embedding_response.data[0].embedding

# --- Step 3: Perform vector search ---
vector_query = VectorizedQuery(
    vector=query_vector,
    k_nearest_neighbors=3,
    fields="embedding"
)

results = search_client.search(
    search_text="",
    vector_queries=[vector_query],
    select=["id", "content", "category"]
)

# --- Step 4: Combine retrieved documents ---
docs = [r["content"] for r in results]
context = "\n".join(docs)
print(f"\n🔎 Retrieved {len(docs)} documents from Azure Search.\n")

# --- Step 5: Ask GPT-4o-mini to answer using the context ---
prompt = f"""
You are an intelligent assistant. Use the following documents to answer the user's question.

Documents:
{context}

Question: {query}
Answer clearly and concisely:
"""

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

answer = response.choices[0].message.content
print("💬 Response:\n", answer)
