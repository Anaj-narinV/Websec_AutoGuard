import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from fpdf import FPDF

start_url = "https://books.toscrape.com/"
visited = set()

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Vulnerability Scan Report", ln=1, align='C')

    def add_link_entry(self, url, forms):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"\nURL: {url}", ln=1)
        if forms:
            self.set_font("Arial", "", 11)
            for i, f in enumerate(forms, 1):
                self.multi_cell(0, 8, f"  Form {i}: Method = {f['method']}, Action = {f['action']}")
        else:
            self.set_font("Arial", "I", 11)
            self.cell(0, 8, "  No forms found", ln=1)

def get_internal_links(url):
    links = set()
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        domain = urlparse(url).netloc

        for a in soup.find_all("a", href=True):
            full_url = urljoin(url, a['href'])
            if urlparse(full_url).netloc == domain:
                links.add(full_url)
    except:
        pass
    return links

def scan_forms(url):
    forms = []
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        for form in soup.find_all("form"):
            action = form.get("action", "N/A")
            method = form.get("method", "GET").upper()
            forms.append({"action": action, "method": method})
    except:
        pass
    return forms

#  Crawl and collect
all_links = get_internal_links(start_url)
all_links.add(start_url)

pdf = PDFReport()
pdf.add_page()

for link in all_links:
    if link not in visited:
        visited.add(link)
        forms = scan_forms(link)
        pdf.add_link_entry(link, forms)

# Save report
pdf.output("scan_report.pdf")
print("PDF report 'scan_report.pdf' created successfully.")