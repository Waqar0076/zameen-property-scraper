"""
STEP 1: Inspect the page structure.

This script opens the Zameen listings page in a real browser (via Playwright),
waits for listings to load, then prints the HTML of the FIRST listing card.

Why: Zameen's CSS class names are hashed/auto-generated (they change over
time), so instead of guessing selectors, we grab one real card's HTML,
look at it, and pick the correct selectors for Step 2.

SETUP (run once in your terminal):
    pip install playwright
    playwright install chromium

RUN:
    python step1_inspect.py
"""

from playwright.sync_api import sync_playwright

URL = "https://www.zameen.com/Homes/Karachi_DHA_City_Karachi-1429-1.html"


def main():
    with sync_playwright() as p:
        # headless=False so you can SEE the browser open — helpful while learning.
        # Switch to headless=True later once things work, for speed.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        print(f"Opening {URL} ...")
        page.goto(URL, timeout=60000)

        # Give the page time to render listing cards (JS-driven content).
        page.wait_for_timeout(5000)

        # Zameen listing cards are typically <li> or <article> elements inside
        # the results list. This is a broad guess — we'll confirm/adjust after
        # seeing the printed HTML below.
        candidates = page.query_selector_all("li article, article, li")

        print(f"\nFound {len(candidates)} candidate elements.\n")

        if candidates:
            # Print the HTML of a card that looks like a real listing
            # (has a link to /Property/ inside it).
            for el in candidates:
                html = el.inner_html()
                if "/Property/" in html:
                    print("---- FIRST MATCHING LISTING CARD HTML ----\n")
                    print(html[:3000])  # first 3000 chars, enough to see structure
                    print("\n---- END SNIPPET ----")
                    break
        else:
            print("No candidates found — the page structure may differ. "
                  "Try increasing wait_for_timeout, or check if a cookie/consent "
                  "popup is blocking content (see screenshot.png).")

        # Save a screenshot too — useful to visually confirm what loaded.
        page.screenshot(path="page_debug.png", full_page=True)
        print("\nSaved screenshot as page_debug.png")

        browser.close()


if __name__ == "__main__":
    main()
