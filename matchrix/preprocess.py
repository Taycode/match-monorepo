# Extract text from pdf
import PyPDF2

def extract_text_from_pdf(pdf_file: str) -> str:
    with open(pdf_file, 'rb') as resume:
        reader = PyPDF2.PdfReader(resume)
        resume_text = ''

        for page in reader.pages:
            content = page.extract_text()
            resume_text += content
        
        return resume_text
    
