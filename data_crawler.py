import json
import requests
from bs4 import BeautifulSoup

def crawl_data(url):
    """Crawl data from the given URL and return the parsed content."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def extract_links(soup):
    """Extract and return a list of links from a BeautifulSoup object."""
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('/wiki/') and not href.startswith('/wiki/Special:'):
            full_url = f"https://en.wikipedia.org{href}"
            links.append(full_url)
    return links

def crawl_wikipedia(start_url, max_depth=2):
    """Crawl Wikipedia starting from the given URL up to a specified depth."""
    visited = set()
    queue = [(start_url, 0)]

    dataset = []

    count = 0

    while queue:
        url, depth = queue.pop(0)
        if depth > max_depth or url in visited:
            continue

        print(f"Crawling: {url} at depth {depth}")
        visited.add(url)
        soup = crawl_data(url)
        if soup:
            links = extract_links(soup)
            for link in links:
                if link not in visited:
                    queue.append((link, depth + 1))

            count += 1

            # Save the dataset every 100 sites
            if count % 100 == 0:
                with open(f'wikipedia_dataset_{count}.json', 'w', encoding='utf-8') as f:
                    json.dump(dataset, f, ensure_ascii=False, indent=4)
                dataset = []  # Clear the dataset after saving
            page_text = soup.get_text(separator=' ', strip=True)
            dataset.append({'url': url, 'content': page_text})

    # Save any remaining data
    with open(f'wikipedia_dataset_final.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Main_Page"
    crawl_wikipedia(start_url)
