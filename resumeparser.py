from ollama import Client
import json
import re

def analyze_resume(text, model_name='llama3.1:8b'):
    """Analyze resume text and return structured JSON data"""
    client = Client(host='http://localhost:11434')
    
    # Structured prompt for JSON output
    prompt = f"""Extract the following information from this resume in JSON format:
    {text}
    
    Return JSON with these keys:
    - "first_name" (string)
    -"last_name"(string)
    - "email" (email)
    - "phone_no" (integer)
    -"adress (string) so that we can use this to fill in form"
    - "education" (array of strings)
    - "passing out date (date) with course mapped correctly so that we can use this to fill in form"
    - "skills" (array of strings)
    - "experience" (array of strings with job titles and durations(format dd-mm-yy) mapped correctly so that we can use this to fill in form)
    - "certifications" (array of strings, optional)
    -"main projects to map in the form (strings) with little bit description"
    
    Format: {{ "key": "value" }} without any additional text."""

    try:
        response = client.chat(model=model_name, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        # Extract JSON from response
        raw_output = response['message']['content']
        
        # Use regex to find JSON in the response
        json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        
        return {"error": "No JSON found in response"}
    
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return {"error": "Invalid JSON format"}
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {"error": str(e)}
