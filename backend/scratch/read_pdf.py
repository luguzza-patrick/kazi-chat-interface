from pypdf import PdfReader
import os

pdf_path = "/workspaces/kazi-chat-interface/backend/data/pdfs/Employment Policy.pdf"
reader = PdfReader(pdf_path)
text = ""
# Read first 2 pages
for i in range(min(2, len(reader.pages))):
    text += reader.pages[i].extract_text()

print(text[:2000])
