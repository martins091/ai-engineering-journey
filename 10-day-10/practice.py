
###############################################################################################################
# Define a function to combine the relevant features into a single string
products = [
    {
        "title": "Smart Home Hub",
        "short_description": "This is a great product for your home.",
        "category": "Home Automation",
        "features": ["Voice Control", "Remote Access", "Energy Monitoring"]
    },
    {
        "title": "Innovative Gadget",
        "short_description": "An innovative gadget that makes life easier.",
        "category": "Gadgets",
        "features": ["Portable", "Multi-functional", "User-friendly"]
    },
    {
        "title": "Stylish Accessory",
        "short_description": "A stylish accessory for your wardrobe.",
        "category": "Fashion",
        "features": ["Trendy Design", "Durable Material", "Comfortable Fit"]
    }       
]
def create_product_text(product):
  return f"""Title: {product['title']}
Description: {product['short_description']}
Category: {product['category']}
Features: {'; '.join(product['features'])}"""

# Combine the features for each product
product_texts = [create_product_text(product) for product in products]

# Create the embeddings from product_texts
product_embeddings = create_embeddings(product_texts)

#################################################################################################################
def find_n_closest(query_vector, embeddings, n=3):
  distances = []
  for index, embedding in enumerate(embeddings):
    # Calculate the cosine distance between the query vector and embedding
    dist = distance.cosine(query_vector, embedding)
    # Append the distance and index to distances
    distances.append({"distance": dist, "index": index})
  # Sort distances by the distance key
  distances_sorted = sorted(distances, key=lambda x: x['distance'])
  # Return the first n elements in distances_sorted
  return distances_sorted[:n]

###############################################################################################################
# Create the query vector from query_text

query_text = "computer"
query_vector = create_embeddings(query_text)[0]

# Find the five closest distances
hits = find_n_closest(query_vector, product_embeddings, n=5)

print(f'Search results for "{query_text}"')
for hit in hits:
  # Extract the product at each index in hits
  product = products[hit['index']]
  print(product["title"])

#######################################################################################################################################
# Combine the features for last_product and each product in products
last_product_text = create_product_text(last_product)
product_texts = [create_product_text(product) for product in products]

# Embed last_product_text and product_texts
last_product_embeddings = create_embeddings(last_product_text)[0]
product_embeddings = create_embeddings(product_texts)

# Find the three smallest cosine distances and their indexes
hits = find_n_closest(last_product_embeddings, product_embeddings, n=3)

for hit in hits:
  product = products[hit['index']]
  print(product['title'])

#######################################################################################################################
# Prepare and embed the user_history, and calculate the mean embeddings
history_texts = [create_product_text(article) for article in user_history]
history_embeddings = create_embeddings(history_texts)
mean_history_embeddings = np.mean(history_embeddings, axis=0)

# Filter products to remove any in user_history
products_filtered = [product for product in products if product not in user_history]

# Combine product features and embed the resulting texts
product_texts = [create_product_text(product) for product in products_filtered]
product_embeddings = create_embeddings(product_texts)

hits = find_n_closest(mean_history_embeddings, product_embeddings, n=3)

for hit in hits:
  product = products_filtered[hit['index']]
  print(product['title'])

########################################################################################################################
# Define a function to return the minimum distance and its index
def find_closest(query_vector, embeddings):
  distances = []
  for index, embedding in enumerate(embeddings):
    dist = distance.cosine(query_vector, embedding)
    distances.append({"distance": dist, "index": index})
  return min(distances, key=lambda x: x["distance"])

for index, review in enumerate(reviews):
  # Find the closest distance and its index using find_closest()
  closest = find_closest(review_embeddings[index], class_embeddings)
  # Subset sentiments using the index from closest
  label = sentiments[closest['index']]['label']
  print(f'"{review}" was classified as {label}')

  ##############################################################################################################
  # Extract and embed the descriptions from sentiments
class_descriptions = [sentiment['description'] for sentiment in sentiments]
class_embeddings = create_embeddings(class_descriptions)
review_embeddings = create_embeddings(reviews)

def find_closest(query_vector, embeddings):
  distances = []
  for index, embedding in enumerate(embeddings):
    dist = distance.cosine(query_vector, embedding)
    distances.append({"distance": dist, "index": index})
  return min(distances, key=lambda x: x["distance"])

for index, review in enumerate(reviews):
  closest = find_closest(review_embeddings[index], class_embeddings)
  label = sentiments[closest['index']]['label']
  print(f'"{review}" was classified as {label}')

