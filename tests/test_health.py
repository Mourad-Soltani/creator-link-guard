# tests/test_health.py
# Signature: Mourad.Soltani

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import check_link, extract_urls, is_affiliate_like

class TestCreatorLinkGuard(unittest.TestCase):
    def test_extract_urls(self):
        text = "Check this https://example.com and http://test.org/page"
        urls = extract_urls(text)
        self.assertIn('https://example.com', urls)
        self.assertIn('http://test.org/page', urls)

    def test_is_affiliate_like(self):
        self.assertTrue(is_affiliate_like('https://amazon.com/dp/123?tag=foo-20'))
        self.assertFalse(is_affiliate_like('https://example.com'))

    @patch('main.requests.head')
    def test_check_link_ok(self, mock_head):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.url = 'https://example.com'
        mock_head.return_value = mock_resp
        result = check_link('https://example.com')
        self.assertTrue(result['ok'])
        self.assertEqual(result['status'], 200)

    @patch('main.requests.head')
    def test_check_link_fail(self, mock_head):
        mock_head.side_effect = Exception('Timeout')
        result = check_link('https://bad.com')
        self.assertFalse(result['ok'])
        self.assertIsNotNone(result['error'])

if __name__ == '__main__':
    unittest.main()
