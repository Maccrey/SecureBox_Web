"""수신자 .sec 열기·설치 안내 홍보 계약 (실패 테스트 선행)."""
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","stories.html","pricing.html","security.html")
def read(path): return (ROOT/path).read_text(encoding="utf-8")

class RecipientOnboardingContract(unittest.TestCase):
    def test_name_examples(self):
        for page in ("features.html","security.html"):
            self.assertIn("SecureBox.md",read(page))
            self.assertIn("SecureBox.sec",read(page))
            self.assertNotIn("kill.md",read(page))
            self.assertNotIn("kill.sec",read(page))
    def test_receiver_help_is_standalone(self):
        help_page=read("open-sec.html")
        for term in ("SecureBox.sec","Windows","macOS","Android","iOS","설치","무료","복호화","출시 예정","파일을 보관"):
            self.assertIn(term,help_page)
        for name in ("Firebase","Polar","Firestore","Cloud KMS"):
            self.assertNotIn(name,help_page)
        self.assertNotIn('href="#"',help_page)
    def test_link_from_existing_pages(self):
        for page in ("index.html","features.html","stories.html","security.html"):
            with self.subTest(page=page):
                self.assertIn('href="./open-sec.html"',read(page))
    def test_share_guidance(self):
        page=read("features.html")
        self.assertIn("설치 안내",page)
        self.assertIn(".sec",page)
        self.assertIn("수신자",page)
    def test_styles_and_site(self):
        self.assertIn('href="./styles.css"',read("open-sec.html"))
        self.assertIn('href="./favicon.svg',read("open-sec.html"))
        self.assertIn('href="./pricing.html"',read("open-sec.html"))
        self.assertIn('href="./open-sec.html"',read("open-sec.html"))

if __name__=="__main__": unittest.main()
