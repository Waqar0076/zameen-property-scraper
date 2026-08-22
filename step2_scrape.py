"""
STEP 2: Extract listing data.

Run this AFTER step1_inspect.py, once we've confirmed the real selectors
from the printed HTML. I've filled in best-guess selectors based on
Zameen's typical markup — you'll likely need to tweak a few after seeing
Step 1's output. Everywhere you might need to adjust is marked "ADJUST ME".

SETUP (if not already done):
    pip install playwright
    playwright install chromium

RUN:
    python step2_scrape.py
"""

import csv
import re
from playwright.sync_api import sync_playwright

URL = "https://www.zameen.com/Homes/Karachi_DHA_City_Karachi-1429-1.html"
OUTPUT_CSV = "zameen_dha_city_karachi.csv"


def clean_text(text):
    """Collapse whitespace/newlines into single spaces."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def scrape_page():
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # set False to watch it work
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        print(f"Opening {URL} ...")
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)  # let JS-rendered listings load

        # ADJUST ME: this selector should match each individual listing "card".
        # From Step 1, pick whatever wrapped a single /Property/ link + price + title.
        cards = page.query_selector_all("li article, article")
        print(f"Found {len(cards)} card elements on the page.")

        for card in cards:
            # Every real listing links to /Property/... — skip ads/new-project cards.
            link_el = card.query_selector("a[href*='/Property/']")
            if not link_el:
                continue

            url = link_el.get_attribute("href")
            if url and url.startswith("/"):
                url = "https://www.zameen.com" + url

            # ADJUST ME: title is usually in an h2/h3 near the link.
            title_el = card.query_selector("h2, h3")
            title = clean_text(title_el.inner_text()) if title_el else ""

            # ADJUST ME: price usually sits in a heading like h4 with "PKR".
            price_el = card.query_selector("h4")
            price = clean_text(price_el.inner_text()) if price_el else ""

            # ADJUST ME: location line — often a <span> right after the price block.
            # We fall back to searching all card text for a plausible location pattern.
            location_el = card.query_selector("[aria-label*='location'], span.location")
            location = clean_text(location_el.inner_text()) if location_el else ""

            # ADJUST ME: beds/baths/area are usually small icon+number groups.
            # Zameen typically lists them in this order: beds, baths, area.
            # We grab all short numeric/unit spans as a fallback.
            info_spans = card.query_selector_all("span")
            beds, baths, area = "", "", ""
            for span in info_spans:
                text = clean_text(span.inner_text())
                if re.match(r"^\d+$", text) and not beds:
                    beds = text
                elif re.match(r"^\d+$", text) and beds and not baths:
                    baths = text
                elif "Sq. Yd." in text or "Sq. Ft." in text or "Marla" in text or "Kanal" in text:
                    area = text

            # ADJUST ME: description is usually a <p> with truncated text ("...more").
            desc_el = card.query_selector("p")
            description = clean_text(desc_el.inner_text()) if desc_el else ""

            listings.append({
                "title": title,
                "price": price,
                "location": location,
                "beds": beds,
                "baths": baths,
                "area": area,
                "description": description,
                "url": url or "",
            })

        browser.close()

    return listings


def save_to_csv(listings, filename):
    if not listings:
        print("No listings scraped — nothing to save.")
        return

    fieldnames = ["title", "price", "location", "beds", "baths", "area", "description", "url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(listings)

    print(f"Saved {len(listings)} listings to {filename}")


if __name__ == "__main__":
    data = scrape_page()
    save_to_csv(data, OUTPUT_CSV)
