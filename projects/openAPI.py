# Import the necessary Libraries
import pandas as pd
from openai import OpenAI
import json

# Load the data
df = pd.read_csv("data/transcriptions.csv")
df.head()

# Initialize the OpenAI client
client = OpenAI()

# Function to extract medical information
def extract_medical_info(transcription):
    prompt = f"""
    Extract the following information from this medical transcription:
    1. Patient's age (extract as a number or 'Unknown' if not mentioned)
    2. Medical specialty (infer from the context if not explicitly stated)
    3. Recommended treatment (specific treatment plan mentioned)
    4. Most appropriate ICD-10-CM code for the primary diagnosis
    
    Return ONLY valid JSON with these exact fields:
    {{
        "age": "patient age as number or 'Unknown'",
        "medical_specialty": "inferred specialty",
        "treatment": "detailed treatment recommendation",
        "icd_code": "ICD-10 code only"
    }}
    
    Transcription: {transcription}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a medical coding specialist. Extract structured medical data including patient age, specialty, treatment, and ICD-10 codes. Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        print(f"Error processing transcription: {e}")
        return {
            "age": "Unknown",
            "medical_specialty": "Unknown",
            "treatment": "Unable to extract",
            "icd_code": "Unable to code"
        }

# Process each transcription
print("Processing transcriptions... This may take a few minutes.")

# Create a list to store results
extracted_data = []

for index, row in df.iterrows():
    print(f"Processing transcription {index + 1} of {len(df)}...")
    result = extract_medical_info(row['transcription'])
    result['transcription'] = row['transcription']
    extracted_data.append(result)

# Create the structured DataFrame with the required fields
df_structured = pd.DataFrame(extracted_data)

# Ensure columns are in the correct order
df_structured = df_structured[['age', 'medical_specialty', 'treatment', 'icd_code', 'transcription']]

# Display the results
print("\nStructured Data:")
df_structured.head()

# Optional: Save to CSV
df_structured.to_csv("structured_transcriptions.csv", index=False)

# Verify the structure
print("\nDataFrame structure:")
print(df_structured.info())
print("\nFirst few rows:")
print(df_structured.head())