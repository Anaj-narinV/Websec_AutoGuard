import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ==== Check if a link is internal ====
def is_internal_link(base_url, link):
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(link).netloc
    return link_domain == '' or base_domain == link_domain

# ==== Web crawler function ====
def crawl_website(start_url, visited=None):
    if visited is None:
        visited = set()

    try:
        response = requests.get(start_url, timeout=10)  # Increased timeout
        print(f"Status code: {response.status_code}")  
    except requests.RequestException as e:
        print(f"Error accessing {start_url}: {e}")  
        return visited

    if response.status_code != 200:
        print(f"Failed to load page: {start_url}")
        return visited

    soup = BeautifulSoup(response.text, 'html.parser')
    print(f" Page loaded: {start_url}")

    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(start_url, href).split('#')[0]  

        if full_url not in visited and is_internal_link(start_url, full_url):
            visited.add(full_url)
            print(f" Visited: {full_url}")
            crawl_website(full_url, visited)

    return visited

# ==== Start crawling ====
if __name__ == "__main__":
    start_url ="http://testphp.vulnweb.com/" 
    found_links = crawl_website(start_url)
    print(f"\n Total internal links found: {len(found_links)}")
