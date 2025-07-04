import requests
from bs4 import BeautifulSoup

def extract_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.find_all("form")
    
    print(f"Found {len(forms)} forms on {url}")
    for form in forms:
        print(form)
url = "http://testphp.vulnweb.com"
extract_forms(url)