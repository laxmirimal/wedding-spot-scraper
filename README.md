# Wedding Spot Scraper

This project is a web scraper built using Scrapy to extract wedding venue details from [Wedding Spot](https://www.wedding-spot.com/).

## Features
- Scrapes venue details such as name, phone number, highlights, guest capacity, and address.
- Handles pagination to scrape multiple pages.
- Stores data in JSON or CSV format.

## Requirements
Make sure you have the following installed on your system:
- Python (>=3.7)
- Scrapy

## Installation
1. Clone the repository or download the code:
   ```bash
   git clone https://github.com/laxmirimal/wedding-spot-scraper.git
   cd wedding-spot-scraper
   ```

## Scraper Location

The main Python script responsible for scraping data is located in:

-wedding_scraper/spiders/wedding_spot.py


2. Install dependencies:
   ```bash
   pip install scrapy
   ```

## Running the Scraper
To run the scraper and save data in JSON format:
```bash
scrapy crawl wedding_spot -o venues.json
```
To save data in CSV format:
```bash
scrapy crawl wedding_spot -o venues.csv
```

## Viewing Scraped Data
- Open `venues.json` in a text editor to view JSON-formatted data.
- Open `venues.csv` using Excel or any CSV viewer.

## Notes
- The scraper includes a download delay to avoid overloading the server.
- If the structure of the website changes, CSS or XPath selectors may need to be updated.

## Contact
For any issues, reach out via email or GitHub Issues.
-email:laxmirimal2005@gmail.com
-github:https:www.github.com/laxmirimal

