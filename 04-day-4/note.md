# Day 4 — Hugging Face 🤖

**Transition: Web Dev → AI Engineering**

## 📌 Overview

Today I was introduced to Hugging Face and how AI models actually work with data.
I learned that AI is not magic — it relies heavily on datasets and how we use them.

---

## 📚 Key Concepts

### 1. Datasets

* Datasets are collections of data used in AI
* Can be used for training, testing, or experimenting
* Example:

```python
from datasets import load_dataset

dataset = load_dataset("TIGER-Lab/MMLU-Pro", split="validation")
print(dataset)
```

---

### 2. Models vs Data

* **Model** = the brain (makes predictions)
* **Dataset** = the knowledge (what the model learns from)
* Models don’t “know” anything without data

---

### 3. Data Filtering

* You can extract specific information from datasets
* Example:

```python
filtered = wikipedia.filter(lambda row: "football" in row["text"])
example = filtered.select(range(1))

print(example[0]["text"])
```

---

### 4. Pipelines (Hugging Face)

Pipelines make it easy to use AI models without building from scratch.

#### Example:

```python
from transformers import pipeline

classifier = pipeline(task="text-classification")
```

---

## 🧠 Tasks I Practiced

### ✔ Text Classification

* Used for labeling text (e.g., sentiment, grammar)

### ✔ Grammar Checking

* Model checks if a sentence is correct

### ✔ QNLI (Question Answering Check)

* Determines if a text contains enough info to answer a question

### ✔ Zero-Shot Classification

* Classifies text into categories without prior training

### ✔ Summarization

* Reduces long text into shorter meaningful content

---

## 💡 Key Takeaways

* AI models depend on data
* Hugging Face provides ready-to-use models & datasets
* Pipelines simplify working with AI
* You don’t always need to train a model from scratch

---

## 🚀 Next Step

Start building with models and applying what I’ve learned.

**Day 5 → Build something real**
