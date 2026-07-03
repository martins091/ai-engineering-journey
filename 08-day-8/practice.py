
from pyexpat.errors import messages
from xml.parsers.expat import model

from openai import OpenAI
message_listing = {
    "role": "user",
    "content": "Please provide a summary of the latest advancements in AI research."
}
function_definition = {
    "name": "summarize_ai_research",
    "description": "Summarizes the latest advancements in AI research.",
    "parameters": {
        "type": "object",
        "properties": {
            "summary_length": {
                "type": "string",
                "enum": ["short", "medium", "long"],
                "description": "The desired length of the summary."
            }
        },
        "required": ["summary_length"]
    }
}

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response= client.chat.completions.create(
    model="gpt-4o-mini",
    # Add the message 
    messages=message_listing,
    # Add your function definition
    tools=function_definition
)

# Print the response
print(response.choices[0].message.tool_calls[0].function.arguments).


##########################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the function parameter type
function_definition[0]['function']['parameters']['type'] = "object"

# Define the function properties
function_definition[0]['function']['parameters']['properties'] = {
    "title": {
        "type": "string",
        "description": "The title of the research paper"
    },
    "year": {
        "type": "string",
        "description": "The year of publication of the research paper"
    }
}

response = get_response(messages, function_definition)
print(response)

############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = get_response(messages, function_definition)

# Define the function to extract the data dictionary
def extract_dictionary(response):
    return response.choices[0].message.tool_calls[0].function.arguments

# Print the data dictionary
print(extract_dictionary(response))


#############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Append the second function
function_definition.append({
    'type': 'function',
    'function': {
        'name': 'reply_to_review',
        'description': 'Generate a reply to the customer review',
        'parameters': {
            'type': 'object',
            'properties': {
                'reply': {
                    'type': 'string',
                    'description': 'A response to the customer review'
                }
            }
        }
    }
})

response = get_response(messages, function_definition)

# Print the response
print(response)

##############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
    model=model,
    messages=messages,
    # Add the function definition
    tools=function_definition,
    # Specify the function to be called for the response
    tool_choice={
        "type": "function",
        "function": {"name": "extract_review_info"}
    }
)

# Print the response
print(response.choices[0].message.tool_calls[0].function.arguments)

###############################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Modify the messages
messages.append({
    "role": "system",
    "content": "Do not make assumptions about missing values. If the required information is not present, return an empty response."
})

response = get_response(messages, function_definition)

print(response)

################################################################################################################

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the function to pass to tools
function_definition = [{
    "type": "function",
    "function": {
        "name": "get_exchange_rate",
        "description": "Return a matching currency code from the user input",
        "parameters": {
            "type": "object",
            "properties": {
                "currency_code": {
                    "type": "string",
                    "description": "The currency code to look up"
                }
            }
        },
        "result": {
            "type": "string"
        }
    }
}]

response = get_response(function_definition)
print(response)

#################################################################################################################
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Call the Chat Completions endpoint 
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a currency exchange assistant. Extract the relevant currency code from the user input."},
    {"role": "user", "content": "I'd like to know the current exchange rates for the Euro."}
  ],
  tools=function_definition
)

print_response(response)

#################################################################################################################
if response.choices[0].finish_reason == 'tool_calls':
    function_call = response.choices[0].message.tool_calls[0].function
    
    # Check function name
    if function_call.name == "get_exchange_rate":
        # Extract currency code
        import json
        code = json.loads(function_call.arguments)["currency_code"]
        
        exchange_info = get_exchange_rate(code)
        print(exchange_info)
    else:
        print("Apologies, I couldn't find the requested currency.")
else: 
    print("I am sorry, but I could not understand your request.")