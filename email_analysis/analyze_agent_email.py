from ollama import Client
import json
import re
import asyncio
async def analyze_agent_email(text, model_name='llama3.1:8b'):
    """Analyze resume text and return structured JSON data"""
    client = Client(host='http://localhost:11434')
    
    # Structured prompt for JSON output
    prompt = f"""Extract the following information from this email in JSON format:
    {text}
    
    Return JSON with these keys:
    -"agent_sentiment_type"(string) either "NEGATIVE", "POSITIVE","NEUTRAL" if highly satisfied when reciever is happy then positive provide accordingly responses.,
    -"agent_email_summary"(string limit upto 30 words),
    -"agent_email_issues"(string)if any problem arrise frome the reciever side In 2_3 words,
    -"proper_address"(string)if in the text address the customer how they would like to be addressed like 'Dear', 'Hello', 'Hi'.Provide response in the string as "YES" or "NO"",
    -"prioritized_concerns"(string) if in the text have answer of all the points in order of importance to the customer.Provide response in the string as "YES" or "NO"",
    -"appropriate_apology"(string)if in the agent replies in the text and shows  appropriate apology if sentiment is not satisfied.like using of keywords like 'apologize', 'sorry', 'regret'.Provide response in the string as "YES" or "NO"",
    -"empathy_indicators"(string) Check for empathy indicators in the text like 'understand', 'appreciate', 'apologize', 'sorry', 'concern', 'inconvenience', 'frustration', 'difficult'.Provide response in the string as "YES" or "NO"",

    
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



