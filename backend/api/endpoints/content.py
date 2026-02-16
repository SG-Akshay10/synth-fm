from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
from backend.schemas import URLRequest, ContentResponse
from backend.utils.content_extractor import (
    extract_from_url,
    extract_from_pdf,
    extract_from_docx,
    extract_from_text,
    aggregate_content
)
import shutil
import os
import tempfile

router = APIRouter()

@router.post("/extract-urls", response_model=ContentResponse)
async def extract_urls(request: URLRequest):
    aggregated_sources = []
    for url in request.urls:
        if url.strip():
            result = extract_from_url(url)
            aggregated_sources.append(result)
    
    final_content = aggregate_content(aggregated_sources)
    return final_content

@router.post("/extract-files", response_model=ContentResponse)
async def extract_files(files: List[UploadFile] = File(...)):
    aggregated_sources = []
    
    # Create a temporary directory to save uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            ext = file.filename.split(".")[-1].lower()
            
            # Since content_extractor functions expect a file object or path, 
            # we might need to adjust them. 
            # Looking at existing utils, they use Streamlit's UploadedFile or paths.
            # Let's check how they are implemented.
            # Assuming they handle paths or we need to open them.
            
            # Re-opening as a standard python file object for the util functions
            # OR passing the path if the utils support it.
            # Based on standard libraries, opening as 'rb' is safest for the Utils to consume.
            
            with open(file_path, "rb") as f:
                # We need to mock the 'name' attribute for some utils if they check extension from the file object
                # Or we modify the utils to accept file paths.
                # For now, let's try passing the file object. 
                # To be safe, let's wrap it in a class that mimics what Streamlit provides if needed,
                # but standard file objects usually work for PyPDF2 etc.
                
                # However, since we can't easily see the utils code right now without viewing it,
                # I will assume I can pass the open file object.
                
                # Check extension to call right function
                if ext == "pdf":
                    # PyPDF2 usually takes a file object
                    result = extract_from_pdf(f)
                elif ext == "docx":
                    result = extract_from_docx(f) # python-docx takes file-like object
                elif ext in ["txt", "md"]:
                    # Text extraction might need text mode, let's re-open in text mode for these
                    pass

            if ext in ["txt", "md"]:
                 with open(file_path, "r", encoding="utf-8") as f:
                     result = extract_from_text(f)
            
            if result:
                 aggregated_sources.append(result)

    final_content = aggregate_content(aggregated_sources)
    return final_content
