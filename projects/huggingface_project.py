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