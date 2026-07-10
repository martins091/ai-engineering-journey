# Day 15: Software Engineering for Data Scientists 🚀

## Table of Contents
1. [Why Software Engineering for Data Scientists](#why-software-engineering-for-data-scientists)
2. [Modularity](#modularity)
3. [Documentation](#documentation)
4. [Testing](#testing)
5. [Packages & PyPI](#packages--pypi)
6. [pip Package Manager](#pip-package-manager)
7. [Reading Documentation with help()](#reading-documentation-with-help)
8. [Key Takeaways](#key-takeaways)
9. [Quick Reference](#quick-reference)

---

## Why Software Engineering for Data Scientists

### The Problem

| Problem | Reality |
|---------|---------|
| Many Data Scientists start in math/statistics | Not formal programmers |
| Code is seen as a "means to an end" | Just to create models |
| Self-taught programmers | Missing best practices |

### The Solution

| Skill | Why It Matters |
|-------|---------------|
| **Modularity** | Code is reusable, readable, debuggable |
| **Documentation** | Others (and future you) can understand |
| **Testing** | Catch bugs early and often |
| **Version Control** | Track changes, collaborate |

---

## Modularity

### What is Modularity?

**Modularity = Breaking code into small, reusable, functional units**

### Non-Modular Code (Bad) ❌

```python
# Everything in one big script - HARD TO READ! 😱
import pandas as pd
df = pd.read_csv('data.csv')
df['new_col'] = df['col1'] + df['col2']
df_clean = df.dropna()
result = df_clean.groupby('category').mean()
print(result)
Modular Code (Good) ✅
python
# Separate functions - EASY TO READ! ✅
import pandas as pd

def load_data(filepath):
    """Load data from CSV file"""
    return pd.read_csv(filepath)

def clean_data(df):
    """Clean data by removing missing values and adding columns"""
    df = df.dropna()
    df['new_col'] = df['col1'] + df['col2']
    return df

def aggregate_data(df):
    """Aggregate data by category"""
    return df.groupby('category').mean()

# Main workflow
df = load_data('data.csv')
df_clean = clean_data(df)
result = aggregate_data(df_clean)
Benefits of Modularity
Benefit	Why It Helps
Readable	Code is easier to understand
Debuggable	Easier to find and fix bugs
Reusable	Use functions in other projects
Testable	Test each function individually
Maintainable	Easier to update and change
Three Ways to Write Modular Code in Python
python
# 1. PACKAGES: Import existing code
import pandas as pd

# 2. CLASSES: Create objects with data and methods
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def clean(self):
        self.data = self.data.dropna()
        return self.data
    
    def aggregate(self, column):
        return self.data.groupby(column).mean()

# 3. METHODS: Functions that belong to classes/objects
df = pd.DataFrame(data)
df.plot('x', 'y')  # plot is a method of DataFrame
Modularity in the Wild (Example)
python
# Import the numpy package
import numpy as np

# Create an array class object
arr = np.array([8, 6, 7, 5, 3, 0, 9])

# Use the sort method
arr.sort()

# Print the sorted array
print(arr)  # Output: [0 3 5 6 7 8 9]
Concept	Code	Purpose
Package	import numpy as np	Import the numpy library
Class	np.array([...])	Create an array object
Method	arr.sort()	Sort the array
Documentation
What is Documentation?
Documentation = Explaining what your code does and how to use it

Who Needs Documentation?
User	Why They Need It
Future You	You'll forget what you wrote!
Team Members	Others need to understand your code
Users	People using your package need guidance
Debugging	Easier to fix issues with clear docs
Types of Documentation
1. Comments
python
# Calculate average sales per category
avg_sales = df.groupby('category')['sales'].mean()

# Check if sales exceed threshold
if avg_sales > 1000:
    print("Sales are above target!")
2. Docstrings (Python's Built-in Documentation)
python
def calculate_average_sales(df, category_col='category', sales_col='sales'):
    """
    Calculate average sales per category.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame containing sales data
    category_col : str, default='category'
        Column name for categories
    sales_col : str, default='sales'
        Column name for sales values
    
    Returns:
    --------
    pandas.Series
        Average sales per category
    
    Examples:
    ---------
    >>> df = pd.DataFrame({'category': ['A', 'B'], 'sales': [100, 200]})
    >>> calculate_average_sales(df)
    A    100
    B    200
    dtype: int64
    """
    return df.groupby(category_col)[sales_col].mean()
3. Self-Documenting Code (Clear Names)
python
# ❌ BAD - Hard to understand
def a(x, y):
    return x / y * 100

# ✅ GOOD - Clear meaning
def calculate_percentage(part, whole):
    """Calculate what percentage 'part' is of 'whole'"""
    return (part / whole) * 100
Docstring Formatting
Section	Description
Summary	One-line description of what the function does
Parameters	List each parameter with type and description
Returns	What the function returns with type and description
Examples	Example usage of the function
Testing
What is Testing?
Testing = Writing code that checks if your other code works correctly

Why Testing Matters
python
# People make mistakes!
# That's why pencils have erasers, 
# computers have spellcheck, 
# and software needs tests! 🧪
Without Testing
python
def add_numbers(a, b):
    return a + b

# You test once, hope it works, move on... 😰
# But what if you change it later? What if it breaks?
With Testing (Using pytest)
python
# test_calculations.py
def test_add_numbers():
    """Test the add_numbers function"""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(2.5, 3.5) == 6.0
    print("All tests passed! ✅")

# Run test
test_add_numbers()
Benefits of Automated Testing
Benefit	Why It Helps
Catch Bugs Early	Find problems before they cause issues
Test After Changes	Ensure new code doesn't break old code
Prevent Regression	Old features still work after updates
Confidence	Deploy with confidence
Documentation	Tests show how code should work
Simple Testing Framework
python
# test_example.py

def test_clean_data():
    """Test that clean_data removes missing values"""
    df = pd.DataFrame({
        'category': ['A', 'B', None],
        'sales': [100, 200, 300]
    })
    
    df_clean = clean_data(df)
    
    assert len(df_clean) == 2
    assert df_clean['category'].isna().sum() == 0

def test_calculate_sales_summary():
    """Test sales summary calculation"""
    df = pd.DataFrame({
        'category': ['A', 'A', 'B', 'B'],
        'sales': [100, 200, 300, 400]
    })
    
    summary = calculate_sales_summary(df)
    
    assert summary['A'] == 150
    assert summary['B'] == 350

# Run all tests
if __name__ == "__main__":
    test_clean_data()
    test_calculate_sales_summary()
    print("All tests passed! ✅")
Common Assertions
Assertion	What It Checks
assert x == y	x equals y
assert x != y	x does not equal y
assert x > y	x is greater than y
assert x < y	x is less than y
assert x in list	x is in the list
assert x is None	x is None
Packages & PyPI
What is PyPI?
PyPI = Python Package Index

Think of it like an App Store for Python packages! 🏪

text
PyPI (App Store)
├── numpy
├── pandas
├── requests
├── openai
├── pinecone
└── 400,000+ more packages!
Why Use Packages?
Benefit	Why It Helps
Reusable	Don't reinvent the wheel
Battle-Tested	Used by thousands of developers
Community Support	Regular updates and bug fixes
Time-Saving	Focus on your problem, not the basics
pip Package Manager
What is pip?
pip = "Pip Installs Packages" (recursive acronym)

Common pip Commands
bash
# Install a package
pip install numpy

# Install a specific version
pip install numpy==1.24.0

# Install multiple packages
pip install numpy pandas matplotlib

# Install package with dependencies
pip install -r requirements.txt

# Uninstall a package
pip uninstall numpy

# List installed packages
pip list

# Show package information
pip show numpy

# Upgrade a package
pip install --upgrade numpy
Installing Packages
bash
# Example: Install numpy
pip install numpy

# Example: Install OpenAI package
pip install openai

# Example: Install Pinecone package
pip install pinecone

# Example: Install multiple packages at once
pip install numpy pandas matplotlib seaborn openai pinecone
Requirements File
txt
# requirements.txt
numpy==1.24.0
pandas==2.0.0
openai==1.0.0
pinecone==3.0.0
bash
# Install all packages from requirements file
pip install -r requirements.txt
Reading Documentation with help()
What is help()?
help() = Python's built-in function to read documentation

Using help() on Different Objects
1. Help on a Function
python
import numpy as np

# Get help on busday_count function
help(np.busday_count)
Output:

text
Help on function busday_count in module numpy:

busday_count(begindates, enddates, weekmask='1111100', holidays=None, 
             busdaycal=None, out=None)
    Counts the number of valid days between begindates and enddates.
    
    Parameters
    ----------
    begindates : array_like of datetime64[D]
        The array of the first dates for counting.
    enddates : array_like of datetime64[D]
        The array of the end dates for counting.
    weekmask : str or array_like of bool, optional
        A seven-element array indicating which days are valid.
    holidays : array_like of datetime64[D], optional
        An array of dates to consider as invalid dates.
    
    Returns
    -------
    out : array_like
        An array of integers representing the number of valid days.
    
    Examples
    --------
    >>> np.busday_count('2024-01-01', '2024-12-31')
    262
    """
2. Help on a Package
python
# Get high-level documentation on numpy
help(np)
3. Help on Any Object
python
# Help on a number
help(5)

# Help on a string
help("hello")

# Help on a list
help([])

# Help on a dictionary
help({})
Example: Using help() to Learn a New Function
python
import numpy as np

# Problem: Count business days in 2024

# 1. First, read the documentation
help(np.busday_count)

# 2. Based on documentation, we need:
#    - begindates: start date
#    - enddates: end date
#    - weekmask: default = Mon-Fri
#    - holidays: optional

# 3. Use the function
start_date = '2024-01-01'
end_date = '2024-12-31'

business_days = np.busday_count(start_date, end_date)
print(f"Business days in 2024: {business_days}")
Output:

text
Business days in 2024: 262
When Documentation is Missing
python
def undocumented_function(x):
    return x * 2

# No documentation!
help(undocumented_function)
Output:

text
Help on function undocumented_function in module __main__:

undocumented_function(x)
Remember: It's up to the developer to include documentation!

Key Takeaways
The 3 Pillars of Software Engineering
Pillar	What It Means	Why Important
Modularity	Break code into small functions	Reusable, readable, debuggable
Documentation	Explain what code does	Others (and future you) can understand
Testing	Write code to test code	Catch bugs early and often
The Golden Rules of Day 15
MODULARITY: One function = One job

DOCUMENTATION: Explain everything! Future you will thank you

TESTING: Always test your code

PACKAGES: Don't reinvent the wheel

help(): Your best friend for learning packages

Quick Reference
Modularity Cheat Sheet
python
# 1. MODULARITY - One function = One job
def load_data():
    pass

def clean_data():
    pass

def analyze_data():
    pass

# 2. Use packages
import pandas as pd

# 3. Use classes and methods
df = pd.DataFrame(data)
df.plot('x', 'y')
Documentation Cheat Sheet
python
def my_function(param1, param2):
    """
    What this function does.
    
    Parameters:
    -----------
    param1 : type - description
    param2 : type - description
    
    Returns:
    --------
    type - description
    
    Examples:
    ---------
    >>> my_function(1, 2)
    3
    """
    return param1 + param2
Testing Cheat Sheet
python
# Simple tests
def test_my_function():
    assert my_function(2, 3) == 5
    assert my_function(-1, 1) == 0
    assert my_function(0, 0) == 0
    print("All tests passed! ✅")
pip Commands Cheat Sheet
bash
pip install package        # Install package
pip install package==1.0   # Install specific version
pip install -r requirements.txt  # Install from file
pip uninstall package      # Uninstall
pip list                   # List installed packages
pip show package           # Show package info
help() Commands Cheat Sheet
python
help(package)              # Package documentation
help(package.function)     # Function documentation
help(package.class)        # Class documentation
help(object)               # Object documentation
help()                     # Interactive help session
One Sentence Summary
"Write clean, documented, tested code - your future self will thank you!" 🚀

Additional Resources
Python Documentation

PyPI - Python Package Index

pytest Documentation

PEP 257 - Docstring Conventions