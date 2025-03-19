import scrapy

class WeddingSpotSpider(scrapy.Spider):
    # Name of the spider
    name = "wedding_spot"
    allowed_domains = ["wedding-spot.com"]
    
    # Starting URL for scraping  ----data extraction for diffrent  pages using page=1,2,3,4,5 
    start_urls = ["https://www.wedding-spot.com/wedding-venues/?page=1&pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1"]
    
    # Custom settings for user agent and download delay
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "DOWNLOAD_DELAY": 2,
    }
    #controling pages links  using functions 
    def parse(self, response):
        """Extracts venue links from listing pages and navigates to each venue page"""
        venue_links = response.css("a[href*='/venue/']::attr(href)").getall()

        for link in venue_links:
            yield response.follow(link, callback=self.parse_venue)

        # Handle pagination to scrape multiple pages
        next_page = response.css("a.pagination__next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_venue(self, response):
        """Extracts details from the venue's main page"""
        
        # Extract venue name
        venue_name = response.css("h1::text").get(default="").strip()
        venue_url = response.url

        # Extract phone number from 'tel:' links
        phone = response.css("a[href^='tel:']::attr(href)").re_first(r"tel:(.*)")

        # Extract venue highlights
        venue_highlights = response.css("div.VenueHighlights--label::text").getall()
        venue_highlights = [vh.strip() for vh in venue_highlights if vh.strip()]

        # Extract guest capacity if available
        guest_capacity = response.css("p.VenuePage--detail-description::text").re_first(r"Accommodates up to (\d+) guests")
        guest_capacity = f"Accommodates up to {guest_capacity} guests" if guest_capacity else "N/A"

        # Extract venue address
        address_line_1 = response.xpath("//p[contains(@class, 'VenuePage--detail-description')]/text()").get()
        address_line_2 = response.xpath("//p[contains(@class, 'VenuePage--detail-description')]/span/text()").get()

        if address_line_1 and address_line_2:
            address = f"{address_line_1.strip()}, {address_line_2.strip()}"
        elif address_line_1:
            address = address_line_1.strip()
        elif address_line_2:
            address = address_line_2.strip()
        else:
            address = "N/A"

        # Return extracted data as a dictionary
        yield {
            "Url": venue_url,
            "Venue Name": venue_name,
            "Phone": phone if phone else "N/A",
            "Venue Highlights": venue_highlights if venue_highlights else ["N/A"],
            "Guest Capacity": guest_capacity,
            "Address": address,
        }
