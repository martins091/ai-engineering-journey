# Day 13: Advanced Pinecone Operations 🚀

## Table of Contents
1. [Metadata Filtering](#metadata-filtering)
2. [Updating Vectors](#updating-vectors)
3. [Deleting Vectors](#deleting-vectors)
4. [Batching Upserts](#batching-upserts)
5. [Code Snippets](#code-snippets)
6. [Common Errors & Fixes](#common-errors--fixes)
7. [Quick Reference](#quick-reference)

---

## Metadata Filtering

### What is Metadata Filtering?

**Metadata filtering = Searching only within specific categories**

Instead of searching ALL vectors, you filter first, then search! This makes queries FASTER and MORE RELEVANT.

### Why Use Metadata Filtering?

| Without Filtering | With Filtering |
|-------------------|----------------|
| Searches ALL vectors | Searches only filtered vectors |
| Slower for large datasets | MUCH faster! |
| Returns results from everywhere | Returns only relevant results |
| Can't narrow down | Can filter by category, year, etc. |

### Filter Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$eq` | Equal to | `{"genre": {"$eq": "action"}}` |
| `$ne` | Not equal to | `{"genre": {"$ne": "comedy"}}` |
| `$gt` | Greater than | `{"year": {"$gt": 2020}}` |
| `$gte` | Greater than or equal | `{"year": {"$gte": 2020}}` |
| `$lt` | Less than | `{"year": {"$lt": 2020}}` |
| `$lte` | Less than or equal | `{"year": {"$lte": 2020}}` |
| `$in` | In a list | `{"genre": {"$in": ["action", "drama"]}}` |
| `$nin` | Not in a list | `{"genre": {"$nin": ["horror", "thriller"]}}` |

### Filter Examples

#### 1. Simple Equality
```python
# Find action movies
filter = {"genre": "action"}
2. Greater Than
python
# Find movies from 2020 or later
filter = {"year": {"$gt": 2019}}
3. Multiple Conditions (AND logic)
python
# Find action movies from 2020 or later
filter = {
    "genre": "action",
    "year": {"$gt": 2019}
}
4. Not Equal To
python
# Find all except horror movies
filter = {"genre": {"$ne": "horror"}}
5. In a List
python
# Find action or comedy movies
filter = {"genre": {"$in": ["action", "comedy"]}}
6. Range Filter
python
# Find movies between 2018 and 2020
filter = {
    "year": {"$gte": 2018, "$lte": 2020}
}
Query with Filter
python
from pinecone import Pinecone

# Initialize
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("datacamp-index")

# Filter: Only action movies from 2020 or later
filter = {
    "genre": "action",
    "year": {"$gt": 2019}
}

# Query with filter
results = index.query(
    vector=query_vector,
    top_k=5,
    filter=filter,
    include_metadata=True
)

# Display results
for match in results['matches']:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")
Updating Vectors
Why Update Vectors?
Reason	Benefit
Keep data current	New values, new metadata
Optimize performance	Remove unused vectors
Maintain data integrity	Fix outdated information
Clean up	Remove redundant data
Update Methods
1. Update Vector Values
python
# Update vector values by ID
index.update(
    id="vec_123",
    values=[0.1, 0.2, 0.3, ...]  # New embedding values
)
2. Update Metadata Only
python
# Update only metadata (values stay the same)
index.update(
    id="vec_123",
    set_metadata={
        "genre": "comedy",
        "rating": 5
    }
)
Important: Metadata updates are additive - existing metadata not mentioned stays the same!

3. Update Both Values and Metadata
python
# Update both values and metadata
index.update(
    id="vec_123",
    values=[0.1, 0.2, 0.3, ...],
    set_metadata={
        "genre": "comedy",
        "year": 2024,
        "rating": 5
    }
)
Update vs Fetch Example
python
# 1. Check current vector
current = index.fetch(ids=["vec_123"])
print("Before update:", current['vectors']['vec_123']['metadata'])

# 2. Update metadata
index.update(
    id="vec_123",
    set_metadata={
        "genre": "comedy",
        "rating": 4.5
    }
)

# 3. Verify update
updated = index.fetch(ids=["vec_123"])
print("After update:", updated['vectors']['vec_123']['metadata'])
Deleting Vectors
Delete Methods
1. Delete by ID
python
# Delete a single vector
index.delete(ids=["vec_123"])

# Delete multiple vectors
index.delete(ids=["vec_123", "vec_456", "vec_789"])
2. Delete by Metadata Filter
python
# Delete all vectors with genre = "action"
index.delete(filter={"genre": "action"})
3. Delete All from Namespace
python
# ⚠️ CAREFUL: Deletes EVERYTHING in the namespace!
index.delete(delete_all=True, namespace="electronics")
Complete Delete Example
python
from pinecone import Pinecone

# Initialize and connect
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("datacamp-index")

# Check before deletion
print("Before:", index.describe_index_stats())

# Delete vectors with IDs "3" and "4"
index.delete(ids=["3", "4"])

# Check after deletion
print("After:", index.describe_index_stats())
Delete Methods Comparison
Method	Code	Use Case
Delete by ID	index.delete(ids=["id1", "id2"])	Remove specific vectors
Delete by Filter	index.delete(filter={"genre": "action"})	Remove groups by metadata
Delete All	index.delete(delete_all=True, namespace="name")	Clear a namespace
Batching Upserts
Why Batch Upserts?
Problem	Solution
Rate limits	Send in batches
Size limits	Break into smaller chunks
Slow uploads	Parallel processing
API restrictions	Work within limits
Chunking Function
python
import itertools

def chunks(iterable, batch_size=100):
    """Break a list into smaller chunks"""
    iterator = iter(iterable)
    chunk = tuple(itertools.islice(iterator, batch_size))
    
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(iterator, batch_size))
Sequential Batching (Slow but Simple)
python
# Upsert vectors in batches of 100
for batch in chunks(vectors, batch_size=100):
    index.upsert(vectors=batch)
    print(f"Upserted batch of {len(batch)} vectors")
Parallel Batching (Faster!)
python
import itertools
from pinecone import Pinecone

# Initialize with pool_threads for parallel requests
pc = Pinecone(
    api_key="YOUR_API_KEY",
    pool_threads=5  # Max simultaneous requests
)

# Connect to index with pool_threads
index = pc.Index("datacamp-index")

# Parallel upsert (async)
async_results = [
    index.upsert(vectors=batch, async_req=True)
    for batch in chunks(vectors, batch_size=100)
]

# Wait for all to complete
for result in async_results:
    result.get()

print("All batches upserted successfully!")
Batching Comparison
Method	Speed	Complexity	When to Use
Sequential	Slow	Simple	Small datasets (<1000 vectors)
Parallel	Fast	Moderate	Large datasets (>10K vectors)
Batch Size Guidelines
Dataset Size	Method	Batch Size
< 1,000	Sequential	100
1,000 - 10,000	Sequential	200-500
10,000 - 100,000	Parallel	500-1000
> 100,000	Parallel	1000
Code Snippets
Complete Setup and Query with Filter
python
from pinecone import Pinecone

# 1. Initialize
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("datacamp-index")

# 2. Query with filter
results = index.query(
    vector=query_vector,
    top_k=3,
    filter={
        "genre": "action",
        "year": {"$gt": 2019}
    },
    include_metadata=True
)

# 3. Display results
for match in results['matches']:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")
Complete Update and Delete Example
python
# 1. Update metadata
index.update(
    id="7",
    set_metadata={
        "genre": "thriller",
        "year": 2024
    }
)

# 2. Fetch to verify
fetched = index.fetch(ids=["7"])
print(fetched['vectors']['7']['metadata'])

# 3. Delete vectors
index.delete(ids=["3", "4"])

# 4. Verify deletion
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
Complete Batching Example
python
import itertools
from pinecone import Pinecone

# Chunking function
def chunks(iterable, batch_size=100):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

# Initialize
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("datacamp-index")

# Sequential batching
for batch in chunks(vectors, batch_size=100):
    index.upsert(vectors=batch)
    print(f"Uploaded {len(batch)} vectors")

# Check result
print(index.describe_index_stats())
Common Errors & Fixes
Error	Cause	Solution
Filter error	Wrong filter syntax	Use correct operators ($gt, $lt, etc.)
KeyError: 'genre'	Metadata field doesn't exist	Check metadata field names
Dimension mismatch	Wrong vector length	Match index dimension
Rate limit exceeded	Too many requests	Use batching
Index not found	Wrong index name	Check index name
Filter Syntax Common Mistakes
python
# ❌ Wrong: Using string comparison
filter = {"year": "> 2019"}

# ✅ Correct: Using operator
filter = {"year": {"$gt": 2019}}

# ❌ Wrong: Missing operator
filter = {"year": 2024}  # Works for equality only

# ✅ Correct: Explicit equality
filter = {"year": {"$eq": 2024}}
Update Common Mistakes
python
# ❌ Wrong: Missing ID
index.update(values=[0.1, 0.2, ...])

# ✅ Correct: Include ID
index.update(id="vec_123", values=[0.1, 0.2, ...])

# ❌ Wrong: Wrong dimension
index.update(id="vec_123", values=[0.1, 0.2])  # Too short!

# ✅ Correct: Match dimension
index.update(id="vec_123", values=[0.1, 0.2, ..., 0.3])  # 1536 numbers
Delete Common Mistakes
python
# ❌ Wrong: Empty filter
index.delete(filter={})  # Deletes everything!

# ✅ Correct: Specific filter
index.delete(filter={"genre": "action"})

# ❌ Wrong: Delete all without namespace
index.delete(delete_all=True)  # Will error!

# ✅ Correct: Specify namespace
index.delete(delete_all=True, namespace="electronics")
Quick Reference
Metadata Operators
Operator	Use Case	Example
$eq	Equal to	{"genre": {"$eq": "action"}}
$ne	Not equal to	{"genre": {"$ne": "comedy"}}
$gt	Greater than	{"year": {"$gt": 2019}}
$gte	Greater than or equal	{"year": {"$gte": 2020}}
$lt	Less than	{"year": {"$lt": 2020}}
$lte	Less than or equal	{"year": {"$lte": 2020}}
$in	In a list	{"genre": {"$in": ["action", "drama"]}}
Update Methods
Operation	Code	Purpose
Update Values	index.update(id, values=...)	Change vector embedding
Update Metadata	index.update(id, set_metadata=...)	Change metadata only
Update Both	index.update(id, values=..., set_metadata=...)	Change everything
Delete Methods
Operation	Code	Purpose
Delete by ID	index.delete(ids=[...])	Remove specific vectors
Delete by Filter	index.delete(filter={...})	Remove groups by metadata
Delete All	index.delete(delete_all=True, namespace=...)	Clear a namespace
Batching Methods
Operation	Code	Purpose
Chunk	chunks(iterable, batch_size)	Split into batches
Sequential	for chunk in chunks(...): index.upsert(chunk)	Batch one at a time
Parallel	async_results = [index.upsert(batch, async_req=True) for batch in chunks(...)]	Batch simultaneously
Best Practices
1. Always Verify After Update
python
# Update
index.update(id="7", set_metadata={"genre": "thriller"})

# Verify
fetched = index.fetch(ids=["7"])
print(fetched['vectors']['7']['metadata'])  # Check it worked
2. Check Before Delete
python
# Check what you're deleting first
fetched = index.fetch(ids=["3", "4"])
print(fetched)

# Then delete
index.delete(ids=["3", "4"])
3. Use include_metadata in Queries
python
# Always include metadata to verify filters
query_result = index.query(
    vector=query_vector,
    top_k=3,
    filter={"genre": "action"},
    include_metadata=True  # ← Important!
)
4. Batch Large Uploads
python
# Don't upload 10,000 vectors at once!
# Use batching instead
for batch in chunks(vectors, batch_size=100):
    index.upsert(vectors=batch)
5. Use Namespaces for Organization
python
# Organize by category
index.upsert(vectors=electronics, namespace="electronics")
index.upsert(vectors=clothing, namespace="clothing")

# Query only specific namespace
results = index.query(
    vector=query_vector,
    namespace="electronics",
    top_k=5
)
Summary
What You Learned Today:
✅ Metadata Filtering - Search within specific categories

✅ Update Vectors - Change values and metadata

✅ Delete Vectors - Remove by ID, filter, or namespace

✅ Batching Upserts - Upload large datasets efficiently

Key Takeaways:
Metadata filtering makes queries FASTER and MORE RELEVANT!

Updates keep your data FRESH and ACCURATE!

Deletes OPTIMIZE performance and CLEAN UP clutter!

Batching makes upserts RELIABLE and EFFICIENT!

Additional Resources
Pinecone Metadata Filtering Docs

Pinecone Update Data Docs

Pinecone Delete Data Docs

Pinecone Quotas and Limits

"Good data practices = Good AI applications!" 🚀

Happy Building! 💻✨

text

---

## How to Add to Your notes.md:

1. **Copy the entire content above**
2. **Paste it into your `notes.md` file**
3. **Save and push to GitHub:**

```bash
git add notes.md
git commit -m "Add Day 13: Advanced Pinecone Operations documentation"
git push origin main
Short Thread Post for Day 13:
text
Day 13
Advanced Pinecone Operations ⚡

Covered:
• Metadata filtering ($gt, $lt, $in, $ne)
• Updating vectors (values & metadata)
• Deleting vectors (by ID, filter, all)
• Batching upserts (sequential & parallel)

Built:
• Filtered semantic search
• Vector update pipeline
• Batch ingestion system

Big lesson:
Filter first → search faster.
Update → keep data fresh.
Delete → optimize performance.
Batch → handle large datasets.

Day 14 loading 🚀