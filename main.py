from crawler import scrape_links

if __name__ == "__main__":
    print("Type your domain: ")
    domain = input("> ")
    print("Enter depth: ")
    DEPTH_LIMIT = int(input("> "))

    scrape_links(domain, 0)
    print("Scraping completed!")

    print("What do you want to ask? ")
    question = input("> ")
