########################################################################################
# Initialize the Pinecone client with your API key
import itertools


pc = Pinecone(api_key="YOUR_API_KEY")

index = pc.Index('datacamp-index')

# Retrieve the MOST similar vector with the year 2024
query_result = index.query(
    vector=vector,
    top_k=1,
    filter={"year": 2024},
    include_metadata=True
)
print(query_result)

#######################################################################
# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="pcsk_7CGK1Z_4dcXhH9GpXxK1zZE1rPBf6cWhsJR1cuJJXUJv4KZPkGwyLmjwqkK18RNSxMqb5L")

index = pc.Index('datacamp-index')

# Update the values of vector ID 7
index.update(id="7", values=vector)

# Fetch vector ID 7
fetched_vector = index.fetch(ids=["7"])
print(fetched_vector)


###################################################################################################
# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="YOUR_API_KEY")

index = pc.Index('datacamp-index')

# Update the metadata of vector ID 7
index.update(
    id="7",
    set_metadata={
        "genre": "thriller",
        "year": 2024
    }
)

# Fetch vector ID 7
fetched_vector = index.fetch(ids=["7"])
print(fetched_vector)


###############################################################
def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    # Convert the iterable into an iterator
    it = iter(iterable)
    # Slice the iterator into chunks of size batch_size
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        # Yield the chunk
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


########################################################################
# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="YOUR_API_KEY")

index = pc.Index('datacamp-index')

# Upsert vectors in batches of 100
for chunk in chunks(vectors):
    index.upsert(vectors=chunk)

# Retrieve statistics of the connected Pinecone index
print(index.describe_index_stats())

########################################################################
# Initialize the client
pc = Pinecone(api_key="YOUR_API_KEY", pool_threads=20)

index = pc.Index('datacamp-index')

# Upsert vectors in batches of 200 vectors
with pc.Index('datacamp-index', pool_threads=20) as index:
    async_results = [index.upsert(vectors=chunk, async_req=True) for chunk in chunks(vectors, batch_size=200)]
    [async_result.get() for async_result in async_results]

# Retrieve statistics of the connected Pinecone index
print(index.describe_index_stats())