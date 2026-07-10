from http import client

from pinecone import Pinecone

# Initialize
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("products")

# Tenant 1: Electronics Store
electronics_vectors = [
    {"id": "prod_1", "values": [...], "metadata": {"name": "iPhone", "price": 999}},
    {"id": "prod_2", "values": [...], "metadata": {"name": "Samsung", "price": 899}}
]
index.upsert(vectors=electronics_vectors, namespace="electronics_store")

# Tenant 2: Clothing Store
clothing_vectors = [
    {"id": "prod_3", "values": [...], "metadata": {"name": "T-shirt", "price": 29}},
    {"id": "prod_4", "values": [...], "metadata": {"name": "Jeans", "price": 79}}
]
index.upsert(vectors=clothing_vectors, namespace="clothing_store")

# Query only Electronics Store
results = index.query(
    vector=query_vector,
    namespace="electronics_store",
    top_k=3,
    include_metadata=True
)

print("Electronics Store Results:")
for match in results['matches']:
    print(f"  {match['metadata']['name']}: ${match['metadata']['price']}")


# 1. Check all tenants
stats = index.describe_index_stats()
print("Current tenants:")
for namespace, data in stats['namespaces'].items():
    print(f"  {namespace}: {data['vector_count']} products")

# 2. Add new tenant
new_tenant_vectors = [...]  # Vectors for new tenant
index.upsert(
    vectors=new_tenant_vectors,
    namespace="new_tenant"
)

# 3. Search across all tenants (using metadata)
all_results = index.query(
    vector=query_vector,
    top_k=10,
    include_metadata=True
)

# 4. Delete a tenant's data
index.delete(
    delete_all=True,
    namespace="old_tenant"
)

# 5. Verify deletion
stats = index.describe_index_stats()
print("After deletion:")
for namespace, data in stats['namespaces'].items():
    print(f"  {namespace}: {data['vector_count']} products")



    # Each user gets their own namespace
user_id = "user_123"

# Store user's interaction history
user_vectors = [
    {"id": "viewed_1", "values": [...], "metadata": {"product": "iPhone", "action": "view"}},
    {"id": "purchased_1", "values": [...], "metadata": {"product": "Samsung", "action": "purchase"}}
]
index.upsert(vectors=user_vectors, namespace=f"user_{user_id}")

# Get recommendations based on user history
recommendations = index.query(
    vector=user_query_vector,
    namespace=f"user_{user_id}",
    top_k=5,
    include_metadata=True
)

# Clean up user data when they leave
index.delete(
    delete_all=True,
    namespace=f"user_{user_id}"
)

##################################################################################################################
# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="YOU_API_KEY")
index = pc.Index('datacamp-index')

# Upsert vector_set1 to namespace1
index.upsert(
  vectors=vector_set1,
  namespace="namespace1"
)

# Upsert vector_set2 to namespace2
index.upsert(
  vectors=vector_set2,
  namespace="namespace2"
)

# Print the index statistics
print(index.describe_index_stats())

#######################################################################################################
# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="YOU_API_KEY")

# Create Pinecone index
pc.create_index(
    name='pinecone-datacamp', 
    dimension=1536,
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)

# Connect to index and print the index statistics
index = pc.Index('pinecone-datacamp')
print(index.describe_index_stats())


########################################################################################################
# Initialize the Pinecone client
pc = Pinecone(api_key="YOU_API_KEY")
index = pc.Index('pinecone-datacamp')

batch_limit = 100

for batch in np.array_split(df, len(df) / batch_limit):
    # Extract the metadata from each row
    metadatas = [{
      "text_id": row['id'],
      "text": row['text'],
      "title": row['title']} for _, row in batch.iterrows()]
    texts = batch['text'].tolist()
    
    ids = [str(uuid4()) for _ in range(len(texts))]
    
    # Encode texts using OpenAI
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    embeds = [np.array(x.embedding) for x in response.data]
    
    # Upsert vectors to the correct namespace
    index.upsert(vectors=zip(ids, embeds, metadatas), namespace="squad_dataset")

    ##########################################################################################################
    # Initialize the Pinecone client
pc = Pinecone(api_key="YOU_API_KEY")
index = pc.Index('pinecone-datacamp')

query = "What is in front of the Notre Dame Main Building?"

# Create the query vector
query_response = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
)
query_emb = query_response.data[0].embedding

# Query the index and retrieve the top five most similar vectors
retrieved_docs = index.query(
    vector=query_emb,
    top_k=5,
    namespace="squad_dataset",
    include_metadata=True
)

for result in retrieved_docs['matches']:
    print(f"{result['id']}: {round(result['score'], 2)}")
    print('\n')

    #########################################################################################################
    # Initialize the Pinecone client
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index('pinecone-datacamp')

batch_limit = 100

for batch in np.array_split(youtube_df, len(youtube_df) / batch_limit):
    # Extract the metadata from each row
    metadatas = [{
      "text_id": row['id'],
      "text": row['text'],
      "title": row['title'],
      "url": row['url'],
      "published": row['published']} for _, row in batch.iterrows()]
    texts = batch['text'].tolist()
    
    ids = [str(uuid4()) for _ in range(len(texts))]
    
    # Encode texts using OpenAI
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    embeds = [np.array(x.embedding) for x in response.data]
    
    # Upsert vectors to the correct namespace
    index.upsert(vectors=zip(ids, embeds, metadatas), namespace='youtube_rag_dataset')
    
print(index.describe_index_stats())

##########################################################################################################
# Initialize the Pinecone client
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index('pinecone-datacamp')

# Define a retrieve function that takes four arguments: query, top_k, namespace, and emb_model
def retrieve(query, top_k, namespace, emb_model):
    # Encode the input query using OpenAI
    query_response = client.embeddings.create(
        input=query,
        model=emb_model
    )
    
    query_emb = query_response.data[0].embedding
    
    # Query the index using the query_emb
    docs = index.query(vector=query_emb, top_k=top_k, namespace=namespace, include_metadata=True)
    
    retrieved_docs = []
    sources = []
    for doc in docs['matches']:
        retrieved_docs.append(doc['metadata']['text'])
        sources.append((doc['metadata']['title'], doc['metadata']['url']))
    
    return retrieved_docs, sources

documents, sources = retrieve(
  query="How to build next-level Q&A with OpenAI",
  top_k=3,
  namespace='youtube_rag_dataset',
  emb_model="text-embedding-3-small"
)
print(documents)
print(sources)