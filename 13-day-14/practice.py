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