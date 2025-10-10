import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")

credential = AzureKeyCredential(key)
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

try:
    indexes = list(index_client.list_indexes())
    print("✅ Connected! Indexes found:", [idx.name for idx in indexes])
except Exception as e:
    print("❌ Connection failed:", e)
