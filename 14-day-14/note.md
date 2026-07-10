# Day 14: Multitenancy and Namespaces 🚀

## Table of Contents
1. [What is Multitenancy?](#what-is-multitenancy)
2. [Multitenancy Strategies](#multitenancy-strategies)
3. [Creating Namespaces](#creating-namespaces)
4. [Inspecting Namespaces](#inspecting-namespaces)
5. [Querying Namespaces](#querying-namespaces)
6. [Operations with Namespaces](#operations-with-namespaces)
7. [Complete Examples](#complete-examples)
8. [Key Takeaways](#key-takeaways)

---

## What is Multitenancy?

**Multitenancy = Serving multiple users/groups (tenants) with one system**

Think of it like:
- **One apartment building** 🏢 (Index)
- **Many apartments** 🚪 (Namespaces)
- Each tenant has their own private space!

### Why Use Namespaces?

| Benefit | Explanation |
|---------|-------------|
| **Data Isolation** | Each tenant's data is separate |
| **Security** | Users can't see other users' data |
| **Faster Queries** | Search only relevant namespace |
| **Easier Management** | Delete/update one tenant at a time |
| **Cost Efficiency** | One index for many tenants |

---

## Multitenancy Strategies

### 1. Namespaces (Best for Most Cases)
Index: "products"
├── Namespace: "company_a"
│ ├── Product 1
│ └── Product 2
├── Namespace: "company_b"
│ ├── Product 3
│ └── Product 4
└── Namespace: "company_c"
└── Product 5

✅ Easy to implement
✅ Fast queries
✅ Data isolation
✅ Auto-created on upsert

text

### 2. Metadata Filtering
Index: "products"
├── Product 1 (metadata: tenant="company_a")
├── Product 2 (metadata: tenant="company_b")
└── Product 3 (metadata: tenant="company_a")

✅ Query across tenants
❌ Slower (must filter)
❌ Harder to manage
❌ Cost tracking challenges

text

### 3. Separate Indexes
Index: "company_a_products"
Index: "company_b_products"
Index: "company_c_products"

✅ Maximum isolation
❌ Expensive
❌ Harder to maintain
❌ More effort

Strategy Comparison
Strategy	Pros	Cons	When to Use
Namespaces	✅ Easy
✅ Fast
✅ Isolated
✅ Auto-created	❌ Shared resources	Most use cases
Metadata	✅ Cross-tenant query	❌ Slower
❌ Harder to manage	Need cross-tenant queries
Separate Indexes	✅ Maximum isolation	❌ Expensive
❌ More work	Strict compliance needs
Creating Namespaces
Namespaces are created automatically on upsert!
python
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("datacamp-index")

# Upsert into namespace "company_a" (auto-created)
index.upsert(
    vectors=vectors_a,
    namespace="company_a"
)

# Upsert into namespace "company_b" (auto-created)
index.upsert(
    vectors=vectors_b,
    namespace="company_b"
)
Important: No need to create namespace first! Just upsert with namespace parameter.

Inspecting Namespaces
python
# Check all namespaces
stats = index.describe_index_stats()
print(stats)
Example Output:
python
{
    'dimension': 1536,
    'index_fullness': 0.01,
    'total_vector_count': 100,
    'namespaces': {
        'company_a': {'vector_count': 50},
        'company_b': {'vector_count': 30},
        'company_c': {'vector_count': 20}
    }
}
Access Specific Namespace Info:
python
stats = index.describe_index_stats()
for namespace, data in stats['namespaces'].items():
    print(f"{namespace}: {data['vector_count']} vectors")
Querying Namespaces
Basic Query with Namespace
python
# Query only specific namespace
results = index.query(
    vector=query_vector,
    top_k=5,
    namespace="company_a",  # ← Only search this namespace!
    include_metadata=True
)

for match in results['matches']:
    print(f"ID: {match['id']}, Score: {match['score']}")
Default Namespace (Empty String)
python
# Queries default namespace (empty string)
results = index.query(
    vector=query_vector,
    top_k=5
)

# Same as:
results = index.query(
    vector=query_vector,
    namespace="",
    top_k=5
)
Operations with Namespaces
1. Upsert to Namespace
python
# Add vectors to a specific namespace
index.upsert(
    vectors=vectors,
    namespace="company_a"
)
2. Query Namespace
python
# Search only in a specific namespace
results = index.query(
    vector=query_vector,
    namespace="company_a",
    top_k=5
)
3. Fetch from Namespace
python
# Fetch vectors by ID from a specific namespace
fetched = index.fetch(
    ids=["vec_1", "vec_2"],
    namespace="company_a"
)
4. Delete from Namespace
python
# Delete specific IDs from namespace
index.delete(
    ids=["vec_1", "vec_2"],
    namespace="company_a"
)

# Delete ALL vectors from namespace
index.delete(
    delete_all=True,
    namespace="company_a"
)
5. Update in Namespace
python
# Update vector in specific namespace
index.update(
    id="vec_123",
    values=[0.1, 0.2, ...],
    namespace="company_a"
)

# Update metadata in specific namespace
index.update(
    id="vec_123",
    set_metadata={"genre": "action"},
    namespace="company_a"
)
Complete Examples
Example 1: Multi-tenant E-commerce
python
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
Example 2: Multi-tenant with Namespace Management
python
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
Example 3: User-Specific Recommendations
python
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
Key Points
IDs Only Need to Be Unique Within Namespace
python
# ✅ Valid: Same ID in different namespaces
index.upsert(
    vectors=[{"id": "product_1", "values": [...]}],
    namespace="company_a"
)
index.upsert(
    vectors=[{"id": "product_1", "values": [...]}],
    namespace="company_b"
)
# Both are fine! IDs only need to be unique WITHIN each namespace
Namespaces Are Auto-Created
python
# No need to create namespace first!
# Just upsert with namespace parameter
index.upsert(
    vectors=vectors,
    namespace="new_namespace"  # Auto-created!
)
Default Namespace
python
# When no namespace is specified, uses empty string ""
index.upsert(vectors=vectors)  # Goes to default namespace

# Empty namespace appears as '' in stats
stats = index.describe_index_stats()
print(stats['namespaces'])  # {'': {'vector_count': 10}}
Common Errors and Fixes
Error	Cause	Solution
Namespace not found	Wrong namespace name	Check spelling or use correct namespace
Duplicate ID in namespace	Same ID in same namespace	Use unique IDs within namespace
Delete_all without namespace	Missing namespace	Specify namespace or use delete_all=True
Best Practices
1. Use Namespaces for Multi-tenant Apps
python
# ✅ Good: Each tenant gets their own namespace
index.upsert(vectors=tenant_a_vectors, namespace="tenant_a")
index.upsert(vectors=tenant_b_vectors, namespace="tenant_b")
2. Query Only Relevant Namespace
python
# ✅ Fast: Query only relevant namespace
results = index.query(
    vector=query_vector,
    namespace="tenant_a",  # Only search tenant A
    top_k=5
)

# ❌ Slow: Query everything then filter
results = index.query(
    vector=query_vector,
    top_k=100  # Must search everything
)
3. Clean Up Old Namespaces
python
# ✅ Good: Delete unused namespaces
index.delete(delete_all=True, namespace="old_tenant")
4. Use Namespaces for Different Environments
python
# Development vs Production
index.upsert(vectors=dev_vectors, namespace="dev")
index.upsert(vectors=prod_vectors, namespace="prod")
Summary
What You Learned Today:
✅ Multitenancy - One system serving multiple tenants

✅ Namespaces - Isolated partitions within an index

✅ Auto-creation - Namespaces created on first upsert

✅ Operations - Query, fetch, update, delete with namespaces

✅ ID Uniqueness - IDs only need to be unique within namespace

Key Takeaways:
Namespaces = Private apartments in one building (index)!

Multitenancy = One system, many users/groups!

Isolation = Each tenant's data stays separate!

Auto-creation = No setup needed, just use it!

Resources
Pinecone Namespaces Documentation

Pinecone Metadata Filtering