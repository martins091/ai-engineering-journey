# Day 10: AI-Powered Applications - Complete Guide 🚀

## Table of Contents
1. [Semantic Search and Enriched Embeddings](#semantic-search-and-enriched-embeddings)
2. [Recommendation Systems](#recommendation-systems)
3. [Zero-Shot Classification](#zero-shot-classification)
4. [Vector Databases](#vector-databases)
5. [How AI Apps Work (Function Calling)](#how-ai-apps-work)
6. [Key Takeaways](#key-takeaways)
7. [Code Snippets](#code-snippets)

---

## Semantic Search and Enriched Embeddings

### What is Semantic Search?
Semantic search finds results based on **MEANING**, not just matching words.

**Example:**
- You search: "smartphone"
- It finds: "phone", "mobile device", "Galaxy" (even if "smartphone" isn't mentioned)
- Because they MEAN the same thing!

### The 3 Steps of Semantic Search:
1. **Embed** the search query and texts to compare against
2. **Compute** cosine distances between the embedded search query and other texts
3. **Extract** texts with the smallest cosine distance

### Enriched Embeddings
Instead of embedding just one feature (like title), combine MULTIPLE features:

**Features to combine:**
- Title
- Description
- Category
- Keywords/Features

### Creating Enriched Text with F-strings:
```python
def create_article_text(article):
    return f"""
    Headline: {article['headline']}
    Topic: {article['topic']}
    Keywords: {', '.join(article['keywords'])}
    """
Why Enriched Embeddings Work Better:
More information → Better meaning capture

Single feature = Limited understanding

Multiple features = Rich understanding

Recommendation Systems
How Recommendation Systems Work:
Recommendation systems work almost exactly like semantic search!

Steps:

Embed potential recommendations

Embed the data point(s) to base recommendations on

Calculate cosine distances

Recommend the closest items

Single Data Point Recommendation:
python
# User viewed one product
last_product_text = create_product_text(last_product)
last_product_embeddings = create_embeddings(last_product_text)[0]

# Compare to all products
hits = find_n_closest(last_product_embeddings, product_embeddings, n=3)

# Recommend top 3
for hit in hits:
    print(products[hit['index']]['title'])
Multiple Data Points (User History):
When a user has viewed multiple products:

Embed each product in user history

Take the MEAN (average) of all embeddings

Filter out already seen products

Recommend the closest unseen products

python
# Embed user history
history_texts = [create_product_text(article) for article in user_history]
history_embeddings = create_embeddings(history_texts)

# Take the mean (average)
mean_history_embeddings = np.mean(history_embeddings, axis=0)

# Filter out seen products
products_filtered = [product for product in products if product not in user_history]

# Find recommendations
hits = find_n_closest(mean_history_embeddings, product_embeddings, n=3)
Zero-Shot Classification
What is Zero-Shot Classification?
Classifying items without any training examples! Just use embeddings to compare.

Classification Workflow:
Step 1: Define Classes with Descriptions

python
# Simple labels (less accurate)
sentiments = [
    {'label': 'Positive'},
    {'label': 'Neutral'},
    {'label': 'Negative'}
]

# Detailed descriptions (more accurate)
sentiments = [
    {'label': 'Positive', 'description': 'A positive restaurant review'},
    {'label': 'Neutral', 'description': 'A neutral restaurant review'},
    {'label': 'Negative', 'description': 'A negative restaurant review'}
]
Step 2: Embed Everything

python
# Extract and embed descriptions
class_descriptions = [sentiment['description'] for sentiment in sentiments]
class_embeddings = create_embeddings(class_descriptions)

# Embed items to classify
review_embeddings = create_embeddings(reviews)
Step 3: Compare and Classify

python
def find_closest(query_vector, embeddings):
    distances = []
    for index, embedding in enumerate(embeddings):
        dist = distance.cosine(query_vector, embedding)
        distances.append({"distance": dist, "index": index})
    return min(distances, key=lambda x: x["distance"])

# Classify each review
for index, review in enumerate(reviews):
    closest = find_closest(review_embeddings[index], class_embeddings)
    label = sentiments[closest['index']]['label']
    print(f'"{review}" was classified as {label}')
Why Detailed Descriptions Work Better:
Approach	Result
"Positive" only	May misclassify (too broad)
"A positive restaurant review"	More accurate (specific context)
Vector Databases
Why We Need Vector Databases:
Old Way (In-Memory):

Store embeddings in RAM

Works for small datasets (<10,000)

Problems:

Each embedding = 13KB (1536 numbers × 4 bytes)

100,000 embeddings = 1.3GB RAM

Slow: checks EVERY document

New Way (Vector Database):

Store embeddings in specialized database

Works for large datasets (millions)

Benefits:

Fast similarity search

Uses smart indexing (ANN)

Can scale to millions

What's Stored in a Vector Database:
Embeddings: The actual vectors (numbers)

Source Text: Original content (for display)

Metadata: IDs, categories, prices, etc.

SQL vs NoSQL:
SQL (Relational)	NoSQL (Vector)
Tables with rows/columns	No tables, flexible structure
Good for structured data	Good for vectors/embeddings
Slow for similarity search	Fast for similarity search
Examples: MySQL, PostgreSQL	Examples: Chroma, Pinecone
Popular Vector Databases:
Database	Type	Best For
Chroma	Open-source	Quick setup, learning
Pinecone	Managed (Cloud)	Production, scalable
Weaviate	Open-source/Commercial	Feature-rich
Milvus	Open-source	Very large scale
Qdrant	Open-source/Commercial	Fast, reliable
Choosing a Vector Database:
Ask These Questions:

How much data? (Small → Chroma, Large → Milvus/Pinecone)

Managed or self-managed? (Managed = easy but costs money)

Open-source or commercial? (Free vs support/features)

What type of data? (Text only vs multi-modal)

What NOT to Store in Metadata:
❌ Large text documents
❌ Full article content
❌ Binary files

✅ Small IDs
✅ Category tags
✅ Timestamps
✅ Numeric filters

How AI Apps Work (Function Calling)
The Big Secret:
AI doesn't understand words - it matches numbers!
AI doesn't do actions - it tells the app to do them!

How Function Calling Works:
1. Developers Write Functions:

python
def refund_purchase(order_id):
    # Find order
    # Process refund
    # Send confirmation email
    return "Refund processed"
2. Developers Give AI Access:

python
ALLOWED_FUNCTIONS = [
    refund_purchase,
    send_email,
    send_money
]
3. User Makes Request:

text
User: "Refund my last purchase"
4. AI Recognizes Intent:

text
AI: "This is the refund_purchase() function"
AI: "I need: order_id"
5. AI Extracts Parameters:

text
order_id = "12345"
reason = "Customer request"
6. AI Calls the Function:

text
AI → App: "Execute refund_purchase(12345, 'Customer request')"
7. App Performs the Action:

text
App: ✅ Refund processed
App: ✅ Confirmation sent
App: "Refund successful!"
8. AI Tells the User:

text
AI: "Your refund has been processed! Money will be back in 3-5 days."
What AI CANNOT Do:
AI can ONLY call functions developers gave access to

AI cannot access data it's not allowed to

AI cannot perform actions not coded by developers

Real-World Examples:
App	User Request	Function Called
Uber	"Book a ride"	book_ride(destination, time)
Spotify	"Play happy music"	play_playlist(mood="happy")
Bank App	"Send $50 to Mom"	transfer_money(amount, recipient)
Calendar	"Schedule meeting at 3pm"	create_event(time, title)
Key Takeaways
1. Embeddings = Numbers That Capture Meaning
Words → Numbers (lists of 1536 floats)

Similar words → Similar numbers

Used for search, recommendations, classification

2. Semantic Search
Find by meaning, not just keywords

Three steps: Embed → Compare → Extract

3. Enriched Embeddings
Combine multiple features

Better than single-feature embeddings

Use F-strings to combine text

4. Recommendation Systems
Same as semantic search

Can use single item or user history

Take mean for multiple history items

Filter out seen items

5. Zero-Shot Classification
No training data needed

Embed class descriptions

Compare to find closest class

Detailed descriptions = better accuracy

6. Vector Databases
For storing millions of embeddings

Fast similarity search

Store: Embeddings + Text + Metadata

Choose based on scale and needs

7. Function Calling
How AI performs actions

Developers write functions

AI triggers them with parameters

App does the actual work

Code Snippets
1. Create Enriched Embeddings:
python
def create_product_text(product):
    return f"""Title: {product['title']}
Description: {product['short_description']}
Category: {product['category']}
Features: {'; '.join(product['features'])}"""

product_texts = [create_product_text(product) for product in products]
product_embeddings = create_embeddings(product_texts)
2. Find Closest Matches:
python
def find_n_closest(query_vector, embeddings, n=3):
    distances = []
    for index, embedding in enumerate(embeddings):
        dist = distance.cosine(query_vector, embedding)
        distances.append({"distance": dist, "index": index})
    distances_sorted = sorted(distances, key=lambda x: x["distance"])
    return distances_sorted[:n]

# Usage
query_text = "computer"
query_vector = create_embeddings(query_text)[0]
hits = find_n_closest(query_vector, product_embeddings, n=5)
3. Semantic Search:
python
# Embed search query
query_text = "AI"
query_vector = create_embeddings(query_text)[0]

# Find closest articles
hits = find_n_closest(query_vector, article_embeddings, n=3)

# Print results
for hit in hits:
    article = articles[hit['index']]
    print(article['headline'])
4. Recommendation with User History:
python
# Embed user history
history_texts = [create_product_text(item) for item in user_history]
history_embeddings = create_embeddings(history_texts)

# Calculate mean
mean_history = np.mean(history_embeddings, axis=0)

# Filter seen items
filtered_products = [p for p in products if p not in user_history]
filtered_texts = [create_product_text(p) for p in filtered_products]
filtered_embeddings = create_embeddings(filtered_texts)

# Get recommendations
hits = find_n_closest(mean_history, filtered_embeddings, n=3)
5. Zero-Shot Classification:
python
# Define classes with descriptions
sentiments = [
    {'label': 'Positive', 'description': 'A positive review'},
    {'label': 'Neutral', 'description': 'A neutral review'},
    {'label': 'Negative', 'description': 'A negative review'}
]

# Embed descriptions
class_descriptions = [s['description'] for s in sentiments]
class_embeddings = create_embeddings(class_descriptions)

# Embed items
review_embeddings = create_embeddings(reviews)

# Classify
def find_closest(query_vector, embeddings):
    distances = []
    for idx, emb in enumerate(embeddings):
        dist = distance.cosine(query_vector, emb)
        distances.append({"distance": dist, "index": idx})
    return min(distances, key=lambda x: x["distance"])

for idx, review in enumerate(reviews):
    closest = find_closest(review_embeddings[idx], class_embeddings)
    label = sentiments[closest['index']]['label']
    print(f'"{review}" → {label}')
6. Function Calling (Conceptual):
python
# Developer writes functions
def refund_purchase(order_id, reason):
    # Implementation
    return f"Refunded {order_id}"

def send_email(to, subject, body):
    # Implementation
    return f"Email sent to {to}"

# Developer gives AI access
FUNCTIONS = {
    "refund_purchase": {"function": refund_purchase, "description": "Refund an order"},
    "send_email": {"function": send_email, "description": "Send an email"}
}

# AI triggers functions
# User: "Refund my last order"
# AI: Calls refund_purchase(order_id="12345", reason="Customer request")
# App: Executes the function
# AI: "Your refund is complete!"
Quick Reference: Important Functions
Custom Functions We Created:
Function	Purpose	Returns
create_embeddings(texts)	Convert text to numbers	List of embeddings
create_product_text(product)	Combine product features	Enriched text string
create_article_text(article)	Combine article features	Enriched text string
find_n_closest(query, embeddings, n)	Find n closest matches	List of {distance, index}
find_closest(query, embeddings)	Find single closest match	{distance, index}
Key Libraries:
python
import numpy as np                    # For calculations
from scipy.spatial import distance    # For cosine distance
from openai import OpenAI             # For API access
Summary: How AI Apps Work (The Big Picture)
text
1. DATA → EMBEDDINGS
   Text → Numbers that capture meaning

2. NUMBERS → STORAGE
   Embedded in vector database for fast retrieval

3. QUERY → COMPARE
   User input → Embed → Find closest matches

4. MATCHES → RESULTS
   Return closest items to user

5. ACTIONS → FUNCTION CALLING
   AI triggers developer-written functions
   App performs actual actions

6. USER ← RESULT
   Return response or action confirmation
Final Thoughts 💭
You now understand:

✅ How AI understands text (embeddings)

✅ How to find similar items (cosine distance)

✅ How to build search engines (semantic search)

✅ How to build recommendation systems

✅ How to classify without training data (zero-shot)

✅ How to scale to millions (vector databases)

✅ How AI performs actions (function calling)

This is how ALL modern AI apps work! 🚀

"AI doesn't understand anything - it just matches numbers really well!"

