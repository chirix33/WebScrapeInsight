import requests
from bs4 import BeautifulSoup
import spacy

nlp = spacy.load("en_core_web_md")

response = requests.get("https://chirix.netlify.app/")
response.raise_for_status()
html_content = response.text

def get_meaningful_content(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text()

    doc = nlp(text)
    organized_text = "\n\n".join([sent.text.strip() for sent in doc.sents])
    return organized_text

# get_meaningful_content(html_content)
meaningful_content = get_meaningful_content(html_content)
print(meaningful_content)