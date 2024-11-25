import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service

def scrape_link(link):
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(link)
        return driver.page_source
    finally:
        driver.quit()

result = scrape_link("https://www.amazon.com")