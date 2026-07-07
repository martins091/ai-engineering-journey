# Day 12: Pinecone Vector Database 🚀

## Table of Contents
1. [What is Pinecone?](#what-is-pinecone)
2. [Key Concepts](#key-concepts)
3. [Setting Up Pinecone](#setting-up-pinecone)
4. [Creating Indexes](#creating-indexes)
5. [Managing Indexes](#managing-indexes)
6. [Vector Ingestion](#vector-ingestion)
7. [Fetching Vectors](#fetching-vectors)
8. [Code Snippets](#code-snippets)
9. [Common Errors & Fixes](#common-errors--fixes)
10. [Quick Reference](#quick-reference)

---

## What is Pinecone?

**Pinecone** is a **fully-managed vector database** for building and scaling AI applications.

### Key Benefits:
- ✅ **Managed Service** - No server maintenance
- ✅ **Scalable** - Handles millions of vectors
- ✅ **Fast** - Optimized for vector search
- ✅ **Easy** - Simple Python API
- ✅ **Free Tier** - Starter account available

### What It's Used For:
- Semantic search engines
- Recommendation systems
- Chatbots and AI assistants
- Similarity matching
- RAG (Retrieval-Augmented Generation)

---

## Key Concepts

### 1. Indexes
**Index = A collection of vectors** (like a table in SQL)
Pinecone Index: "products"
├── Vector 1: iPhone embedding
├── Vector 2: Samsung embedding
├── Vector 3: Headphones embedding
└── Vector 4: Laptop embedding

text

### 2. Serverless vs Pod-Based

| Serverless | Pod-Based |
|------------|-----------|
| Scales automatically | Fixed hardware (pods) |
| Pay for what you use | Pay for reserved capacity |
| Good for most cases | Good for predictable loads |
| ✅ We use this! | ❌ Not in this course |

### 3. Namespaces
**Namespaces = Folders inside an index** for organizing vectors
Index: "products"
├── Namespace: "electronics"
│ ├── iPhone
│ └── Samsung
├── Namespace: "clothing"
│ ├── T-shirt
│ └── Jeans
└── Namespace: "books"
├── Fiction
└── Non-fiction

text

### 4. Records
**Record = Vector + Metadata**

```python
{
    "id": "unique_id",
    "values": [0.1, 0.2, ...],  # The embedding
    "metadata": {                # Extra info
        "name": "iPhone 15",
        "price": 799
    }
}
5. Read Units (RUs)
How Pinecone measures usage:

Operation	RUs Cost
Fetch up to 10 records	1 RU
Query	Varies
List vectors	1 RU per 10 records
6. Organizations Hierarchy
text
Organization (Top level)
├── Projects
│   ├── Indexes
│   │   ├── Namespaces
│   │   │   └── Records (Vectors + Metadata)
│   │   └── Namespaces
│   └── Indexes
└── Projects
Roles:

Organization Owner - Full access (billing, users, all projects)

Organization User - Limited access (only assigned projects)

Setting Up Pinecone
Step 1: Get API Key
Visit pinecone.io

Sign up for Starter account (free)

Go to "API Keys" page

Copy your API key (starts with pc-)

Step 2: Install Pinecone
bash
pip install pinecone
Step 3: Initialize Client
python
from pinecone import Pinecone, ServerlessSpec

# Initialize with your API key
pc = Pinecone(api_key="YOUR_API_KEY")

# Your API key looks like: pc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Creating Indexes
Basic Index Creation
python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="YOUR_API_KEY")

# Create a serverless index
pc.create_index(
    name="my-index",
    dimension=1536,              # OpenAI embeddings = 1536
    metric="cosine",             # Similarity metric
    spec=ServerlessSpec(
        cloud="aws",             # Cloud provider
        region="us-east-1"       # Region
    )
)
Check Index Exists First
python
# Safer approach
if "my-index" not in pc.list_indexes():
    pc.create_index(
        name="my-index",
        dimension=1536,
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print("Index created!")
else:
    print("Index already exists!")
Index Parameters:
Parameter	Description	Example
name	Index name	"product-index"
dimension	Vector size	1536 (OpenAI)
metric	Similarity method	"cosine" (most common)
cloud	Cloud provider	"aws", "gcp", "azure"
region	Data location	"us-east-1"
Managing Indexes
Connect to an Index
python
# Connect to existing index
index = pc.Index("my-index")
Get Index Statistics
python
# Check index status
stats = index.describe_index_stats()
print(stats)

# Output:
# {
#     'dimension': 1536,
#     'index_fullness': 0.01,
#     'total_vector_count': 100,
#     'namespaces': {'': {'vector_count': 100}}
# }
List All Indexes
python
# See all your indexes
indexes = pc.list_indexes()
print(indexes)  # ['my-index', 'products', 'reviews']
Delete an Index
python
# ⚠️ CAREFUL: This deletes ALL data permanently!
pc.delete_index("my-index")

# Verify deletion
print(pc.list_indexes())  # 'my-index' no longer appears
Vector Ingestion
Vector Structure
python
vector = {
    "id": "unique_id",           # Required: Unique identifier
    "values": [0.1, 0.2, ...],   # Required: The embedding
    "metadata": {                # Optional: Extra info
        "name": "iPhone 15",
        "price": 799,
        "category": "Electronics"
    }
}
Check Dimensionality
python
# Check all vectors match index dimension
vectors = [...]  # Your list of vectors

vector_dims = [len(vector['values']) == 1536 for vector in vectors]
all_match = all(vector_dims)

if all_match:
    print("All vectors match dimension!")
else:
    print("Some vectors have wrong dimension!")
Upsert Vectors
python
# Insert or update vectors
index.upsert(vectors=vectors)

# Verify insertion
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
Upsert with Namespace
python
# Add vectors to a specific namespace
index.upsert(
    vectors=vectors,
    namespace="electronics"
)
Bulk Upsert (Efficient)
python
# Process large batches
batch_size = 100

for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    index.upsert(vectors=batch)
    print(f"Upserted {i+batch_size} vectors")
Fetching Vectors
Basic Fetch
python
# Fetch by ID
result = index.fetch(ids=["vec_1", "vec_2"])

# Access results
for vector_id, data in result['vectors'].items():
    print(f"ID: {vector_id}")
    print(f"Values: {data['values'][:5]}...")  # First 5 numbers
    print(f"Metadata: {data['metadata']}")
Fetch from Namespace
python
# Fetch from specific namespace
result = index.fetch(
    ids=["vec_1", "vec_2"],
    namespace="electronics"
)
Check if Vector Exists
python
result = index.fetch(ids=["vec_1"])
if 'vec_1' in result['vectors']:
    print("Vector exists!")
else:
    print("Vector not found")
Read Units Usage
python
result = index.fetch(ids=["vec_1", "vec_2", "vec_3"])
print(f"Read units used: {result['usage']['read_units']}")
# 1 RU per 10 records fetched
Code Snippets
Complete Setup Example
python
from pinecone import Pinecone, ServerlessSpec

# 1. Initialize
pc = Pinecone(api_key="YOUR_API_KEY")

# 2. Create index
index_name = "product-index"

if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1536,
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
    print(f"Created index: {index_name}")

# 3. Connect to index
index = pc.Index(index_name)

# 4. Check index status
print(index.describe_index_stats())
Create and Ingest Example
python
import numpy as np

# Create sample vectors
dimension = 1536
vectors = []

for i in range(10):
    vector = {
        "id": f"vec_{i}",
        "values": np.random.rand(dimension).tolist(),
        "metadata": {
            "index": i,
            "category": "sample",
            "created": "2024-01-01"
        }
    }
    vectors.append(vector)

# Check dimensions
if all(len(v['values']) == dimension for v in vectors):
    # Upsert
    index.upsert(vectors=vectors)
    print(f"Added {len(vectors)} vectors")

# Verify
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
Fetch Example
python
# Fetch specific vectors
result = index.fetch(ids=["vec_0", "vec_1", "vec_2"])

# Display results
for vector_id, data in result['vectors'].items():
    print(f"\nVector: {vector_id}")
    print(f"Metadata: {data['metadata']}")
    print(f"First 5 values: {data['values'][:5]}")

print(f"Read units: {result['usage']['read_units']}")
Error Handling Example
python
from pinecone import exceptions

try:
    # Try to create index
    pc.create_index(
        name="my-index",
        dimension=1536,
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
except exceptions.PineconeApiException as e:
    if "already exists" in str(e):
        print("Index already exists!")
    else:
        print(f"Error: {e}")

# Connect to index
try:
    index = pc.Index("my-index")
    stats = index.describe_index_stats()
    print("Connected successfully!")
except exceptions.NotFoundException:
    print("Index not found!")
Common Errors & Fixes
Error	Cause	Solution
401 Unauthorized	Invalid API key	Get new key from Pinecone dashboard
404 Not Found	Index doesn't exist	Create index first or check name
Dimension mismatch	Wrong vector length	Match index dimension
Index already exists	Duplicate name	Use different name or skip creation
List conversion error	IDs not as list	Use ids=["id1"] not ids="id1"
Namespace not found	Wrong namespace	Use correct namespace or omit
Quick Reference
Pinecone Methods
Method	Purpose
Pinecone(api_key)	Initialize client
pc.create_index()	Create new index
pc.list_indexes()	List all indexes
pc.delete_index()	Delete index (⚠️ permanent)
pc.Index(name)	Connect to index
index.describe_index_stats()	Get index info
index.upsert(vectors)	Insert/update vectors
index.fetch(ids)	Get vectors by ID
index.query(vector)	Search similar vectors
Common Parameters
python
# Index creation
pc.create_index(
    name="index-name",      # String
    dimension=1536,         # Integer (matches embedding size)
    metric="cosine",        # "cosine", "euclidean", "dotproduct"
    spec=ServerlessSpec(    # Serverless configuration
        cloud="aws",        # "aws", "gcp", "azure"
        region="us-east-1"  # Region
    )
)

# Upsert
index.upsert(
    vectors=[...],          # List of vector dictionaries
    namespace="name"        # Optional: namespace
)

# Fetch
index.fetch(
    ids=["id1", "id2"],     # List of vector IDs
    namespace="name"        # Optional: namespace
)
Vector Structure
python
{
    "id": "unique_string",           # Required
    "values": [0.1, 0.2, ...],       # Required (list of floats)
    "metadata": {                    # Optional (dict)
        "key1": "value1",
        "key2": 123,
        "key3": True
    }
}
Best Practices
1. Check Dimensionality Before Upsert
python
# Always check before upserting
if all(len(v['values']) == dimension for v in vectors):
    index.upsert(vectors=vectors)
else:
    print("Dimension mismatch! Fix vectors first.")
2. Batch Your Upserts
python
# Upsert in batches for large datasets
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    index.upsert(vectors=batch)
3. Fetch Multiple IDs at Once
python
# ✅ Efficient
result = index.fetch(ids=["id1", "id2", "id3"])

# ❌ Inefficient (uses 3 RUs)
for id in ["id1", "id2", "id3"]:
    result = index.fetch(ids=[id])
4. Use Namespaces for Organization
python
# Organize by category
index.upsert(vectors=electronics, namespace="electronics")
index.upsert(vectors=clothing, namespace="clothing")
5. Keep Metadata Small
python
# ✅ Good
metadata = {
    "id": 123,
    "category": "electronics",
    "price": 799
}

# ❌ Bad (too large)
metadata = {
    "full_description": "Very long text here..."  # Don't do this!
}
Summary
What You Learned Today:
✅ Pinecone Basics - What it is and why use it

✅ Indexes - Creating and managing

✅ Serverless vs Pod - Choosing the right type

✅ Namespaces - Organizing vectors

✅ Vector Ingestion - Adding data to Pinecone

✅ Fetching - Getting vectors by ID

✅ Read Units - Understanding usage costs

✅ Error Handling - Common issues and fixes

Key Takeaways:
Pinecone makes it easy to store and search embeddings at scale!

Index = Collection of vectors

Upsert = Add or update vectors

Fetch = Get vectors by ID

Query = Find similar vectors

Namespace = Organize data

RUs = Usage measurement

Additional Resources
Pinecone Documentation

Pinecone API Reference

Pinecone Pricing

"Vector databases make AI applications scale!" 🚀

Happy Building! 💻✨
