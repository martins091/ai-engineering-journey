################################## Project 1: Basic usage of OpenAI API with fallback for missing API key

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No API key found → using mock response")
    print("October has 31 days")
else:
    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "How many days are in October?"}
            ]
        )

        print(response.choices[0].message.content)

    except Exception as e:
        print("API not working → using fallback")
        print("October has 31 days")





# ####################################### Project 2: Basic usage of OpenAI API with token usage and cost calculation 

# Your prompt
prompt = """Replace car with plane and adjust phrase:
A car is a vehicle that is typically powered by an internal combustion engine or an electric motor."""

# Limit for response tokens
max_completion_tokens = 100

# Make request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_completion_tokens=max_completion_tokens
)

# Get AI response
output_text = response.choices[0].message.content
print("AI Response:\n", output_text)

# Pricing (example values)
input_token_price = 0.15 / 1_000_000
output_token_price = 0.60 / 1_000_000

# Extract REAL token usage
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens

# Calculate cost correctly
cost = (input_tokens * input_token_price) + (output_tokens * output_token_price)

print("\nToken Usage:")
print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")

print(f"\nEstimated cost: ${cost:.10f}")




#################################################### Project 3: Sentiment classification

# zero shot prompt for sentiment classification
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")

prompt = """Classify sentiment as 1–5 (negative to positive):

This product is amazing!
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print(response.choices[0].message.content)


# one shot prompt for sentiment classification
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")

prompt = """Classify sentiment as 1–5 (negative to positive):

Terrible product = 1

This product is amazing =
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print(response.choices[0].message.content)


# few shot prompt for sentiment classification
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")

prompt = """Classify sentiment as 1–5 (negative to positive):

Love these! = 5
Horrible experience = 1
It's okay, not great = 3

Unbelievably good! =
Shoes fell apart on second use =
The shoes look nice, but aren't comfortable =
Can't wait to show them off! =
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print(response.choices[0].message.content)



#################################################### Project 4: Study planning assistant

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  max_completion_tokens=150,
  messages=[
    {"role": "system",
     "content": "You are a study planning assistant that creates plans for learning new skills."},
    {"role": "user",
     "content": "I want to learn to speak Dutch."}
  ]
)

# Extract the assistant's text response
print(response.choices[0].message.content)


client = OpenAI(api_key="<OPENAI_API_TOKEN>")

sys_msg = """You are a study planning assistant that creates plans for learning new skills.

If these skills are non related to languages, return the message:

'Apologies, to focus on languages, we no longer create learning plans on other topics.'
"""

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": sys_msg},
    {"role": "user", "content": "Help me learn to ____."}
  ]
)

print(response.choices[0].message.content)



# Guardrail: If the user asks for a learning plan on a non-language skill, the assistant should respond with the message:
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    # Add a user and assistant message for in-context learning
    messages=[
        {"role": "system", "content": "You are a helpful Geography tutor that generates concise summaries for different countries."},
        {"role": "user", "content": "Give me a quick summary of Portugal."},
        {"role": "assistant", "content": "Portugal is a country in Europe that borders Spain. The capital city is Lisboa."},
        {"role": "user", "content": "Give me a quick summary of Greece."}
    ]
)

print(response.choices[0].message.content)




client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
   model="gpt-4o-mini",
   # Add in the extra examples and responses
   messages=[
       {"role": "system", "content": "You are a helpful Geography tutor that generates concise summaries for different countries."},
       {"role": "user", "content": "Give me a quick summary of Portugal."},
       {"role": "assistant", "content": "Portugal is a country in Europe that borders Spain. The capital city is Lisboa."},
       {"role": "user", "content": "Give me quick summary of Nigeria"},
       {"role": "assistant", "content": "Nigeria is a country in Africa that borders Cameroon. The capital city is Abuja."},
       {"role": "user", "content": "Give me a quick summary of Japan."},
       {"role": "assistant", "content": "Japan is a country in East Asia. The capital city is Tokyo."},
       {"role": "user", "content": "Give me a quick summary of Brazil."},
       {"role": "assistant", "content": "Brazil is a country in South America. The capital city is Brasília."},
       {"role": "user", "content": "Give me a quick summary of Greece."}
   ]
)

print(response.choices[0].message.content)