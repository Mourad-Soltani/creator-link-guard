# CreatorLinkGuard
# Signature: Mourad.Soltani

A minimal, shippable CLI micro-tool for solo content creators and YouTubers to quickly check the health of affiliate links in video descriptions or link lists.

## Features
- Extract URLs from text/description
- Check HTTP status and final redirects
- Flag affiliate-like links
- Simple health score
- Zero dependencies beyond requests (stdlib otherwise)

## Usage
```bash
pip install -r requirements.txt
python main.py --text "Check my links: https://amzn.to/abc https://example.com"
# or
python main.py --file description.txt
# or pipe
echo "https://badlink.example" | python main.py
```

## Health Tests
```bash
python -m unittest tests/test_health.py
```

## License
MIT

Built by Mourad.Soltani
