## Day 2 – Prompt Engineering (Part 1)

### Creating a Reusable AI Function
We created a function to send prompts to the AI and get responses dynamically.

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content
```

### What This Does

* Takes any prompt as input
* Sends it to the AI model
* Returns the AI’s response

### What I Learned

* How to wrap AI calls inside a reusable function
* How to pass different prompts dynamically
* How the `prompt` controls the output
* `temperature=0` makes responses more accurate and consistent

### Key Insight

* One function → multiple use cases
* The same function can answer questions, summarize, translate, etc.

### Example Usage

```python
response = get_response("Explain AI in one sentence")
print(response)
```



##################################################################################
## Key Principles of Prompt Engineering

### Delimited Prompts (with f-strings)

**Delimiter Meaning:**
A *delimiter* is a symbol or set of symbols used to clearly separate different parts of a prompt. It tells the AI exactly **where the input text starts and ends**, so there is no confusion.

**In this case:**
Triple backticks (```) are used as delimiters.

---

### Why Use Delimiters?

* Clearly separates **instruction** from **data**
* Helps the model focus on the exact content to work on
* Reduces confusion and improves accuracy of responses

---

### Using f-strings

* f-strings allow you to insert variables dynamically into prompts
* Example: `{text}` will be replaced with actual content

---

### Example

````python
prompt = f"""Summarize the text below:

```{text}```
"""
````

---

### What’s Happening

* Instruction: *"Summarize the text below"*
* Delimited content: the text inside ` `
* `{text}` is dynamically inserted using an f-string

---

### Key Idea

> Clear structure + clear separation = better AI understanding and better responses


### Summary
Delimiters are used to clearly pass your data (text, story, or input) to the AI, so it understands exactly what to work on and responds based on that data.


🔹 Custom Output Format

You can control how AI responds by defining a format.

Example
instructions = "You will be provided with a text delimited by triple backticks. Generate a suitable title."

output_format = """Use the following format:
- Text: <text>
- Title: <title>"""

prompt = instructions + output_format + f"""```{text}```"""
🔹 Conditional Prompting

You can tell AI to behave differently based on conditions.

Example
instructions = """You will be provided with a text delimited by triple backticks. Infer the language and the number of sentences. If the text has more than one sentence, generate a title. Otherwise, write 'N/A'."""

output_format = """Use the following format:
Text: <text>
Language: <language>
Number of sentences: <number>
Title: <title>"""

prompt = instructions + output_format + f"""```{text}```"""
🔥 What I Learned Today
How to use delimiters (``` )
How to structure prompts clearly
How to control AI output format
How to use conditional logic in prompts
How to combine everything using f-strings
💡 Personal Understanding

Prompt engineering is not just asking AI questions —
👉 it is about feeding AI structured data and clear instructions so it gives precise results.
