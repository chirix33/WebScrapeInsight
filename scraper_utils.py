import os
import hashlib
from bs4 import BeautifulSoup
import spacy
from difflib import unified_diff
import pymupdf
import requests

# Load SpaCy model
nlp = spacy.load("en_core_web_md")

# Directory Setup
BASE_DIR = "scraped_content"
CHANGES_DIR = "changes"

# Extract Meaningful Text from HTML
def extract_meaningful_text(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text()
    doc = nlp(text)
    return "\n\n".join([sent.text.strip() for sent in doc.sents])

# Extract text from PDF
def extract_text_from_pdf(pdf_url):
    response = requests.get(pdf_url)
    temp_file_path = "temp_files/"+hashlib.md5(pdf_url.encode()).hexdigest()+".pdf"
    
    with open(temp_file_path, "wb") as file:
        file.write(response.content)
    
    doc = pymupdf.open(temp_file_path)
    text = ""
    for page in doc:
        text += page.get_text().encode("utf8")
    doc.close()
    os.remove(temp_file_path)

    return text

# Save content and generate changes
def compare_and_save(link, new_content, is_pdf = False, is_excel = False):
    if is_pdf:
        meaningful_text = extract_text_from_pdf(link)
    else:
        meaningful_text = extract_meaningful_text(new_content)
        
    hashed_filename = hashlib.md5(link.encode()).hexdigest() + ".txt"
    filepath = os.path.join(BASE_DIR, hashed_filename)
    changes_filepath = os.path.join(CHANGES_DIR, hashed_filename + "_changes")

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    if not os.path.exists(CHANGES_DIR):
        os.makedirs(CHANGES_DIR)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            old_content = file.read()
            if old_content != meaningful_text:
                print(f"# Changes detected in {link}. Saving changes to {changes_filepath}\n")
                changes = list(unified_diff(
                    old_content.splitlines(),
                    meaningful_text.splitlines(),
                    fromfile='Old Content',
                    tofile='New Content',
                    lineterm=''
                ))
                with open(changes_filepath, "w", encoding="utf-8") as change_file:
                    change_file.write("\n".join(changes))

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(meaningful_text)