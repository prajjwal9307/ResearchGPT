import fitz
import os

def save_uploaded_file(uploaded_file):
    """Save the Uploaded File in Data Folder."""
    
    file_path=os.path.join("data",uploaded_file.name)

    with open(file_path,"wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF"""

    text=""

    try:
        doc=fitz.open(pdf_path)
        for page in doc:
            text+=page.get_text()
        
        doc.close()

    
    except Exception as e:
        print("Error:",e)
    
    if not text.strip():
        return "No text found in PDF."
    
    return text
