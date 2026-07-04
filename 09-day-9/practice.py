##############################################################################################################
# Create an OpenAI client
from openai import OpenAI


client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to obtain embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello, I am learning about embeddings!"
)

# Convert the response into a dictionary
response_dict = response.model_dump()
print(response_dict)

###############################################################################################################
# Extract the total_tokens from response_dict
print(response_dict['data'][0]['embedding'])

###############################################################################################################
# Extract a list of product short descriptions from products
products = [
    {"id": 1, "short_description": "This is a great product for your home."},
    {"id": 2, "short_description": "An innovative gadget that makes life easier."},
    {"id": 3, "short_description": "A stylish accessory for your wardrobe."}
]
product_descriptions = [product['short_description'] for product in products]

# Create embeddings for each product description
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=product_descriptions
)
response_dict = response.model_dump()

# Extract the embeddings from response_dict and store in products
for i, product in enumerate(products):
    product['embedding'] = response_dict['data'][i]['embedding']
    
print(products[0].items())

################################################################################################################
# Create reviews and embeddings lists using list comprehensions
categories = [product['category'] for product in products]
embeddings = [product['embedding'] for product in products]

# Reduce the number of embeddings dimensions to two using t-SNE
tsne = TSNE(n_components=2, perplexity=5)
embeddings_2d = tsne.fit_transform(np.array(embeddings))

# Create a scatter plot from embeddings_2d
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])

for i, category in enumerate(categories):
    plt.annotate(category, (embeddings_2d[i, 0], embeddings_2d[i, 1]))

plt.show()