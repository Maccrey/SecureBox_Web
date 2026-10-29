"""이전 분실 후 암호화 설계의 재유입 방지 회귀 테스트."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_text(encoding="utf-8")
class LegacyPolicyRegression(unittest.TestCase):
    def test_current_policy_in_public_pages(self):
        for p in ("features.html","stories.html","pricing.html"):
            self.assertIn("상시 암호화",read(p))
            self.assertNotIn("분실 후 원격 암호화 요청</h3>",read(p))
        self.assertIn("PC 원격 잠금",read("features.html"))
    def test_security_disclosure(self):
        for term in ("오프라인","기존 키","평문","MFA","관리자 승인"):
            self.assertIn(term,read("security.html")+read("features.html"))
if __name__=="__main__":unittest.main()
