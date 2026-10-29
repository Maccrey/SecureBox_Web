"""복호화 이력 홍보 정합성과 파비콘 캐시 재발 방지 테스트 (RED 먼저)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "features.html", "stories.html", "pricing.html", "security.html")
ICON_VERSION = "20261029-audit1"

def read(path): return (ROOT / path).read_text(encoding="utf-8")

class MarketingAuditContract(unittest.TestCase):
    def test_features_and_pricing(self):
        features = read("features.html")
        for term in ("복호화 이력", "PC·모바일", "Team", "Business", "제공 예정"):
            self.assertIn(term, features)
        for term in ("복호화 이력", "Team", "Business"):
            self.assertIn(term, read("pricing.html"))
    def test_security_history_bounds(self):
        s = read("security.html")
        for term in ("복호화 요청", "복호화 완료", "복호화 실패", "본인", "관리자", "인터넷", "출시 예정"):
            self.assertIn(term, s)
        self.assertNotIn("Firebase", s)
        self.assertNotIn("Firestore", s)
    def test_favicon_version_and_order(self):
        for path in PAGES:
            with self.subTest(page=path):
                head = read(path).split("</head>", 1)[0]
                ico = head.find('href="./favicon.ico?v=' + ICON_VERSION + '"')
                svg = head.find('href="./favicon.svg?v=' + ICON_VERSION + '"')
                self.assertGreaterEqual(ico, 0)
                self.assertGreater(svg, ico, "SVG는 마지막 선언해 지원 브라우저에서 우선")
                self.assertIn('sizes="any"', head)
        rules = json.loads(read("firebase.json"))
        headers = rules["hosting"]["headers"]
        self.assertTrue(any("favicon" in h["source"] and
            any("no-cache" in x.get("value", "").lower() for x in h["headers"]) for h in headers))
    def test_home_value_proposition(self):
        self.assertIn("복호화 이력", read("index.html"))
    def test_no_technical_vendors_in_public_copy(self):
        for path in PAGES:
            for vendor in ("Firebase", "Firestore", "Cloud KMS", "Polar"):
                self.assertNotIn(vendor, read(path))

if __name__ == "__main__": unittest.main()
