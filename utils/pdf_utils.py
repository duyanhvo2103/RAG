# utils/pdf_utils.py
import re

def clean_pdf_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\x00", "").replace("\ufeff", "").replace("�", "")
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    return text.strip()
