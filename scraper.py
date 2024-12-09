import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import spacy
from difflib import unified_diff

DIR = "content.txt"
CHANGES = "changes.txt"
nlp = spacy.load("en_core_web_md")

def scrape_link(link):
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    html = ""

    try:
        driver.get(link)
        html = driver.page_source
    finally:
        driver.quit()

    return html

def get_body_content(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    if body:
        return str(body)
    else:
        return ""
    
def clean_html(html):
    soup = BeautifulSoup(html, 'lxml')

    for script in soup(["script", "style"]):
        script.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_content(content, max_length=6000):
    return [
        content[i: i + max_length] for i in range(0, len(content), max_length)
    ]

def extract_meaningful_text(text):
    doc = nlp(text)
    return "\n\n".join([sent.text.strip() for sent in doc.sents])



print("Scraping...")
result = scrape_link("https://chirix.netlify.app")
content = get_body_content(result)
cleaned_content = clean_html(content)
meaningful_text = extract_meaningful_text(cleaned_content)

with open(DIR, "r", encoding="utf-8") as file:
    old_content = file.read()
    if old_content != meaningful_text:
        print("Changes detected!")
        changes = list(unified_diff(
            old_content.splitlines(),
            meaningful_text.splitlines(),
            fromfile='Old Content',
            tofile='New Content',
            lineterm=''
        ))
        with open(CHANGES, "w", encoding="utf-8") as change_file:
            change_file.write("\n".join(changes))
    else:
        print("No changes detected!")

print("Scraping done!")