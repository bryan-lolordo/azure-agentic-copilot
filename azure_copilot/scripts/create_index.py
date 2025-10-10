import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    HnswParameters,
)

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

credential = AzureKeyCredential(key)
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

# --- Define fields ---
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
    SearchField(
        name="embedding",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-vector-profile"
    ),
]

# --- Vector search configuration ---
algo = HnswAlgorithmConfiguration(
    name="my-hnsw-config",
    parameters=HnswParameters(
        m=4,
        ef_construction=400,
        ef_search=500,
        metric="cosine"
    )
)

vector_search = VectorSearch(
    algorithms=[algo],
    profiles=[
        VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="my-hnsw-config"
        )
    ]
)

# --- Create the index ---
index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search
)

try:
    result = index_client.create_or_update_index(index)
    print(f"✅ Successfully created or updated index '{result.name}'")
except Exception as e:
    print("⚠️ Error creating index:", e)
