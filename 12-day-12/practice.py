# Import the Pinecone library
from pinecone import Pinecone

# Initialize the Pinecone client
pc = Pinecone(api_key="YOUR_API_KEY")


############################################################################
# Import ServerlessSpec
from pinecone import ServerlessSpec

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="API_KEY")

# Create your Pinecone index
pc.create_index(
    name="my-first-index",
    dimension=256,
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

############################################################################
# Set up the client with your API key
pc = Pinecone(api_key="pcsk_7CGK1Z_4dcXhH9GpXxK1zZE1rPBf6cWhsJR1cuJJXUJv4KZPkGwyLmjwqkK18RNSxMqb5L")

# Connect to your index
index = pc.Index("my-first-index")

# Print the index statistics
print(index.describe_index_stats())

############################################################################
# Initialize the Pinecone client using your API key
pc = Pinecone(api_key="YOUR_API_KEY")

# Create your Pinecone index
pc.create_index(
    name="datacamp-index", 
    dimension=1536, 
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-east-1'
    )
)

# Check that each vector has a dimensionality of 1536
vector_dims = [len(vector['values']) == 1536 for vector in vectors]
print(all(vector_dims))

############################################################################
# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="pcsk_7CGK1Z_4dcXhH9GpXxK1zZE1rPBf6cWhsJR1cuJJXUJv4KZPkGwyLmjwqkK18RNSxMqb5L")

index = pc.Index('datacamp-index')
ids = ['2', '5', '8']

# Fetch the vectors from the connected Pinecone index
fetched_vectors = index.fetch(ids=ids)

# Extract the metadata from each result in fetched_vectors
metadatas = [fetched_vectors['vectors'][id]['metadata'] for id in ids]
print(metadatas)