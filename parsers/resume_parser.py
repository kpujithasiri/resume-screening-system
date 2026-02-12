from pathlib import Path
import PyPDF2


class ResumeParser:
    def __init__(self):
        pass

    def extract_text(self, file_path: str) -> str:
        """
        Detect file type and extract text accordingly.
        """
        file_path = Path(file_path)

        if file_path.suffix.lower() == ".pdf":
            return self._extract_pdf(file_path)

        elif file_path.suffix.lower() == ".docx":
            return self._extract_docx(file_path)

        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are allowed.")

    def _extract_pdf(self, file_path: Path) -> str:
        text = ""

        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text.strip()

    def _extract_docx(self, file_path: Path) -> str:
        from docx import Document

        doc = Document(file_path)

        return "\n".join(
            para.text for para in doc.paragraphs
        ).strip()
