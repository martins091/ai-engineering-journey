#################################################################################################################
# Import the pipeline function
from ast import Load

from transformers import pipeline

# Create a text generation pipeline using GPT-2
gpt2_pipeline = pipeline(
    task="text-generation",
    model="openai-community/gpt2"
)

# Generate two different outputs with a maximum of 10 new tokens
results = gpt2_pipeline(
    "What if AI",
    max_new_tokens=10,
    num_return_sequences=2
)

# Print each generated result
for i, result in enumerate(results, 1):
    print(f"Output {i}:")
    print(result['generated_text'])
    print("-" * 30)

##################################################################################################################
from datasets import load_dataset

# Load both datasets
my_dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="validation")
wikipedia = load_dataset("wikipedia", "20220301.en", split="train[:1%]")

print(my_dataset)

# Now this will work
filtered = wikipedia.filter(lambda row: "football" in row["text"])

example = filtered.select(range(1))

print(example[0]["text"])


###################################################################################################################
# Create a pipeline for grammar checking
grammar_checker = pipeline(
  task="text-classification", 
  model="abdulmatinomotoso/English_Grammar_Checker"
)

# Check grammar of the input text
output = grammar_checker("I will walk dog")
print(output)


###################################################################################################################
# Create the pipeline
classifier = pipeline(task="text-classification", model="cross-encoder/qnli-electra-base")

# Predict the output
output = classifier("Where is the capital of France?, Brittany is known for its stunning coastline.")

print(output)

###################################################################################################################
text = "AI-powered robots assist in complex brain surgeries with precision."

# Create the pipeline
classifier = pipeline(task="zero-shot-classification", model="facebook/bart-large-mnli")

# Create the categories list
categories = ["politics", "technology", "health"]

# Predict the output
output = classifier(text, categories)

# Print the top label and its score
print(f"Top Label: {output['labels'][0]} with score: {output['scores'][0]}")


###################################################################################################################
# Create the summarization pipeline
original_text = " In a groundbreaking development, AI-powered robots have been successfully assisting in complex brain surgeries. These robots are equipped with advanced imaging and precision tools, allowing surgeons to perform intricate procedures with enhanced accuracy. The integration of AI technology in the operating room has led to improved patient outcomes, reduced recovery times, and minimized risks associated with traditional surgical methods. As the medical community continues to embrace these innovations, the future of neurosurgery looks promising, with AI playing a pivotal role in advancing healthcare."
summarizer = pipeline(task="summarization", model="cnicu/t5-small-booksum")

# Summarize the text
summary_text = summarizer(original_text)

# Compare the length
print(f"Original text length: {len(original_text)}")
print(f"Summary length: {len(summary_text[0]['summary_text'])}")


###################################################################################################################
short_summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum",
    min_new_tokens=1,
    max_new_tokens=10
)

short_summary_text = short_summarizer(original_text)

print(short_summary_text[0]["summary_text"])

###################################################################################################################
# Repeat for a summary between 50 and 150 tokens
long_summarizer = pipeline(
    task="summarization",
    model="cnicu/t5-small-booksum",
    min_new_tokens=50,
    max_new_tokens=150
)

long_summary_text = long_summarizer(original_text)

print(long_summary_text[0]["summary_text"])