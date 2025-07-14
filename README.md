# Amazon Link Extractor

This Python script fetches the webpage the user provides (and its internal pages), extracts all Amazon links, and saves them in a .txt file.

## How to Use

1. Make sure you have Python 3 installed.
2. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
3. Run the script:
   ```bash
   python extract_amazon_links.py https://example.com
   ```
   Or, if you don't provide a URL, the script will prompt you to enter one.
4. The extracted Amazon links will be saved in `amazon_links.txt`.
