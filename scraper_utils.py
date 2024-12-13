import os
import json
from urllib.parse import urlparse
import time
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
JSON_DIR = "json_files"

# Extract Meaningful Text from HTML
def get_body_content(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    if body:
        return str(body)
    else:
        return ""
    
def extract_meaningful_text(html):
    body = get_body_content(html)
    soup = BeautifulSoup(body, 'lxml')
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text(separator="\n")
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
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
        text += page.get_text()
    doc.close()
    os.remove(temp_file_path)

    return text

# Save content and generate changes
def compare_and_save(link, parent_url, new_content, is_pdf = False, is_excel = False):
    if is_pdf:
        meaningful_text = extract_text_from_pdf(link)
    else:
        meaningful_text = extract_meaningful_text(new_content)

    # Calculate the hash of the new content
    new_content_hash = hashlib.md5(meaningful_text.encode()).hexdigest()

    hashed_filename = hashlib.md5(link.encode()).hexdigest() + ".txt"
    filepath = os.path.join(BASE_DIR, hashed_filename)
    changes_filepath = os.path.join(CHANGES_DIR, hashed_filename + "_changes")
    changes = list()

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    if not os.path.exists(CHANGES_DIR):
        os.makedirs(CHANGES_DIR)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            old_content = file.read()
            # Calculate the hash of the old content
            old_content_hash = hashlib.md5(old_content.encode()).hexdigest()

            if old_content_hash != new_content_hash:
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
    
    if len(changes) > 0:
        update_scrape_record(link, link, parent_url, filepath, changes_filepath)
    else:
        update_scrape_record(link, link, parent_url, filepath)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(meaningful_text)

# Function to Get JSON Data
def get_json_data(domain):
    domain = urlparse(domain).netloc + ".json"
    domain = os.path.join(JSON_DIR, domain)
    if os.path.exists(domain):
        with open(domain, "r") as readJSON:
            return json.load(readJSON)
    return "{}"

# Function to Update Scrape Date of a URL
def update_scrape_date(domain, url):
    data = get_json_data(domain)
    domain = urlparse(domain).netloc + ".json"
    domain = os.path.join(JSON_DIR, domain)
    try:
        if url in data:
            data[url]["scrape_date"] = time.strftime("%Y-%m-%d")
            with open(domain, "w", encoding="utf-8") as writeFile:
                json.dump(data, writeFile, indent=4)
    except(Exception) as e:
        print(f'Error updating scrape date of {domain}.json: {e}')
        return False
    
    return True


def is_scrape_today(domain, url, updateDate = False):
    domain = urlparse(domain).netloc + ".json"
    domain = os.path.join(JSON_DIR, domain)
    with open(domain, "r", encoding="utf-8") as readJSON:
        data = json.load(readJSON)
        if url in data:
            if data[url]["scrape_date"] == time.strftime("%Y-%m-%d"):
                if updateDate:
                    update_scrape_date(domain, url)
                return True
    return False
        
def update_scrape_record(domain, url, parent_url, content, changes = "N/A"):
    # Construct the JSON file path
    domain = urlparse(domain).netloc + ".json"
    path = os.path.join(JSON_DIR, domain)
    
    # Ensure the JSON directory exists
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    
    # Set default value for parent_url
    if parent_url is None:
        parent_url = "N/A"

    # Load existing data or initialize an empty dictionary
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as readJSON:
            data = json.load(readJSON)
    else:
        data = {}

    # Update the record for the given URL
    data[url] = {
        "parent": parent_url,
        "content": content,
        "changes": changes,
        "scrape_date": time.strftime("%Y-%m-%d")
    }

    # Write the updated data back to the file
    with open(path, "w", encoding="utf-8") as writeFile:
        json.dump(data, writeFile, indent=4)
