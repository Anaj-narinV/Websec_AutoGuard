from flask import Flask, render_template, request, redirect, url_for
from scanner import Scanner
from form_parser import FormParser
from vulnerability_detector import VulnerabilityDetector
from report_generator import ReportGenerator
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("websec_autoguard.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')
    scan_xss = request.form.get('scan_xss') == 'on'

    logger.info(f"Received scan request for URL: {url}")

    scanner = Scanner()
    parser = FormParser()
    detector = VulnerabilityDetector()
    reporter = ReportGenerator()

    html = scanner.scan(url)
    forms = parser.parse(html)

    findings = []

    if scan_xss:
        findings.extend(detector.detect(forms))

   
    report_filename = "WebUI_Report.pdf"  # For display
    report_path = "static/WebUI_Report.pdf"  # For saving file
    reporter.generate(findings, filename=report_path)

    return render_template('result.html', url=url, findings=findings, report=report_filename)

if __name__ == '__main__':
    app.run(debug=True)
