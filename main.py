from crawler import scrape_links

if __name__ == "__main__":
    print("Type your domain: ")
    domain = input("> ").strip()
    print("\nEnter depth: ")
    DEPTH_LIMIT = input("(Default 1)> ").strip()
    DEPTH_LIMIT = int(DEPTH_LIMIT) if DEPTH_LIMIT else 1
    scrape_links(domain, 0, DEPTH_LIMIT=DEPTH_LIMIT)
    print("Scraping completed!")