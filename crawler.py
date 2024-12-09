import requests
import csv
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from scraper_utils import compare_and_save
from config import get_headers
import os

# Crawler Configuration
DEPTH_LIMIT = 1  # Will be updated by the user input
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
                    # If the day is already in the CSV, don't write it again
                    if row["Domain"] == domain and row["URL"] == url and row["Parent URL"] == parent_url and row["Date Visited"] == time.strftime("%Y-%m-%d"):
                        return  
        writer.writerow({"Domain": domain, "URL": url, "Parent URL": parent_url, "Date Visited": time.strftime("%Y-%m-%d")})
        
# Scrape Links Recursively
def scrape_links(url, depth, parent_url = None, is_pdf = False, is_excel = False):
    if depth + 1 > DEPTH_LIMIT or url in discovered_links:
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

        response = requests.get(url, headers=headers)  # You can add `proxies=proxy` for proxy handling
        response.raise_for_status()
        html_content = response.text
        # Save and compare content
        compare_and_save(url, html_content, is_pdf, is_excel)
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

                # Check if the link is from the same domain and not already discovered
                if parsed_full_url.netloc == urlparse(url).netloc and full_url not in discovered_links:
                    # Check if the link is a PDF
                    if full_url.endswith(PDF_EXTENSION):
                        scrape_links(full_url, depth + 1, url, is_pdf = True)

                    # Check if the link is an Excel file
                    elif full_url.endswith(tuple(EXCEL_EXTENSIONS)):
                        scrape_links(full_url, depth + 1, url, is_excel = True)
                    else:
                        scrape_links(full_url, depth + 1, url)
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error accessing {url}: {e}")
        print("Sleeping for 10 seconds then retrying...")
        time.sleep(10)
        scrape_links(url, depth, parent_url)