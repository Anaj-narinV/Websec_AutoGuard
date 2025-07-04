import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class FormParser:
    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        forms = soup.find_all('form')
        parsed_forms = []

        for form in forms:
            inputs = form.find_all('input')
            has_csrf = any('csrf' in (inp.get('name') or '').lower() or
                           'token' in (inp.get('name') or '').lower()
                           for inp in inputs)

            if not has_csrf:
                logger.warning("Possible CSRF issue: Form missing CSRF token.")

            parsed_forms.append(form)

        logger.info(f"Total forms extracted: {len(forms)}")
        return parsed_forms
