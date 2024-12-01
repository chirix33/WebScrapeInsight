import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from parse import parse_with_ollama

DIR = "temp_files/source_code1.txt"


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


print("Scraping...")
result = scrape_link("https://blog.val.town/blog/building-a-code-writing-robot")
content = get_body_content(result)
cleaned_content = clean_html(content)
# robust_content = parse_with_ollama(split_content(cleaned_content))

with open(DIR, "w", encoding="utf-8") as file:
    file.write(cleaned_content)
    file.write("\n\n")

print("Scraping done!")