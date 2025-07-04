from flask import Flask, render_template, request
from scanner import Scanner
from form_parser import FormParser
from vulnerability_detector import VulnerabilityDetector
from report_generator import ReportGenerator

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    scan_xss = 'scan_xss' in request.form

    scanner = Scanner()
    parser = FormParser()
    detector = VulnerabilityDetector()
    reporter = ReportGenerator()

    html = scanner.scan(url)
    forms = parser.parse(html)
    findings = []

    if scan_xss:
        findings = detector.detect(forms)

    reporter.generate(findings, filename="WebSec_Report.pdf")

    return render_template('result.html', findings=findings, url=url)

if __name__ == '__main__':
    app.run(debug=True)
