"""구매 설득형 메뉴 순서와 전 페이지 동일 로고 계약."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","incidents.html","features.html","stories.html","pricing.html","security.html","open-sec.html")
ORDER=("제품 소개","사고 사례","주요 기능","활용 사례","요금제","보안 안내","SEC 파일 열기")

def read(p): return (ROOT/p).read_text(encoding="utf-8")

class HeaderFlowContract(unittest.TestCase):
    def test_menu_order(self):
        for page in PAGES:
            with self.subTest(page=page):
                html=read(page)
                nav=re.search(r'<nav aria-label="주 메뉴" class="nav-links" id="nav-links">([\s\S]*?)</nav>',html)
                self.assertIsNotNone(nav)
                body=nav.group(1)
                positions=[body.index(label) for label in ORDER]
                self.assertEqual(positions,sorted(positions))
                self.assertEqual(body.count('aria-current="page"'),1)

    def test_header_logo_markup_is_identical(self):
        brands=[]
        for page in PAGES:
            html=read(page)
            brand=re.search(r'<a aria-label="SecureBox 홈" class="brand brand-header"[\s\S]*?</a>',html)
            self.assertIsNotNone(brand)
            brands.append(brand.group(0))
        self.assertEqual(len(set(brands)),1)

if __name__=="__main__": unittest.main()
