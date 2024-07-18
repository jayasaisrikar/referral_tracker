import os
import pytesseract
from pdf2image import convert_from_path
from .models import JobRole

def get_pdf_text(pdf_path):
    """Extract text from a PDF file using OCR."""
    try:
        images = convert_from_path(pdf_path)
        extracted_text = ""
        for image in images:
            extracted_text += pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        raise ValueError(f"Error processing PDF: {e}")

def parse_resume_and_match_jobs(resume_path, job_roles):
    """Parse the resume text and match with job roles."""
    resume_text = get_pdf_text(resume_path)

    # Delete the resume file
    os.remove(resume_path)

    matched_jobs = []
    for job_role in job_roles:
        job_description = job_role.job_description.lower()
        role = job_role.role
        if job_description in resume_text.lower():
            matched_jobs.append({"job_role": role, "match_percentage": 100})  # Simplified matching for demo

    return matched_jobs, resume_text
