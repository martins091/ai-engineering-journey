################################################################################################################
# Import necessary library for tokenization
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Split input text into tokens
tokens = tokenizer.tokenize("AI: Making robots smarter and humans lazier!")

# Display the tokenized output
print(f"Tokenized output: {tokens}")


################################################################################################################
# Download the model and tokenizer
my_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
my_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Create the pipeline
my_pipeline = pipeline(task="sentiment-analysis", model=my_model, tokenizer=my_tokenizer)

# Predict the sentiment
output = my_pipeline("This course is pretty good, I guess.")
print(f"Sentiment using AutoClasses: {output[0]['label']}")

########################################################################################################
from pypdf import PdfReader

# Extract text from the PDF
reader = PdfReader("US_Employee_Policy.pdf")

# Extract text from all pages
document_text = ""
for page in reader.pages: 
    document_text += page.extract_text()

print(document_text)


########################################################################################################## Load the question-answering pipeline
qa_pipeline = pipeline(task="question-answering", model="distilbert-base-cased-distilled-squad")

question = "What is the notice period for resignation?"

# Get the answer from the QA pipeline
result = qa_pipeline(question=question, context=document_text)

# Print the answer
print(f"Answer: {result['answer']}")


#########################################################################################################
from transformers import pipeline
from pypdf import PdfReader

# Load PDF
reader = PdfReader("projects/martins_resume.pdf")

document_text = ""
for page in reader.pages:
    document_text += page.extract_text()

# Load QA model
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

# Ask questions
while True:
    question = input("\nAsk a question (type 'exit' to stop): ")

    if question.lower() == "exit":
        break

    result = qa_pipeline(
        question=question,
        context=document_text
    )

    print("Answer:", result["answer"])