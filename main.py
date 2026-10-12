# CreatorLinkGuard
# Signature: Mourad.Soltani
# A minimal CLI tool for solo content creators to check the health of affiliate links in descriptions or lists.
# Realistic micro-SaaS: one-time purchase or freemium for bulk checks.

import argparse
import requests
import sys
from urllib.parse import urlparse
import re

AFFILIATE_PATTERNS = [
    r'amazon\.com.*tag=',
    r'amzn\.to',
    r'bit\.ly',
    r'go\.aff',
    r'affiliate',
    r'ref=',
    r'aff=',
]

def is_affiliate_like(url):
    for pattern in AFFILIATE_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False

def check_link(url, timeout=10):
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        if response.status_code >= 400:
            response = requests.get(url, allow_redirects=True, timeout=timeout)
        final_url = response.url
        status = response.status_code
        is_ok = 200 <= status < 400
        affiliate = is_affiliate_like(url) or is_affiliate_like(final_url)
        return {
            'original': url,
            'final': final_url,
            'status': status,
            'ok': is_ok,
            'affiliate_like': affiliate,
            'error': None
        }
    except Exception as e:
        return {
            'original': url,
            'final': None,
            'status': None,
            'ok': False,
            'affiliate_like': is_affiliate_like(url),
            'error': str(e)
        }

def extract_urls(text):
    url_pattern = re.compile(r'https?://[^\s<>"\']+')
    return url_pattern.findall(text)

def main():
    parser = argparse.ArgumentParser(description='CreatorLinkGuard: Check affiliate link health for creators. Mourad.Soltani')
    parser.add_argument('--file', type=str, help='File containing URLs or description text')
    parser.add_argument('--text', type=str, help='Direct text input')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        content = sys.stdin.read()

    urls = extract_urls(content)
    if not urls:
        print("No URLs found.")
        return

    results = [check_link(url) for url in urls]
    ok_count = sum(1 for r in results if r['ok'])
    aff_count = sum(1 for r in results if r['affiliate_like'])
    health = (ok_count / len(results)) * 100 if results else 0

    print(f"Checked {len(results)} links. Health score: {health:.1f}%")
    print(f"Affiliate-like: {aff_count}")
    for r in results:
        status_str = f"OK ({r['status']})" if r['ok'] else f"FAIL ({r['status'] or r['error']})"
        print(f"- {r['original']} -> {status_str} {'[AFF]' if r['affiliate_like'] else ''}")

if __name__ == '__main__':
    main()
