# Start coding here
# Use as many cells as you need
# ========================================================
# PROJECT: Women's Clothing E-Commerce Reviews Analysis
# ========================================================

# STEP 1: Import Libraries
import pandas as pd
import numpy as np
from openai import OpenAI
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from scipy.spatial import distance
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# STEP 2: Load the dataset
reviews = pd.read_csv("womens_clothing_e-commerce_reviews.csv")
reviews.head()

# STEP 3: Clean the data (drop rows with missing Review Text)
reviews_clean = reviews.dropna(subset=['Review Text']).reset_index(drop=True)
review_texts = reviews_clean['Review Text'].tolist()

# ========================================================
# TASK 1: Create and store the embeddings
# ========================================================

# Initialize OpenAI client
client = OpenAI()

# Function to create embeddings
def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]

# Create embeddings for all reviews
embeddings = create_embeddings(review_texts)

print(f"✅ Created {len(embeddings)} embeddings")
print(f"✅ Each embedding has {len(embeddings[0])} dimensions")


# ========================================================
# TASK 2: Dimensionality reduction & visualization
# ========================================================

# Apply t-SNE to reduce to 2D
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
embeddings_2d = tsne.fit_transform(np.array(embeddings))

print(f"✅ Reduced embeddings shape: {embeddings_2d.shape}")

# Plot 2D visualization (colored by rating)
plt.figure(figsize=(12, 8))
ratings = reviews_clean['Rating'].values
scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
                     c=ratings, cmap='RdYlGn', alpha=0.6, s=50)
plt.colorbar(scatter, label='Rating')
plt.title('2D Visualization of Customer Reviews (Colored by Rating)')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.show()


# ========================================================
# TASK 3: Feedback categorization
# ========================================================

topics = ['quality', 'fit', 'style', 'comfort', 'color', 'size', 'material']

def categorize_reviews(review_texts, embeddings, topic_keywords):
    """Categorize reviews by topic using semantic similarity"""
    
    # Create embeddings for topic keywords
    topic_embeddings = create_embeddings(topic_keywords)
    
    results = {}
    
    for topic, topic_emb in zip(topic_keywords, topic_embeddings):
        # Calculate cosine distances to each review
        distances = []
        for i, rev_emb in enumerate(embeddings):
            dist = distance.cosine(topic_emb, rev_emb)
            distances.append((i, dist))
        
        # Sort by distance (closest first)
        distances.sort(key=lambda x: x[1])
        
        # Get top 3 reviews for this topic
        top_indices = [idx for idx, _ in distances[:3]]
        results[topic] = [review_texts[idx] for idx in top_indices]
    
    return results

# Categorize the reviews
categorized_reviews = categorize_reviews(review_texts, embeddings, topics)

# Display results
for topic, reviews_list in categorized_reviews.items():
    print(f"\n--- Reviews about '{topic}' ---")
    for i, review in enumerate(reviews_list, 1):
        print(f"{i}. {review[:120]}...")

def find_similar_reviews(input_review, review_texts, embeddings, n=3):
    """
    Find the n most similar reviews to a given input review
    (includes the input review itself as the closest match)
    """
    # Create embedding for the input review
    input_embedding = create_embeddings([input_review])[0]
    
    # Calculate distances to all reviews
    distances = []
    for i, emb in enumerate(embeddings):
        dist = distance.cosine(input_embedding, emb)
        distances.append((i, dist))
    
    # Sort by distance (closest first)
    distances.sort(key=lambda x: x[1])
    
    # Get the n closest reviews (including the input itself)
    similar_indices = [idx for idx, _ in distances[:n]]
    
    return [review_texts[idx] for idx in similar_indices]

# Apply to the first review
first_review = "Absolutely wonderful - silky and sexy and comfortable"
most_similar_reviews = find_similar_reviews(first_review, review_texts, embeddings, n=3)

print("\n" + "="*60)
print("SIMILARITY SEARCH RESULTS")
print("="*60)
print(f"\n📝 Input Review: {first_review}\n")
print("🔍 Most Similar Reviews:")
for i, review in enumerate(most_similar_reviews, 1):
    print(f"\n{i}. {review}")