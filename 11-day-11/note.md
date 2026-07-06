📘 Day 11: Vector Databases with ChromaDB – Complete Notes
🧠 What We Covered Today
What is ChromaDB?

Installing and connecting to ChromaDB

Creating collections (tables)

Adding data (documents + embeddings)

Estimating embedding costs with tiktoken

Querying the database (semantic search)

Updating, upserting, and deleting data

Understanding query results

1. What is ChromaDB?
ChromaDB is an open-source vector database designed for AI applications. It stores embeddings and makes it easy to search by meaning (semantic search).

Two Flavors of ChromaDB:
Mode	Description	Best For
Local Mode	Everything runs inside Python	Development, prototyping
Client/Server Mode	Chroma runs as a separate server	Production systems
In this course, we use Local Mode.

2. Installing and Connecting
Install ChromaDB
bash
pip install chromadb
Connect to the Database
python
import chromadb

# Persistent client (saves data to disk)
client = chromadb.PersistentClient(path="./my_db")

# Or ephemeral (in-memory, for testing)
# client = chromadb.EphemeralClient()
3. Creating a Collection
A collection is like a table in SQL.

python
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# Create a collection
collection = client.create_collection(
    name="netflix_titles",
    embedding_function=OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key="<OPENAI_API_TOKEN>"
    )
)

# List all collections
print(client.list_collections())

# Get an existing collection
collection = client.get_collection(name="netflix_titles")
Key Points:

create_collection() creates a new collection

get_collection() retrieves an existing one

Always specify the same embedding function when retrieving

4. Adding Data to a Collection
python
# Add documents
collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=[
        "Title: Inception (Movie)\nDescription: A thief who steals corporate secrets...\nCategories: Sci-Fi, Thriller",
        "Title: The Notebook (Movie)\nDescription: A poor yet passionate young man...\nCategories: Romance, Drama",
        "Title: Stranger Things (TV Show)\nDescription: When a young boy disappears...\nCategories: Sci-Fi, Horror"
    ],
    metadatas=[
        {"year": 2010, "rating": 8.8},
        {"year": 2004, "rating": 7.8},
        {"year": 2016, "rating": 8.7}
    ]  # Optional
)

# Check size
print(f"Number of documents: {collection.count()}")

# View first 10 items
print(collection.peek())
Important:

Chroma auto-generates embeddings from the documents

You must provide your own ids (they don't auto-generate)

Metadata is optional but useful for filtering

5. Estimating Embedding Costs with tiktoken
Before embedding large datasets, estimate the cost!

python
import tiktoken

# Load token encoder for your model
enc = tiktoken.encoding_for_model("text-embedding-3-small")

# Calculate total tokens
documents = ["Text 1", "Text 2", "Text 3"]  # Your dataset
total_tokens = sum(len(enc.encode(text)) for text in documents)

# Cost calculation
cost_per_1k_tokens = 0.00002  # $0.00002 per 1K tokens for text-embedding-3-small
total_cost = (total_tokens / 1000) * cost_per_1k_tokens

print(f"Total tokens: {total_tokens}")
print(f"Estimated cost: ${total_cost:.6f}")
Why this matters: OpenAI charges per token. This helps you avoid surprise bills!

6. Querying the Collection (Semantic Search)
Basic Query
python
# Retrieve the collection (must use same embedding function!)
collection = client.get_collection(
    name="netflix_titles",
    embedding_function=OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key="<OPENAI_API_TOKEN>"
    )
)

# Search
results = collection.query(
    query_texts=["sci-fi action movie with mind-bending plot"],
    n_results=5  # Number of results to return
)
Understanding Query Results
The results come as a dictionary:

python
{
    'ids': [['id1', 'id2', 'id3', 'id4', 'id5']],
    'documents': [['doc1', 'doc2', 'doc3', 'doc4', 'doc5']],
    'metadatas': [[{...}, {...}, {...}, {...}, {...}]],
    'distances': [[0.12, 0.34, 0.56, 0.78, 0.89]],
    'embeddings': None  # Not returned by default
}
Why lists of lists? Because query_texts accepts multiple queries:

python
# Multiple queries
results = collection.query(
    query_texts=["sci-fi movie", "romantic comedy", "documentary"],
    n_results=3
)

# Access results for each query
first_query_docs = results['documents'][0]   # Results for "sci-fi movie"
second_query_docs = results['documents'][1]  # Results for "romantic comedy"
third_query_docs = results['documents'][2]   # Results for "documentary"
Accessing Results (Single Query):

python
# Get the first query's results
documents = results['documents'][0]
distances = results['distances'][0]
ids = results['ids'][0]

# Loop through results
for i, doc in enumerate(documents):
    print(f"Result {i+1}: {doc}")
    print(f"Similarity score: {1 - distances[i]:.4f}")
    print("---")
Key Points:

Smaller distance = more similar (0 = identical, 1 = completely different)

You can convert to similarity score: similarity = 1 - distance

Chroma auto-embeds your query text!

7. Updating Data in a Collection
Update (Existing IDs)
python
collection.update(
    ids=["doc1", "doc2"],
    documents=["Updated description for doc1", "Updated description for doc2"]
)
# Chroma auto-generates new embeddings
Upsert (Update or Insert)
python
# If IDs exist → update them
# If IDs don't exist → add them
collection.upsert(
    ids=["doc1", "doc3"],
    documents=["Updated doc1", "New doc3"]
)
Difference:

update() → Only works if IDs already exist

upsert() → Works whether IDs exist or not

8. Deleting Data
Delete Specific Documents
python
collection.delete(ids=["doc1", "doc2"])
Delete All Documents in a Collection
python
all_ids = collection.get()['ids']
collection.delete(ids=all_ids)
Reset the Entire Database
python
# ⚠️ This deletes ALL collections and ALL data!
client.reset()
Warning: reset() is permanent. Use with caution!

9. Complete Workflow Example
python
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# 1. Connect to database
client = chromadb.PersistentClient(path="./netflix_db")

# 2. Create or get collection
collection = client.get_or_create_collection(
    name="netflix_titles",
    embedding_function=OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key="<OPENAI_API_TOKEN>"
    )
)

# 3. Add documents
collection.add(
    ids=["movie_1", "movie_2", "movie_3"],
    documents=[
        "Inception: A thief who steals corporate secrets through dream-sharing technology.",
        "The Notebook: A poor young man falls for a rich young woman in 1940s South Carolina.",
        "Stranger Things: A group of kids uncover supernatural mysteries in their small town."
    ]
)

# 4. Query
results = collection.query(
    query_texts=["mind-bending dream thriller"],
    n_results=2
)

# 5. Display results
print("Top recommendations:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")
    print(f"   Similarity: {1 - results['distances'][0][i]:.4f}\n")

# 6. Update a document
collection.update(
    ids=["movie_1"],
    documents=["Inception: Updated description about dreams within dreams."]
)

# 7. Delete a document
collection.delete(ids=["movie_2"])

# 8. Check size
print(f"Total documents: {collection.count()}")
10. Quick Reference Table
Operation	Method	Notes
Connect	chromadb.PersistentClient(path)	Saves data to disk
Create Collection	client.create_collection(name, embedding_function)	Create new "table"
Get Collection	client.get_collection(name, embedding_function)	Retrieve existing "table"
Get or Create	client.get_or_create_collection(...)	Creates if doesn't exist
List Collections	client.list_collections()	Show all collections
Add Documents	collection.add(ids, documents, metadatas)	Add data, auto-embed
Count Documents	collection.count()	Number of documents
Peek	collection.peek()	First 10 documents
Query	collection.query(query_texts, n_results)	Semantic search
Update	collection.update(ids, documents)	Update existing docs
Upsert	collection.upsert(ids, documents)	Update or insert
Delete	collection.delete(ids)	Remove documents
Reset	client.reset()	⚠️ Delete EVERYTHING


11. Key Takeaways
text
✅ Collection = Table (SQL)
✅ Document = Row
✅ Chroma auto-embeds documents when you add them
✅ Chroma auto-embeds queries when you search
✅ Always use the same embedding function when retrieving a collection
✅ Query results are dictionaries with lists of lists
✅ Smaller distance = more similar
✅ n_results controls how many results you get
✅ ids are required (not auto-generated)
✅ update() → only for existing IDs
✅ upsert() → works for new OR existing IDs
✅ reset() → deletes all data (use carefully!)
✅ Use tiktoken to estimate embedding costs


🎯 Summary in One Sentence
ChromaDB is a vector database that stores embeddings, auto-embeds your data and queries, and lets you search, update, and delete using semantic meaning.





PHASE 1: SETUP (Building the Knowledge Base)
This happens before any customer asks a question.

##################################################################################
Step 1: Gather Your Data
You have product information, support documents, FAQs, etc.

Example:

text
"iPhone 15 has USB-C charging port."
"iPhone 15 costs $799 for 128GB."
"iPhone 15 comes in Black, Blue, and Pink."




###################################################################################
=>. summary of how ai apps works
Step 2: Chunk the Data
Break long documents into small, focused pieces.

Example Chunks:

text
Chunk 1: "iPhone 15 has USB-C charging port."
Chunk 2: "iPhone 15 costs $799 for 128GB."
Chunk 3: "iPhone 15 comes in Black, Blue, and Pink."



#######################################################################################
Step 3: Convert Each Chunk to Numbers (Embeddings)
You send each chunk to the Embedding Model (like text-embedding-3-small).

text
Chunk 1: "iPhone 15 has USB-C" → [0.12, 0.45, 0.78, ...]
Chunk 2: "iPhone 15 costs $799" → [0.34, 0.78, 0.12, ...]
Chunk 3: "iPhone 15 comes in Black" → [0.56, 0.21, 0.67, ...]



#######################################################################################
Step 4: Store in Vector Database
You store BOTH the text and the embedding together.

text
Vector DB:
┌──────────────────────────────────────────────────────┐
│ text: "iPhone 15 has USB-C"                        │
│ embedding: [0.12, 0.45, 0.78, 0.33, ...]          │
├──────────────────────────────────────────────────────┤
│ text: "iPhone 15 costs $799"                       │
│ embedding: [0.34, 0.78, 0.12, 0.56, ...]          │
├──────────────────────────────────────────────────────┤
│ text: "iPhone 15 comes in Black, Blue, Pink"       │
│ embedding: [0.56, 0.21, 0.67, 0.44, ...]          │
└──────────────────────────────────────────────────────┘
Now your system is ready!

PHASE 2: LIVE QUERY (Customer Interaction)


########################################################################################
Step 5: Customer Asks a Question
text
Customer: "Does the iPhone 15 have USB-C?"


#######################################################################################
Step 6: Convert Question to Numbers
You send the question to the Embedding Model.

text
"Does the iPhone 15 have USB-C?" → [0.14, 0.46, 0.77, 0.31, ...]


########################################################################################
Step 7: Search Vector Database
You send these numbers to the Vector DB and ask:

"Find the closest matching embeddings!"

text
Vector DB compares:
Question:  [0.14, 0.46, 0.77, 0.31, ...]

Chunk 1:   [0.12, 0.45, 0.78, 0.33, ...] → Distance: 0.05 ✅ CLOSEST!
Chunk 2:   [0.34, 0.78, 0.12, 0.56, ...] → Distance: 0.45 
Chunk 3:   [0.56, 0.21, 0.67, 0.44, ...] → Distance: 0.85


#######################################################################################
Step 8: Vector DB Returns the Context (as Words!)
text
Vector DB returns:
"iPhone 15 has USB-C charging port."  ← Words!


#######################################################################################
Step 9: Prepare the Prompt for Generation Model
You combine the context and the question into a prompt.

text
Prompt:
Context: "iPhone 15 has USB-C charging port."
Question: "Does the iPhone 15 have USB-C?"


######################################################################################
Step 10: Send to Generation Model
You send this prompt to the Generation Model (like gpt-4o-mini).

text
Generation Model Input (Words):
"Context: iPhone 15 has USB-C charging port.
Question: Does the iPhone 15 have USB-C?"


#######################################################################################
Step 11: Generation Model Auto-Completes
The Generation Model predicts the next words one by one.

text
Word 1: "Yes" (95% probability)
Word 2: "iPhone" (90% probability)
Word 3: "15" (90% probability)
Word 4: "has" (95% probability)
Word 5: "USB-C" (99% probability)


#######################################################################################
Step 12: Generation Model Outputs the Answer (as Words!)
text
"Yes, iPhone 15 has USB-C."


######################################################################################
Step 13: You Return the Answer to the Customer
text
Answer: "Yes, iPhone 15 has USB-C." ✅