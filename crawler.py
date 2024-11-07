import requests
import csv
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from scraper_utils import compare_and_save
from config import get_proxy, get_headers
import os

# Crawler Configuration
DEPTH_LIMIT = 1  # Will be updated by the user input
discovered_links = set()
depth_list = []

# Add URLs to CSV
def save_to_csv(domain, url, parent_url):
    with open("visited_links.csv", "a", newline="") as csvfile:
        fieldnames = ["Domain", "URL", "Parent URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if os.stat("visited_links.csv").st_size == 0:
            writer.writeheader()

        writer.writerow({"Domain": domain, "URL": url, "Parent URL": parent_url})

# Scrape Links Recursively
def scrape_links(url, depth, parent_url=None):
    if depth > DEPTH_LIMIT or url in discovered_links:
        return

    discovered_links.add(url)

    headers = get_headers()
    proxy = {"http": get_proxy(), "https": get_proxy()}
    
    if depth + 1 not in depth_list:
        depth_list.append(depth + 1)
        print(f"# DEPTH: {depth + 1} \n")

    try:
        print(f"Scraping {url} from {parent_url}")
        response = requests.get(url, headers=headers)  # You can add `proxies=proxy` for proxy handling
        response.raise_for_status()
        html_content = response.text
        # Save and compare content
        compare_and_save(url, html_content)
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
                    scrape_links(full_url, depth + 1, url)
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error accessing {url}: {e}")
        print("Sleeping for 10 seconds then retrying...")
        time.sleep(10)
        scrape_links(url, depth, parent_url)