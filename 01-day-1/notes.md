# AI Engineering Journey - Notes

## Day 1 - OpenAI Basics

### What I Learned

* How to install and use `python-dotenv`
* How to store API keys securely in a `.env` file
* How to load environment variables using:

  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
* How to access environment variables:

  ```python
  os.getenv("OPENAI_API_KEY")
  ```

---

### OpenAI API Setup

* Create client:

  ```python
  from openai import OpenAI
  client = OpenAI(api_key=api_key)
  ```

* Basic request:

  ```python
  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "user", "content": "Your question"}
      ]
  )
  ```

---

### Errors I Encountered

* `insufficient_quota` (Error 429)

#### Meaning:

* No billing / no credits

#### Solution:

* Add billing OR use fallback (mock response)

---

### Fallback Strategy (Important)

* If API fails, return a manual response

Example:

```python
try:
    # API call
except:
    print("Fallback response")
```

---

### Key Lessons

* API is not free (pay-as-you-go)
* Always handle errors in production code
* Never expose API keys in code
* Use `.env` for security

---

### My Understanding

* AI apps = Input → API → Response
* I can simulate AI without API for now

---

### Next Step

* Continue course
* Practice without API
* Learn prompt structure






## Tokens and Cost in AI

Tokens:

* Tokens are pieces of text (words or parts of words)
* Both input (prompt) and output (response) use tokens

Max Completion Tokens:

* max_completion_tokens sets the maximum number of tokens the AI can generate
* It is a limit, not a fixed number

Temperature:

* Temperature controls how creative or random the AI response is

Low Temperature (0.0 – 0.3):

* More accurate and predictable
* Best for coding, math, and factual answers

High Temperature (0.7 – 1.0):

* More creative and diverse
* Best for writing, ideas, and storytelling

Important:

* Temperature affects style, not length
* max_completion_tokens affects length, not creativity

Cost:

* Cost is based on both input and output tokens

Formula:
Total Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price)

Tracking Usage:
Use:
response.usage.prompt_tokens
response.usage.completion_tokens

This returns:

* prompt_tokens
* completion_tokens
* total_tokens

Key Idea:

* Always monitor tokens to control cost in real applications

## Mini Project: AI Cost Tracker with Temperature

This project sends a prompt to an AI model, controls creativity, and calculates cost.

Example Code:

from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

prompt = "Explain what a plane is in a simple way"

max_completion_tokens = 100

response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "user", "content": prompt}],
temperature=0.7,
max_completion_tokens=max_completion_tokens
)

output_text = response.choices[0].message.content
print("AI Response:\n", output_text)

# Pricing

input_token_price = 0.15 / 1_000_000
output_token_price = 0.60 / 1_000_000

# Token usage

input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens

# Cost calculation

cost = (input_tokens * input_token_price) + (output_tokens * output_token_price)

print("\nToken Usage:")
print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")

print(f"\nEstimated cost: ${cost:.10f}")

Lesson:

* Temperature controls creativity
* max_completion_tokens controls length
* Tokens determine cost
* Always track usage in real-world AI systems




## Prompting Techniques (Structured Examples)

Prompting techniques help guide how the AI responds by providing examples.

---

### Zero-shot Prompting

* No examples provided

Example:
"Classify sentiment as 1–5 (negative to positive):

This product is amazing!"

Output:
5

Use when:

* Task is simple and clear

---

### One-shot Prompting

* One example provided

Example:
"Classify sentiment as 1–5 (negative to positive):

Terrible product = 1

This product is amazing ="

Output:
5

Use when:

* You want to guide the format or scale

---

### Few-shot Prompting

* Multiple examples provided

Example:
"Classify sentiment as 1–5 (negative to positive):

Love these! = 5
Horrible experience = 1
It's okay, not great = 3

Unbelievably good! =
Shoes fell apart on second use =
The shoes look nice, but aren't comfortable =
Can't wait to show them off! ="

Expected Output:
5
1
3
5

Use when:

* Task needs consistency
* You want better accuracy

---

### Key Idea

* The model learns from the pattern you show
* More examples = better guidance
* More examples = more tokens = higher cost

---

### Summary

* Zero-shot = no example
* One-shot = one example
* Few-shot = multiple examples

Lesson:

* Structure your prompt like teaching a student with examples
