import os
import hashlib
from bs4 import BeautifulSoup
import spacy
from difflib import unified_diff

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

# Save content and generate changes
def compare_and_save(link, new_content):
    meaningful_text = extract_meaningful_text(new_content)
    hashed_filename = hashlib.md5(link.encode()).hexdigest() + ".txt"
    filepath = os.path.join(BASE_DIR, hashed_filename)
    changes_filepath = os.path.join(CHANGES_DIR, hashed_filename + "_changes")

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    if not os.path.exists(CHANGES_DIR):
        os.makedirs(CHANGES_DIR)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            old_content = file.read()
            if old_content != meaningful_text:
                changes = list(unified_diff(
                    old_content.splitlines(),
                    meaningful_text.splitlines(),
                    fromfile='Old Content',
                    tofile='New Content',
                    lineterm=''
                ))
                with open(changes_filepath, "w") as change_file:
                    change_file.write("\n".join(changes))

    with open(filepath, "w") as file:
        file.write(meaningful_text)