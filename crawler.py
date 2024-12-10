import requests
import csv
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from scraper_utils import compare_and_save
from config import get_headers
import os

PDF_EXTENSION = ".pdf"
EXCEL_EXTENSIONS = [".xlsx", ".xls"]

discovered_links = set()
depth_list = []

# Add URLs to CSV
def save_to_csv(domain, url, parent_url):
    with open("visited_links.csv", "a", newline="") as csvfile:
        fieldnames = ["Domain", "URL", "Parent URL", "Date Visited"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if parent_url is None:
            parent_url = "N/A"

        if os.stat("visited_links.csv").st_size == 0:
            writer.writeheader()
        else:
            with open("visited_links.csv", "r") as readfile:
                reader = csv.DictReader(readfile)
                for row in reader:
                    # Skip if entry already exists for the day
                    if row["Domain"] == domain and row["URL"] == url and row["Parent URL"] == parent_url and row["Date Visited"] == time.strftime("%Y-%m-%d"):
                        return  
        writer.writerow({"Domain": domain, "URL": url, "Parent URL": parent_url, "Date Visited": time.strftime("%Y-%m-%d")})

# Scrape Links Recursively
def scrape_links(url, depth, parent_url=None, is_pdf=False, is_excel=False, DEPTH_LIMIT=1):
    if depth >= DEPTH_LIMIT or url in discovered_links:
        return

    discovered_links.add(url)

    headers = get_headers()
    
    if depth not in depth_list:
        depth_list.append(depth)
        print(f"\n# DEPTH: {depth + 1}")

    try:
        print(f"Scraping {url} from {parent_url}")
        if is_pdf:
            print(f"# Found PDF: {url}")
        elif is_excel:
            print(f"# Found Excel: {url}")

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        # Save and compare content
        compare_and_save(url, parent_url, html_content, is_pdf, is_excel)
        save_to_csv(urlparse(url).netloc, url, parent_url)

        # Find all the links on the page
        soup = BeautifulSoup(html_content, 'lxml')
        all_links = soup.find_all("a", href=True)

        # Recursively scrape each valid link
        for link in all_links:
            href = link.get('href')
            if href:
                # Ignore anchor links
                if href.startswith('#'):
                    continue
                full_url = urljoin(url, href)
                parsed_full_url = urlparse(full_url)

                # Check if the link is from the same domain or localhost
                if (parsed_full_url.netloc == urlparse(url).netloc or 
                    parsed_full_url.netloc in ["localhost", "127.0.0.1"]) and full_url not in discovered_links:
                    # Check for file types
                    if full_url.endswith(PDF_EXTENSION):
                        scrape_links(full_url, depth + 1, url, is_pdf=True, DEPTH_LIMIT=DEPTH_LIMIT)
                    elif full_url.endswith(tuple(EXCEL_EXTENSIONS)):
                        scrape_links(full_url, depth + 1, url, is_excel=True, DEPTH_LIMIT=DEPTH_LIMIT)
                    else:
                        scrape_links(full_url, depth + 1, url, DEPTH_LIMIT=DEPTH_LIMIT)
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error accessing {url}: {e}")
        print("Sleeping for 10 seconds then retrying...")
        time.sleep(10)
        scrape_links(url, depth, parent_url, DEPTH_LIMIT=DEPTH_LIMIT)