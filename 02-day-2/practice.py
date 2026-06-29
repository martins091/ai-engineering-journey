
from email.mime import text
from xmlrpc import client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

############################################################################################################
def get_response(prompt):
  # Create a request to the chat completions endpoint
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}], 
    temperature = 0)
  return response.choices[0].message.content

# Test the function with your prompt
response = get_response("write a poem about ChatGPT")
print(response)

###########################################################################################################
# Craft a prompt that follows the instructions
prompt = "write a poem about ChatGPT, ensure that it is writtn in basic English that a child can understand"

# Get the response
response = get_response(prompt)

print(response)




###########################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")


story = """Once upon a time, in a land far away, there was a little village where everyone loved to tell stories. The villagers would gather every evening to share tales of adventure, magic, and friendship. One day, a mysterious traveler arrived in the village, carrying a book filled with ancient secrets. The villagers were eager to hear the traveler's stories and learn from the wisdom contained within the book."""
 

# Create a prompt that completes the story
prompt = f"""Complete the story delimited by triple backticks. 
 ```{story}```"""

# Get the generated response 
response = get_response(prompt)

print("\n Original story: \n", story)
print("\n Generated story: \n", response)



#################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a prompt that generates the table
prompt = "Generate a table of 10 books that a science fiction lover should read, with columns for Title, Author, and Year."
response = get_response(prompt)
# Get the response
response = get_response(prompt)
print(response)

#########################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the instructions
instructions = """You will be provided with a text delimited by triple backticks. Infer the language and the number of sentences in the text. If the text contains more than one sentence, generate a suitable title. Otherwise, write 'N/A' for the title."""

# Create the output format
output_format = """Use the following format for the output:
Text: <text>
Language: <language>
Number of sentences: <number of sentences>
Title: <title>"""

prompt = instructions + output_format + f"""```{text}```"""
response = get_response(prompt)
print(response)




##############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a one-shot prompt
prompt = """Extract the odd numbers from the set.

Example:
Input: {1, 3, 7, 12, 19}
Output: {1, 3, 7, 19}

Now do the same for the following set:
Input: {3, 5, 11, 12, 16}
Output:"""

response = get_response(prompt)
print(response)


#####################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": "The product quality exceeded my expectations"},
    {"role": "assistant", "content": "1"},

    {"role": "user", "content": "I had a terrible experience with this product's customer service"},
    {"role": "assistant", "content": "-1"},

    # Text to classify
    {"role": "user", "content": "The price of the product is really fair given its features."}
  ],
  temperature=0
)

print(response.choices[0].message.content)


#####################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a single-step prompt to get help planning the vacation
prompt = "Help me plan the perfect beach vacation, including destination ideas, activities, budget tips, and travel suggestions."

response = get_response(prompt)
print(response)


###############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a prompt detailing steps to plan the trip
prompt = """Help me plan a beach vacation.

Provide exactly four potential beach locations.

For each location, include:
- Accommodation options (at least 2)
- Activities available in that location
- Pros and cons of choosing that location

Make sure each of the four locations is fully evaluated separately so I can compare them easily."""

response = get_response(prompt)
print(response)



#################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

code = '''
def calculate_rectangle_area(length, width):
    area = length * width
    return area
'''

# Create a prompt that analyzes correctness of the code
prompt = f"""Analyze the following Python function and evaluate it based on these three criteria:

1. Correct syntax
2. Receives exactly two inputs (parameters)
3. Returns exactly one output

Code:
{code}

For each criterion, clearly state whether it is correct or incorrect and briefly explain why."""

response = get_response(prompt)
print(response)


#############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the chain-of-thought prompt
prompt = """Your friend is 20 years old. Your friend's father is currently twice your friend's age.

Step by step:
1. Determine the father's current age.
2. Calculate how old the father will be in 10 years.
Show your reasoning clearly before giving the final answer."""

response = get_response(prompt)
print(response)


####################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the self_consistency instruction
self_consistency_instruction = """Solve the problem using three different reasoning approaches (three "experts").
Each expert should solve it independently step by step.
Then compare their final answers and choose the most common result using majority vote."""

# Create the problem to solve
problem_to_solve = "If you own a store that sells laptops and mobile phones. You start your day with 50 devices in the store, out of which 60% are mobile phones. Throughout the day, three clients visited the store, each of them bought one mobile phone, and one of them bought additionally a laptop. Also, you added to your collection 10 laptops and 5 mobile phones. How many laptops and mobile phones do you have by the end of the day?"

# Create the final prompt
prompt = self_consistency_instruction + "\n\n" + problem_to_solve

response = get_response(prompt)
print(response)


######################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Refine the following prompt
prompt = "Provide a table of the top 10 pre-trained language models. The table should have three columns: Model Name, Release Year, and Owning Company."

response = get_response(prompt)
print(response)

##################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Refine the following prompt
prompt = """
Receiving a promotion at work made me feel on top of the world -> Happiness
The movie's ending left me with a heavy feeling in my chest -> Sadness
Walking alone in the dark alley sent shivers down my spine -> Fear
Time flies like an arrow -> no explicit emotion
They sat and ate their meal ->
"""

response = get_response(prompt)
print(response)


######################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to transform the text
prompt = f"""Improve the following text in two steps:

1. Proofread the text by correcting grammar and spelling errors without changing its original structure.
2. Adjust the tone to be formal and friendly while keeping the meaning the same.

Text:
{text}
"""

response = get_response(prompt)

print("Before transformation:\n", text)
print("After transformation:\n", response)