# Day 1 — OpenAI Basics 🚀

**AI Engineering Journey**

## 📌 Overview

Today I learned the fundamentals of working with AI using APIs and how AI applications are structured.

---

## 🧠 Core Understanding

* AI apps follow a simple flow: **Input → API → Response**
* AI is not magic — it’s controlled by prompts, parameters, and data
* You can simulate AI logic even without an API

---

## 🔑 Key Concepts

### API & Security

* OpenAI API is **pay-as-you-go**
* Never expose API keys in code
* Use `.env` files for security
* Always handle errors in production

---

### Tokens & Cost

* Tokens = pieces of text (input + output)
* Cost depends on total tokens used

**Formula:**
Cost = (Input Tokens × Price) + (Output Tokens × Price)

* Always track token usage in real applications

---

### Model Controls

* **Temperature** → controls creativity

  * Low = accurate
  * High = creative

* **max_completion_tokens** → controls response length

> Key idea: *Creativity ≠ Length*

---

## 🧩 Prompting Techniques

* **Zero-shot** → no examples
* **One-shot** → one example
* **Few-shot** → multiple examples

📌 Lesson:
The AI learns from patterns you provide — like teaching a student.

---

## 🛠️ What I Built

* AI response generator with fallback (no API key)
* Cost tracker using token usage
* Sentiment classifier (zero, one, few-shot)
* Study planning assistant using system prompts
* Guardrails to control AI responses
* Multi-turn conversation handling (chat memory)

---

## 💡 Key Takeaways

* AI = prompts + parameters + tokens
* Good prompts = better results
* Always control cost and usage
* Structure matters when guiding AI

---

## 🚀 Next Step

* Dive deeper into prompting
* Start working with real models
* Build more practical AI tools

**Day 2 → Prompt Engineering 🧠**
