import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 🎯 Starting URL (you can change it later)
start_url = "https://books.toscrape.com/"
visited = set()

def get_internal_links(url):
    internal_links = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        domain = urlparse(url).netloc

        for a in soup.find_all("a", href=True):
            full_url = urljoin(url, a['href'])
            if urlparse(full_url).netloc == domain:
                internal_links.add(full_url)
    except:
        pass
    return internal_links

def scan_forms(url):
    print(f"\n🔍 Scanning: {url}")
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")

        if forms:
            print(f"📝 {len(forms)} form(s) found:")
            for i, form in enumerate(forms, 1):
                action = form.get("action", "N/A")
                method = form.get("method", "GET").upper()
                print(f"  ▶ Form {i}: Method={method}, Action={action}")
        else:
            print("❌ No forms found.")
    except Exception as e:
        print(f"⚠ Error: {e}")

# 🌐 Crawl and scan
all_links = get_internal_links(start_url)
all_links.add(start_url)  # Include main page

for link in all_links:
    if link not in visited:
        visited.add(link)
        scan_forms(link)