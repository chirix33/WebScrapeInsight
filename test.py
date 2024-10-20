import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import random
import csv
import hashlib
import time
import pprint
from dotenv import load_dotenv

load_dotenv()

# Get the proxy server using environment variables
host, port  = os.environ.get('PROXY_HOST').split(":")
username = os.environ.get('PROXY_USERNAME')
password = os.environ.get('PROXY_PASSWORD')

proxy_url = f'http://{username}:{password}@{host}:{port}'


# User-specified configurations
HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/127.0.0.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65 Safari/535.11"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Zoom 3.6.0; wbx 1.0.0; cwms 1.0.0; Zoom 3.6.0)"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"},
    {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; ru) Presto/2.9.168 Version/11.50"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/112.0.5197.53"},
]
BASE_DIR = "scraped_content"
DEPTH_LIMIT = 1  # This will be updated by the user input

print("Type your domain: ")
domain = input("> ")
print("Enter depth: ")
DEPTH_LIMIT = int(input("> "))

parsed_base = urlparse(domain)

# To store visited URLs
discovered_links = set()

# Compare and save file if different
def compare_and_save(link, new_content):
    hashed_filename = hashlib.md5(link.encode()).hexdigest() + ".txt"
    filepath = os.path.join(BASE_DIR, hashed_filename)

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            old_content = file.read()
            if old_content != new_content:
                with open(filepath + "_changes", "w") as change_file:
                    change_file.write(f"Changes in {link}\n\n")
                    change_file.write(f"Old Content:\n{old_content}\n\n")
                    change_file.write(f"New Content:\n{new_content}\n")
    with open(filepath, "w") as file:
        file.write(new_content)

# Add URLs to CSV
def save_to_csv(domain, url, parent_url):
    with open("visited_links.csv", "a", newline="") as csvfile:
        fieldnames = ["Domain", "URL", "Parent URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if os.stat("visited_links.csv").st_size == 0:
            writer.writeheader()

        writer.writerow({"Domain": domain, "URL": url, "Parent URL": parent_url})

# Scrape links recursively
def scrape_links(url, depth, parent_url=None):
    if depth > DEPTH_LIMIT or url in discovered_links:
        return

    discovered_links.add(url)

    headers = random.choice(HEADERS_LIST)
    proxy = {"http": proxy_url, "https": proxy_url}

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        response.raise_for_status()
        html_content = response.text

        # Save and compare content
        compare_and_save(url, html_content)
        save_to_csv(parsed_base.netloc, url, parent_url)

        # Find all the links on the page
        soup = BeautifulSoup(html_content, 'lxml')
        all_links = soup.find_all("a", href=True)

        # Recursively scrape each valid link
        for link in all_links:
            href = link.get('href')
            if href:
                # Exclude anchor links
                if href.startswith('#'):
                    continue
                # Construct full URL for relative paths
                full_url = urljoin(url, href)
                parsed_full_url = urlparse(full_url)
                # Only keep links that are from the same domain and have not been visited
                if parsed_full_url.netloc == parsed_base.netloc and full_url not in discovered_links:
                    scrape_links(full_url, depth + 1, url)
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error accessing {url}: {e}")

# Main script
if __name__ == "__main__":
    scrape_links(domain, 0)
    print("Scraping completed!")
