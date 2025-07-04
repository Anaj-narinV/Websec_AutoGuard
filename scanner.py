import logging
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self):
        self.visited = set()
        self.session = requests.Session()

    def login(self, login_url, username, password):
        try:
            login_data = {
                "username": username,
                "password": password
            }
            response = self.session.post(login_url, data=login_data)
            if response.status_code == 200:
                logger.info("Login successful.")
            else:
                logger.warning(f"Login may have failed. Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Login error: {e}")

    def fetch_url(self, url):
        try:
            response = self.session.get(url)

            # --- Security Header Checks ---
            security_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "Content-Security-Policy"
            ]

            for header in security_headers:
                if header not in response.headers:
                    logger.warning(f"Missing Security Header: {header}")

            # --- Insecure HTTP Check ---
            if url.startswith("http://"):
                logger.warning(f"Insecure connection: URL {url} uses HTTP instead of HTTPS")

            return response.text

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return ""

    def scan(self, url, max_threads=5):
        logger.info(f"Scanning URL: {url}")
        html = self.fetch_url(url)
        return html
