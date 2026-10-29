"""원격 분실 암호화 공개 문구 계약: RED → GREEN → REFACTOR (Business 기획 기능)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class RemoteLossMarketingContract(unittest.TestCase):
    def test_remote_command_is_primary_flow(self):
        features = read("features.html")
        self.assertIn("분실 후 원격 암호화", features)
        self.assertIn("Windows/macOS", features)
        self.assertIn("지정 폴더", features)
        self.assertIn("PC에서", features)
        self.assertIn("암호화 완료", features)
        self.assertNotIn("중요 파일은 분실 전에 암호화", features)

    def test_status_is_not_confused_with_delivery(self):
        features = read("features.html")
        for state in ("명령 접수", "기기 수신", "암호화 진행", "암호화 완료"):
            self.assertIn(state, features)
        self.assertIn("완료 확인", features)
        self.assertIn("보장하지", features)

    def test_comic_and_home_match_requested_workflow(self):
        stories = read("stories.html")
        home = read("index.html")
        self.assertIn("원격 암호화 명령", stories)
        self.assertIn("원본 정리", stories)
        self.assertIn("앱이 실행", stories)
        self.assertIn("PC에서 분실 암호화", home)
        self.assertIn("comic-copy", stories)
        self.assertIn("comic-bubble", stories)

    def test_pricing_faq_scope_and_no_vendor_exposure(self):
        pricing = read("pricing.html")
        security = read("security.html")
        self.assertIn("원격 암호화 요청", pricing)
        for term in ("오프라인", "백그라운드", "iOS", "Android", "보장하지"):
            self.assertIn(term, security)
        for page in ("index.html", "features.html", "stories.html", "pricing.html", "security.html"):
            public = read(page)
            for private_term in ("Firebase", "Polar", "Firestore", "Cloud KMS"):
                self.assertNotIn(private_term, public)

    def test_architecture_contract_exists(self):
        contract = read("docs/REMOTE_LOSS_ENCRYPTION_CONTRACT.md")
        for term in ("command_id", "nonce", "expires_at", "서명", "멱등성", "FCM", "APNs",
                     "명령 접수", "기기 수신", "암호화 진행", "암호화 완료", "원본 삭제",
                     "Android", "iOS", "실기기", "TDD"):
            self.assertIn(term, contract)

if __name__ == "__main__":
    unittest.main()
