## Getting Started

These instructions will help you set up and run **WebScrapeInsight** on your local machine.

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `python-dotenv`
  - `numpy`
  - `spacy`
  - `pymupdf`

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/WebScrapeInsight.git
    cd WebScrapeInsight
    ```

2. Install the required Python libraries:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a [`.env`](.env ) file in your root folder and save the proxy settings (optional):
    ```sh
    PROXY_HOST=your_proxy_host:your_proxy_port
    PROXY_USERNAME=your_proxy_username
    PROXY_PASSWORD=your_proxy_password
    ```

### Usage

1. Run the main script:
    ```sh
    python main.py
    ```

2. Follow the prompts to enter the domain and the depth limit for scraping.

### Project Structure

- [`config.py`](config.py ): Contains functions to get proxy settings and headers.
- [`crawler.py`](crawler.py ): Contains the main scraping logic, including recursive link scraping and saving URLs to CSV.
- [`scraper_utils.py`](scraper_utils.py ): Contains utility functions for extracting meaningful text, comparing and saving content, and updating scrape records.
- [`main.py`](main.py ): Entry point of the application, prompts user for input and starts the scraping process.

### Data Storage

- **Scraped Content**: Stored in text files within the `scraped_data` directory.
- **Changes**: Stored in separate text files within the [changes](http://_vscodecontentref_/1) directory.
- **Discovered URLs**: Logged in CSV files within the `logs` directory.
- **Scrape Records**: Stored in JSON files within the `json_data` directory.

### Example

```sh
Type your domain:
> example.com

Enter depth:
(Default 1)> 2