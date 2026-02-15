import requests
import trafilatura
from PyPDF2 import PdfReader
from docx import Document
import io

def extract_from_url(url: str) -> dict:
    """Extracts main content from a URL using Trafilatura."""
    result = {
        "source": url,
        "title": "Unknown Title",
        "content": "",
        "word_count": 0,
        "success": False,
        "error": None
    }
    
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            content = trafilatura.extract(downloaded, include_comments=False, favor_precision=True)
            if content:
                result["content"] = content
                result["word_count"] = len(content.split())
                result["success"] = True
                
                # Try to extract title
                # Simple extraction, could be improved with BS4 if needed
                if "<title>" in downloaded:
                    start = downloaded.find("<title>") + 7
                    end = downloaded.find("</title>", start)
                    if start != -1 and end != -1:
                        result["title"] = downloaded[start:end]
            else:
                result["error"] = "Content extraction failed (empty content)"
        else:
            result["error"] = "Failed to fetch URL"
    except Exception as e:
        result["error"] = f"Error extracting from URL: {str(e)}"
        
    return result

def extract_from_pdf(file) -> dict:
    """Extracts text from a PDF file."""
    result = {
        "source": file.name,
        "title": file.name,
        "content": "",
        "word_count": 0,
        "success": False,
        "error": None
    }
    
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
            
        if text.strip():
            result["content"] = text
            result["word_count"] = len(text.split())
            result["success"] = True
        else:
            result["error"] = "No text found in PDF"
    except Exception as e:
        result["error"] = f"Error extracting from PDF: {str(e)}"
        
    return result

def extract_from_docx(file) -> dict:
    """Extracts text from a DOCX file."""
    result = {
        "source": file.name,
        "title": file.name,
        "content": "",
        "word_count": 0,
        "success": False,
        "error": None
    }
    
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        
        if text.strip():
            result["content"] = text
            result["word_count"] = len(text.split())
            result["success"] = True
        else:
            result["error"] = "No text found in DOCX"
    except Exception as e:
        result["error"] = f"Error extracting from DOCX: {str(e)}"
        
    return result

def extract_from_text(file) -> dict:
    """Extracts text from TXT or MD file."""
    result = {
        "source": file.name,
        "title": file.name,
        "content": "",
        "word_count": 0,
        "success": False,
        "error": None
    }
    
    try:
        # Try to decode with utf-8, fallback if needed could be added
        text = file.read().decode("utf-8")
        
        if text.strip():
            result["content"] = text
            result["word_count"] = len(text.split())
            result["success"] = True
        else:
            result["error"] = "Empty file"
    except Exception as e:
        result["error"] = f"Error reading file: {str(e)}"
        
    return result

def aggregate_content(sources: list[dict]) -> dict:
    """Aggregates content from multiple extracted sources."""
    aggregated = {
        "combined_content": "",
        "total_word_count": 0,
        "sources_summary": [],
        "valid": False,
        "error": None
    }
    
    for source in sources:
        if source["success"]:
            aggregated["combined_content"] += f"\n\n--- Source: {source['title']} ---\n{source['content']}"
            aggregated["total_word_count"] += source["word_count"]
            aggregated["sources_summary"].append(f"✅ {source['title']} ({source['word_count']} words)")
        else:
            aggregated["sources_summary"].append(f"❌ {source['source']}: {source['error']}")
            
    if aggregated["total_word_count"] >= 500:
        aggregated["valid"] = True
    else:
        aggregated["error"] = f"Content too short ({aggregated['total_word_count']} words). Minimum 500 words required."
        
    return aggregated
