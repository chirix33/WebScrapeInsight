# WebScrapeInsight

**WebScrapeInsight** is a Python-based web scraper designed to capture and compare changes on a website over time. It utilizes custom headers and proxy settings to avoid blocks, and allows the user to specify the depth of the scraping. The tool also saves discovered URLs, stores retrieved content, and keeps track of content differences between scrapes.

## Features

- Scrapes a website recursively with user-specified depth.
- Supports custom user agents and proxy settings.
- Compares and stores content changes in separate files.
- Logs discovered links, including parent-child relationships.
- Uses retry mechanism with delays to handle failed requests.

## Getting Started

These instructions will help you set up and run **WebScrapeInsight** on your local machine.

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `python-dotenv`

### Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/yourusername/WebScrapeInsight.git
    cd WebScrapeInsight

2.  Create a .env file in your root folder and save the proxy settings:
    ```sh
    PROXY_HOST=your_proxy_host:your_proxy_port
    PROXY_USERNAME=your_proxy_username
    PROXY_PASSWORD=your_proxy_password

3.  python scrape.py


Let me know if you need help setting this up or if you have any other questions!