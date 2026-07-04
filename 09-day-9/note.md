📘 AI Engineering - Day 9: Embeddings Documentation
📌 Table of Contents
What are Embeddings?

Creating Embeddings with OpenAI API

Working with Embeddings

Dimensionality Reduction with t-SNE

Text Similarity with Cosine Distance

Practical Applications

Key Vocabulary

Common Pitfalls & Best Practices

📚 What are Embeddings?
Definition
Embeddings are numerical representations of text (words, phrases, or entire documents) in a multi-dimensional vector space. They capture the semantic meaning of text, allowing computers to understand relationships between words and concepts.

Key Properties
Dimensions: OpenAI embeddings always output 1536 numbers (dimensions) per text input

Semantic Meaning: Similar texts are mapped closer together in the vector space

Fixed Size: Every text, regardless of length, produces exactly 1536 numbers

Universal: The same model works for any language or domain

The Core Concept
Think of embeddings like GPS coordinates for meaning:

Each text gets a unique "location" in meaning space

Similar texts have similar coordinates

The model can "find" meaning by calculating distances between coordinates

How Meaning is Preserved
The numbers themselves don't tell humans what they mean

Only the model understands the patterns in the numbers

The COMBINATION of all 1536 numbers creates the meaning

Similar texts produce similar number patterns

The AI Communication Cycle
text
User Question (Text) → AI → Answer (Text)
         ↓                         ↑
    [Convert to Numbers]    [Convert to Text]
         ↓                         ↑
    Embedding (Numbers) ←→ Model Processing (Numbers)
🚀 Creating Embeddings with OpenAI API
Basic Setup
python
from openai import OpenAI

# Initialize client
client = OpenAI(api_key="your-api-key")

# Create embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)

# Convert to dictionary
response_dict = response.model_dump()

# Extract embedding
embedding = response_dict['data'][0]['embedding']
Response Structure
The API response is a nested dictionary:

python
response_dict = {
    'data': [
        {
            'embedding': [0.001, -0.002, 0.003, ...],  # 1536 numbers
            'index': 0
        }
    ],
    'model': 'text-embedding-3-small',
    'usage': {
        'prompt_tokens': 5,
        'total_tokens': 5
    }
}
Single Input vs Multiple Inputs
Single Text:

python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello, I am learning about embeddings!"
)
response_dict = response.model_dump()
embedding = response_dict['data'][0]['embedding']
Multiple Texts (Batching):

python
# ✅ Efficient: Embed multiple texts at once
texts = ["Text 1", "Text 2", "Text 3"]
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts  # List of strings
)
response_dict = response.model_dump()

# Extract all embeddings
for i in range(len(texts)):
    embedding = response_dict['data'][i]['embedding']
Why Batching Matters:

✅ Fewer API calls = faster processing

✅ More cost-effective

✅ Better for large datasets

✅ Still returns one embedding per input

Extracting Information from Response
python
# Extract total tokens used
total_tokens = response_dict['usage']['total_tokens']

# Extract the actual embedding vector (1536 numbers)
embedding = response_dict['data'][0]['embedding']

# Check embedding length
embedding_length = len(embedding)  # Always 1536
Custom Embedding Function
python
def create_embeddings(text, model="text-embedding-3-small"):
    """
    Create embeddings for text (string or list of strings)
    
    Args:
        text: String or list of strings to embed
        model: OpenAI embedding model name
    
    Returns:
        List of embeddings (or single embedding for single input)
    """
    response = client.embeddings.create(
        model=model,
        input=text
    )
    response_dict = response.model_dump()
    embeddings = [data['embedding'] for data in response_dict['data']]
    
    # Return single embedding or list
    if len(embeddings) == 1:
        return embeddings[0]
    return embeddings
💾 Working with Embeddings
Storing Embeddings in Data Structures
When working with embeddings, you typically store them alongside your original data:

python
# Example: Products with embeddings
products = [
    {
        "title": "Smartphone X1",
        "short_description": "Latest flagship smartphone with AI features",
        "category": "Electronics",
        "price": 799.99,
        "embedding": [0.001, -0.002, ...]  # 1536 numbers
    },
    # ... more products
]
Extracting Data with List Comprehensions
List comprehensions provide a clean way to extract specific fields:

python
# Extract categories
categories = [product['category'] for product in products]

# Extract embeddings
embeddings = [product['embedding'] for product in products]
Looping with Enumerate
When you need both index and value:

python
# Add embeddings to existing data
for i, product in enumerate(products):
    product['embedding'] = response_dict['data'][i]['embedding']
Checking Token Usage
Always monitor token usage to manage costs:

python
# Extract token usage
total_tokens = response_dict['usage']['total_tokens']
prompt_tokens = response_dict['usage']['prompt_tokens']

print(f"Total tokens used: {total_tokens}")
print(f"Prompt tokens: {prompt_tokens}")
📊 Dimensionality Reduction with t-SNE
Why t-SNE?
Problem: 1536 dimensions is impossible to visualize

Solution: Reduce to 2D or 3D for visualization

Purpose: Understand patterns and clusters in your data

Caveat: Some information is lost in the transformation

What is t-SNE?
t-SNE = t-distributed Stochastic Neighbor Embedding

It's a technique that:

Preserves local structure (similar items stay close)

Reveals clusters and patterns

Makes high-dimensional data visualizable

Should be used cautiously (information loss occurs)

Basic t-SNE Implementation
python
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Prepare data
embeddings = [product['embedding'] for product in products]
embeddings_array = np.array(embeddings)  # Shape: (n, 1536)

# Apply t-SNE
tsne = TSNE(
    n_components=2,      # Reduce to 2 dimensions
    perplexity=5,        # Must be < number of data points
    random_state=42      # For reproducible results
)
embeddings_2d = tsne.fit_transform(embeddings_array)  # Shape: (n, 2)
Understanding t-SNE Parameters
Parameter	Description	Typical Value
n_components	Target dimensions (2 or 3)	2
perplexity	Balance local/global structure	5-50 (must be < n_samples)
learning_rate	Speed of learning	200 (default)
n_iter	Number of iterations	1000 (default)
random_state	For reproducible results	42
Important: perplexity must always be less than the number of data points!

Visualizing Embeddings
Simple Scatter Plot:

python
# Create scatter plot
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])

# Add annotations
for i, product in enumerate(products):
    plt.annotate(
        product['category'],
        (embeddings_2d[i, 0], embeddings_2d[i, 1])
    )

plt.title('Product Embeddings Visualized with t-SNE')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.show()
Color-Coded by Category:

python
# Color by category
unique_categories = list(set(categories))
color_map = {
    'Electronics': 'blue',
    'Sports': 'red',
    'Home & Kitchen': 'green'
}

for category in unique_categories:
    indices = [i for i, c in enumerate(categories) if c == category]
    plt.scatter(
        embeddings_2d[indices, 0],
        embeddings_2d[indices, 1],
        label=category,
        color=color_map.get(category, 'gray'),
        s=100
    )

plt.legend()
plt.title('Product Categories Visualized with t-SNE')
plt.show()
Interpreting t-SNE Results
Clusters: Similar items group together

Distance: Closer = more similar

Separation: Different categories should be separated

Patterns: Reveals natural groupings in your data

📐 Text Similarity with Cosine Distance
Understanding Cosine Distance
Cosine distance measures the similarity between two vectors based on the angle between them.

The Distance Scale
0.0 = Very similar (same direction)

1.0 = Unrelated (perpendicular)

2.0 = Very different (opposite direction)

Basic Implementation
python
from scipy.spatial import distance

# Measure similarity between two embeddings
similarity = distance.cosine(embedding1, embedding2)

# Smaller number = more similar
Finding the Most Similar Item
python
from scipy.spatial import distance
import numpy as np

# User query
query_text = "computer"
query_embedding = create_embeddings(query_text)

# Calculate distances to all articles
distances = []
for article in articles:
    dist = distance.cosine(query_embedding, article['embedding'])
    distances.append(dist)

# Find the most similar article
min_index = np.argmin(distances)  # Index of smallest distance
most_similar = articles[min_index]

print(f"Most similar: {most_similar['headline']}")
print(f"Distance: {distances[min_index]:.4f}")
Finding Top N Most Similar Items
python
# Get top 3 most similar
top_indices = np.argsort(distances)[:3]

print("Top 3 most similar:")
for i, idx in enumerate(top_indices, 1):
    print(f"{i}. {articles[idx]['headline']} (distance: {distances[idx]:.4f})")
Complete Similarity Search Function
python
def semantic_search(query, articles, top_n=3):
    """
    Find most semantically similar articles to a query
    
    Args:
        query: Text query string
        articles: List of articles with embeddings
        top_n: Number of results to return
    
    Returns:
        List of top_n most similar articles with distances
    """
    # Embed query
    query_embedding = create_embeddings(query)
    
    # Calculate distances
    distances = []
    for article in articles:
        dist = distance.cosine(query_embedding, article['embedding'])
        distances.append(dist)
    
    # Get top N
    top_indices = np.argsort(distances)[:top_n]
    
    results = []
    for idx in top_indices:
        results.append({
            'article': articles[idx],
            'distance': distances[idx]
        })
    
    return results

# Usage
results = semantic_search("AI technology", articles, top_n=3)
for result in results:
    print(f"• {result['article']['headline']} (dist: {result['distance']:.4f})")
🎯 Practical Applications
1. Semantic Search Engine
Traditional search uses keywords; semantic search uses meaning.

How it works:

Embed all documents and store in database

For each search query, embed the query

Calculate cosine distance to all documents

Return documents with smallest distances

Advantages:

Understands synonyms (e.g., "comfortable" = "soft")

Understands paraphrasing (e.g., "directions to shop" = "way to supermarket")

Returns relevant results even without matching keywords

2. Recommendation Systems
Recommends items based on semantic similarity.

How it works:

Embed all items in your catalog

Find what user likes (viewed, purchased, etc.)

Recommend items with most similar embeddings

Example:

User views "Smartphone X1" → Recommend phones with similar descriptions

Works even if product titles vary (e.g., "iPhone" vs "Galaxy")

3. Classification
Assigns labels based on semantic similarity.

How it works:

Define categories with example texts

Embed new text to classify

Find which category embedding is closest

Examples:

News article classification (politics, sports, tech)

Sentiment analysis (positive, negative, neutral)

Spam detection (spam vs not spam)

4. Clustering
Groups similar items automatically.

How it works:

Embed all items

Use clustering algorithms (like K-Means)

Items in same cluster share similar meaning

Benefits:

Discovers patterns automatically

Groups similar products/categories

Identifies outliers and anomalies

📖 Key Vocabulary
Term	Definition
Embedding	Numerical representation of text (1536 numbers)
Vector Space	Multi-dimensional space where embeddings reside
Semantic Meaning	The context and intent captured by embeddings
Cosine Distance	Measure of similarity between vectors (0-2, smaller = more similar)
t-SNE	t-distributed Stochastic Neighbor Embedding (dimensionality reduction for visualization)
Perplexity	t-SNE parameter balancing local/global structure (must be < n_samples)
Batching	Processing multiple inputs in one API call (more efficient)
Semantic Search	Search based on meaning, not keywords
Dimensionality Reduction	Reducing high-dimensional data to 2D/3D for visualization
Vector Database	Database optimized for storing and searching embeddings
⚠️ Common Pitfalls & Best Practices
✅ DO's
1. Batch Your Embeddings

python
# ✅ Efficient: One API call for multiple texts
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=headlines  # List of strings
)
2. Set Random State for Reproducibility

python
# ✅ Always set random_state
tsne = TSNE(n_components=2, random_state=42)
3. Use argmin for Smallest Distance

python
# ✅ Correct
min_index = np.argmin(distances)
4. Check Token Usage for Cost Monitoring

python
# ✅ Monitor your usage
tokens = response_dict['usage']['total_tokens']
print(f"Tokens used: {tokens}")
5. Use List Comprehensions for Clean Code

python
# ✅ Clean and efficient
categories = [product['category'] for product in products]
embeddings = [product['embedding'] for product in products]
❌ DON'Ts
1. Don't Make Separate API Calls

python
# ❌ Slow and expensive
for text in texts:
    client.embeddings.create(input=text)
2. Don't Set Perplexity >= Number of Samples

python
# ❌ Will cause error
tsne = TSNE(perplexity=100)  # If n_samples < 100
3. Don't Forget to Convert to Numpy Array

python
# ❌ Won't work with t-SNE
tsne.fit_transform(embeddings)  # embeddings is a list

# ✅ Convert to numpy array first
tsne.fit_transform(np.array(embeddings))
4. Don't Assume Embeddings Are Human-Readable

python
# ❌ You can't read embeddings like text
print(embedding)  # [0.001, -0.002, ...] → Just numbers!

# ✅ Use them for calculations and comparisons
distance.cosine(embedding1, embedding2)  # This works!
🔍 Quick Reference
Embedding API Call Pattern
python
client.embeddings.create(
    model="text-embedding-3-small",
    input=text  # String or list of strings
)
t-SNE Pattern
python
TSNE(n_components=2, perplexity=5, random_state=42)
.fit_transform(np.array(embeddings))
Similarity Pattern
python
distance.cosine(query_embedding, article['embedding'])
Finding Most Similar
python
np.argmin(distances)  # Returns index of smallest value
np.argsort(distances)[:n]  # Returns indices of top N
📊 Summary
Embeddings are the foundation of modern NLP applications:

Convert text to meaningful numbers (1536 dimensions)

Enable semantic understanding beyond keywords

Power search, recommendations, classification, and more

Key Operations:

Create embeddings with OpenAI API (batch for efficiency)

Store embeddings alongside your data

Reduce dimensions with t-SNE for visualization

Compare embeddings with cosine distance

Search for semantic similarity

The Power of Embeddings:

Similar meanings = close together in vector space

Different meanings = far apart in vector space

Distance = measure of semantic similarity

