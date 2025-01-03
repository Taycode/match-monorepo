import requests
from io import BytesIO
from docx import Document
import fitz


class DocumentReader:
    @staticmethod
    def fetch_document(url):
        """
        Fetch the document from the given URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.content, response.headers.get('Content-Type', '')
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch the document: {e}")

    @staticmethod
    def read_pdf(file_stream):
        """
        Extract text from a PDF file stream.
        """
        try:
            pdf_content = ""
            with fitz.open(stream=file_stream, filetype="pdf") as pdf_document:
                for page in pdf_document:
                    pdf_content += page.get_text()
            return pdf_content
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}")

    @staticmethod
    def read_docx(file_stream):
        """
        Extract text from a DOCX file stream.
        """
        try:
            doc_content = ""
            document = Document(file_stream)
            for paragraph in document.paragraphs:
                doc_content += paragraph.text + "\n"
            return doc_content
        except Exception as e:
            raise ValueError(f"Failed to read DOCX: {e}")

    def read_document(self, url):
        """
        Main method to fetch and extract text from a document (PDF or DOCX) at a given URL.
        """
        try:
            file_content, content_type = self.fetch_document(url)
            file_stream = BytesIO(file_content)

            if 'application/pdf' in content_type or url.endswith('.pdf'):
                return self.read_pdf(file_stream)
            elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type or url.endswith('.docx'):
                return self.read_docx(file_stream)
            else:
                raise ValueError("Unsupported document type. Only PDF and DOCX are supported.")
        except Exception as e:
            return f"An error occurred: {e}"
