from ollama import Client
import json
import re
import asyncio
async def analyze_email(text, model_name='llama3.1:8b'):
    """Analyze resume text and return structured JSON data"""
    client = Client(host='http://localhost:11434')
    
    # Structured prompt for JSON output
    prompt = f"""Extract the following information from this email in JSON format:
    {text}
    
    Return JSON with these keys:
    -"sentiment type"(string) either "NEGATIVE", "POSITIVE","NEUTRAL" if highly satisfied when senders is happy then positive provide accordingly responses.
    -"email_summary"(string limit upto 30 words)
    -"email_issues"(string)if any problem arrise from the sender side In 2_3 words
    -"resolution"(string)within 20 words in straight forward manner.

    
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



