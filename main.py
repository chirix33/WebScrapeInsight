from crawler import scrape_links

if __name__ == "__main__":
    print("Type your domain: ")
    domain = input("> ").strip()
    print("Enter depth: ")
    DEPTH_LIMIT = int(input("> "))

    scrape_links(domain, 0, DEPTH_LIMIT=DEPTH_LIMIT)
    print("Scraping completed!")