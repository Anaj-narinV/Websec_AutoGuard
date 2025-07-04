import logging
import argparse
import json

from scanner import Scanner
from form_parser import FormParser
from vulnerability_detector import VulnerabilityDetector
from report_generator import ReportGenerator

# ----------------------------
# Set up logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("websec_autoguard.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ----------------------------
# Set up CLI argument parser
# ----------------------------
parser = argparse.ArgumentParser(description="WebSec AutoGuard CLI")

parser.add_argument('--url', help='Target URL to scan')
parser.add_argument('--output', help='PDF output filename')
parser.add_argument('--scan-xss', action='store_true', help='Enable XSS scan')
parser.add_argument('--scan-sql', action='store_true', help='Enable SQL injection scan')
parser.add_argument('--config', help='Path to config.json')
parser.add_argument('--threads', type=int, default=5, help='Number of concurrent threads')

# New auth arguments
parser.add_argument('--login-url', help='Login URL for form-based login')
parser.add_argument('--username', help='Username for login')
parser.add_argument('--password', help='Password for login')

args = parser.parse_args()

# ----------------------------
# Load config.json if provided
# ----------------------------
if args.config:
    try:
        with open(args.config, 'r') as f:
            config_data = json.load(f)
            args.url = args.url or config_data.get('url')
            args.output = args.output or config_data.get('output')
            args.scan_xss = args.scan_xss or config_data.get('scan_xss')
            args.scan_sql = args.scan_sql or config_data.get('scan_sql')
            args.threads = args.threads or config_data.get('threads', 5)
            args.login_url = args.login_url or config_data.get('login_url')
            args.username = args.username or config_data.get('username')
            args.password = args.password or config_data.get('password')
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        exit(1)

# ----------------------------
# Main Execution Logic
# ----------------------------
if __name__ == "__main__":
    if not args.url:
        logger.error("No URL provided. Use --url or --config.")
        exit(1)

    logger.info("Starting WebSec AutoGuard...")

    scanner = Scanner()
    parser_module = FormParser()
    detector = VulnerabilityDetector()
    reporter = ReportGenerator()

    # Perform login if credentials are provided
    if args.login_url and args.username and args.password:
        scanner.login(args.login_url, args.username, args.password)

    html = scanner.scan(args.url, max_threads=args.threads)
    forms = parser_module.parse(html)

    findings = []

    if args.scan_xss:
        findings.extend(detector.detect(forms))

    output_filename = args.output or "WebSec_Report1.pdf"
    reporter.generate(findings, filename=output_filename)

    logger.info("Scan completed successfully.")
