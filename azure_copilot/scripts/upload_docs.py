import os, json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

load_dotenv()

# --- Azure setup ---
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

# --- Sample documents ---
docs = [
    {
        "id": "1",
        "content": "Our onboarding policy requires new employees to complete orientation and compliance training within the first 30 days.",
        "category": "policy"
    },
    {
        "id": "2",
        "content": "Quarter 3 incident summary: 5 minor system outages and 1 critical incident resolved within SLA.",
        "category": "report"
    },
    {
        "id": "3",
        "content": "Company values emphasize integrity, teamwork, and innovation across all business units.",
        "category": "values"
    }
]

# --- Generate embeddings and upload ---
for d in docs:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=d["content"]
    )
    d["embedding"] = response.data[0].embedding

search_client.upload_documents(docs)
print("✅ Uploaded sample documents successfully.")
