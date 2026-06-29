# Start your code here!

import os
from openai import OpenAI

# Define the model to use

model = "gpt-4o-mini"

# Define the client

client = OpenAI()

# Start coding here

conversation = [
{
"role": "system",
"content": "You are an AI-powered travel guide for Paris working for Peterman Reality Tours. Provide clear, accurate, and helpful answers to tourist questions."
},
{
"role": "user",
"content": "How far away is the Louvre from the Eiffel Tower (in miles) if you are driving?"
},
{
"role": "assistant",
"content": "The driving distance between the Louvre Museum and the Eiffel Tower is approximately 2 miles (about 3.2 kilometers), depending on traffic and route."
},
{
"role": "user",
"content": "Where is the Arc de Triomphe?"
},
{
"role": "assistant",
"content": "The Arc de Triomphe is located in Paris, France, at the western end of the Champs-Élysées in the center of Place Charles de Gaulle."
},
{
"role": "user",
"content": "What are the must-see artworks at the Louvre Museum?"
},
{
"role": "assistant",
"content": "Some must-see artworks at the Louvre Museum include the Mona Lisa by Leonardo da Vinci, the Venus de Milo, and the Winged Victory of Samothrace."
}
]

response = client.chat.completions.create(
model=model,
messages=conversation,
temperature=0.0,
max_tokens=100
)

print(response.choices[0].message.content)
