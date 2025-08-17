from fastapi import FastAPI
from pydantic import BaseModel
from pdfminer.high_level import extract_text
from resumeparser import analyze_resume
import requests
from io import BytesIO
import os
import tempfile

class PDFInput(BaseModel):
    path: str

app = FastAPI()

@app.post("/api/resumeparser")
def pdf_parser(request: PDFInput):
    temp_file_path = None
    try:
        # Check if the path is a URL (starts with http or https)
        if request.path.startswith(('http://', 'https://')):
            # Download the PDF file from the URL
            response = requests.get(request.path)
            if response.status_code != 200:
                return {"error": f"Failed to download PDF. Status code: {response.status_code}"}
            
            # Create a temporary file
            fd, temp_file_path = tempfile.mkstemp(suffix='.pdf')
            os.close(fd)
            
            # Write the content to the temporary file
            with open(temp_file_path, 'wb') as f:
                f.write(response.content)
            
            # Extract text from the PDF
            text = extract_text(temp_file_path)
        else:
            # Treat as a local file path
            text = extract_text(request.path)
        
        # Analyze the text
        ans = analyze_resume(text, model_name='llama3.1:8b')
        return ans
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up the temporary file if it exists
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Error removing temporary file: {e}")