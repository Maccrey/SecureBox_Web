"""Business 상시 암호화 보관함+PC 원격 잠금 TDD 계약."""
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding="utf-8")
class VaultContract(unittest.TestCase):
    def test_home_and_details(self):
        for term in ("상시 암호화", "PC 원격 잠금", "키 접근 차단"):
            self.assertIn(term, read("index.html")+read("features.html"))
        self.assertIn("생체 인증",read("features.html"))
        self.assertIn("관리자 승인",read("features.html"))
    def test_comics_pricing_security(self):
        self.assertIn("comic-bubble",read("stories.html"))
        self.assertIn("상시 암호화 보관함",read("stories.html"))
        self.assertIn("원격 잠금",read("pricing.html"))
        for term in ("오프라인", "기존 키","평문","모바일","PC"):
            self.assertIn(term,read("security.html"))
    def test_no_vendor_or_premature_release(self):
        for p in ("index.html","features.html","stories.html","pricing.html","security.html"):
            for token in ("Firebase","Polar","Firestore","Cloud KMS"):
                self.assertNotIn(token,read(p))
            self.assertIn("예정",read(p))
if __name__=="__main__":unittest.main()
