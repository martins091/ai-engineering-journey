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
# Define a create_embeddings function
short_description = "This is a great product for your home."
list_of_descriptions = [
    "This is a great product for your home.",
    "An innovative gadget that makes life easier.",
    "A stylish accessory for your wardrobe."
]
def create_embeddings(texts):
  response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
  )
  response_dict = response.model_dump()
  
  return [data['embedding'] for data in response_dict['data']]

# Embed short_description and print
print(create_embeddings(short_description)[0])

# Embed list_of_descriptions and print
print(create_embeddings(list_of_descriptions))

################################################################################################################
# Embed the search text
products = [
    {
        "short_description": "This is a great product for your home.",
        "embedding": create_embeddings("This is a great product for your home.")[0]
    },
    {
        "short_description": "An innovative gadget that makes life easier.",
        "embedding": create_embeddings("An innovative gadget that makes life easier.")[0]
    },
    {
        "short_description": "A stylish accessory for your wardrobe.",
        "embedding": create_embeddings("A stylish accessory for your wardrobe.")[0]
    }
]
search_text = "soap"
search_embedding = create_embeddings(search_text)[0]

distances = []
for product in products:
  # Compute the cosine distance for each product description
  dist = distance.cosine(search_embedding, product['embedding'])
  distances.append(dist)

# Find and print the most similar product short_description    
min_dist_ind = np.argmin(distances)
print(products[min_dist_ind]['short_description'])