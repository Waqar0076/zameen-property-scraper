**Zameen Property Scraper**

A Python-based web scraping project for extracting real-estate property listings from Zameen.com using Sync Playwright.

The project currently targets DHA City Karachi and extracts useful property information such as title, price, location, bedrooms, bathrooms, area, description, and listing URL.

🚀 **Features**
Dynamic web scraping using Sync Playwright
Property title extraction
Price extraction
Location extraction
Bedrooms and bathrooms extraction
Property area extraction
Description extraction
Listing URL extraction
Text cleaning and normalization
CSV data export

**🛠️ Technologies Used**
Python
Sync Playwright
NumPy
Pandas
Requests
CSV
Regular Expressions

**📁 Project Structure**
zameen-property-scraper/
│
├── step1_inspect.py
├── step2_scrape.py
├── zameen_dha_city_karachi.csv
├── requirements.txt
└── README.md

**step1_inspect.py**

Used to inspect the HTML structure of the Zameen.com page and identify the selectors required for scraping.

**step2_scrape.py**

Performs the actual property listing extraction and saves the collected data into a CSV file.

** Installation**
**1. Clone the repository**
git clone https://github.com/YOUR-USERNAME/zameen-property-scraper.git
cd zameen-property-scraper

**2. Create a virtual environment**
python -m venv venv

**3. Activate the virtual environment**

**Windows**:

venv\Scripts\activate

**macOS / Linux:**

source venv/bin/activate

**4. Install dependencies**
pip install playwright pandas numpy requests

**5. Install Chromium**
playwright install chromium

**▶️ How to Run**
Step 1 — Inspect the page

**Run:**

python step1_inspect.py

Use the output to identify the actual HTML selectors used by the property listings.

**Step 2 — Run the scraper**

After confirming the selectors, run:

python step2_scrape.py

The scraped data will be saved to:

zameen_dha_city_karachi.csv

**📊 Data Collected**
Field	Description
title	Property listing title
price	Property asking price
location	Property location
beds	Number of bedrooms
baths	Number of bathrooms
area	Property area
description	Property description
url	Property listing URL
🔧 Selector Configuration

The scraper contains several sections marked:

The step1_inspect.py script helps identify the correct selectors before running the scraper.

**📄 Output**
The scraper generates:

zameen_dha_city_karachi.csv

The CSV file contains structured property listing data that can be further analyzed using Pandas, NumPy, Excel, Power BI, or other data-analysis tools.

🔮 Future Improvements
 Pagination support
 Multi-page scraping
 Duplicate listing detection
 Better error handling
 Database storage
 Pandas data analysis
 Price analysis and visualization
 Configurable search locations
 Excel export
 Automated scheduled scraping

**Waqar Aamir
If you found this project useful, feel free to ⭐ star the repository and explore the code.**_I_
