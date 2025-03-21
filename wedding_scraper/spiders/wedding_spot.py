import scrapy


class WeddingSpotSpider(scrapy.Spider):
    name = "wedding_spot"
    allowed_domains = ["wedding-spot.com"]

    start_urls =["https://www.wedding-spot.com/wedding-venues/?page=2&pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response):
        """Extract venue links from listing pages and navigate to each venue"""
        venue_links = response.css("a[href*='/venue/']::attr(href)").getall()

        for link in venue_links:
            yield response.follow(link, callback=self.parse_venue)

        # Handle pagination
        next_page = response.css("a.pagination__next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_venue(self, response):
        """Extract details from the venue's main page"""
        venue_name = response.css("h1::text").get(default="").strip()
        venue_url = response.url

        phone = response.css("a[href^='tel:']::attr(href)").re_first(r"tel:(.*)")

# Extract highlights and remove duplicates while keeping order
        venue_highlights = response.css("div.VenueHighlights--label::text").getall()
        venue_highlights = list(dict.fromkeys([vh.strip() for vh in venue_highlights if vh.strip()]))


        # Extract only the address from "VenuePage--detail-description"
        address_section = response.xpath(
            "//h3[contains(text(),'Location')]/following-sibling::p"
        ).get()

        if address_section:
            address_lines = response.xpath(
                "//h3[contains(text(),'Location')]/following-sibling::p/text() | //h3[contains(text(),'Location')]/following-sibling::p/span/text()"
            ).getall()
            address = " ".join([line.strip() for line in address_lines if line.strip()])
        else:
            address = "N/A"

        # Extract guest capacity correctly
        guest_capacity = response.css("p.VenuePage--detail-description::text").re_first(r"Accommodates up to (\d+) guests")
        guest_capacity = f"{guest_capacity} " if guest_capacity else "N/A"

        yield {
            "Url": venue_url,
            "Venue Name": venue_name,
            "Phone": phone if phone else "N/A",
            "Venue Highlights": venue_highlights if venue_highlights else ["N/A"],
            "Guest Capacity": guest_capacity,
            "Address": address,
        }
