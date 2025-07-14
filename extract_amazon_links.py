import requests
from bs4 import BeautifulSoup
import re
import sys
import time

def fetch_amazon_links_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if re.search(r"amazon\.[a-z.]+/", href):
                links.add(href)
        return links, soup
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return set(), None

def get_internal_links(soup, base_url):
    internal_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(base_url) and href != base_url:
            internal_links.add(href)
    return internal_links

def crawl_and_extract_amazon_links(start_url):
    visited = set()
    to_visit = set([start_url])
    all_amazon_links = set()
    base_url = start_url.rstrip('/')
    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        print(f"Crawling: {url}")
        amazon_links, soup = fetch_amazon_links_from_url(url)
        all_amazon_links.update(amazon_links)
        visited.add(url)
        if soup:
            internal_links = get_internal_links(soup, base_url)
            to_visit.update(internal_links - visited)
        time.sleep(1)  # be polite to the server
    return all_amazon_links

def save_links(links, filename):
    with open(filename, 'w') as f:
        for link in links:
            f.write(link + '\n')

def main():
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
    else:
        start_url = input("Enter the URL to scrape (e.g., https://quaily.me): ").strip()
    amazon_links = crawl_and_extract_amazon_links(start_url)
    save_links(amazon_links, 'amazon_links.txt')
    print(f"Extracted {len(amazon_links)} Amazon links. Saved to amazon_links.txt.")

if __name__ == "__main__":
    main()
