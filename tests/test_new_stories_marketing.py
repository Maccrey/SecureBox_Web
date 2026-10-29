"""홍보 만화 신규 활용사례 및 불필요 안내 문구 제거의 회귀 테스트."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
STORY_IMAGES = (
    "filename-sec.svg",
    "decryption-audit.svg",
    "bulk-lock.svg",
    "secure-id-transfer.svg",
)
HEADINGS = (
    "파일 이름은 익숙하게, 내용은 암호화",
    "누가 열어봤는지 이력으로 확인",
    "자물쇠로 파일별·일괄 접근 제한",
    "가입자 ID로 보내고 수신 알림 받기",
)


class NewStoryContract(unittest.TestCase):
    def test_comics_have_eleven_distinct_cases(self):
        page = (ROOT / "stories.html").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r'<article class="comic-episode"', page)), 11)
        self.assertIn("11편의 만화", page)
        self.assertIn("11개의 이야기를 보여드립니다.", page)
        for n, heading in enumerate(HEADINGS, 8):
            with self.subTest(episode=n):
                self.assertIn(f"EPISODE {n:02}", page)
                self.assertIn(heading, page)
                self.assertIn(f'src="./assets/stories/{STORY_IMAGES[n-8]}"', page)

    def test_exact_requested_footer_paragraph_removed(self):
        page = (ROOT / "stories.html").read_text(encoding="utf-8")
        self.assertNotIn('class="comic-footnote"', page)
        self.assertNotIn("만화 삽화에는 글자가 없습니다.", page)
        self.assertNotIn("이미 발급된 키와 평문 회수, 스마트폰 전체 잠금", page)

    def test_text_free_svg_and_accessible_separate_copy(self):
        page = (ROOT / "stories.html").read_text(encoding="utf-8")
        for image in STORY_IMAGES:
            with self.subTest(image=image):
                root = ET.parse(ROOT / "assets" / "stories" / image).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertFalse(any(n.tag.rsplit("}",1)[-1] in
                       ("text","tspan","foreignObject") for n in root.iter()))
                self.assertIn('class="comic-bubble comic-problem"', page)
                self.assertIn('class="comic-bubble comic-solution"', page)
                self.assertRegex(page, re.escape(image) + r'[^>]*>')
        self.assertIn('data-story-filter="team"', page)
        self.assertIn('data-story-filter="business"', page)

    def test_truthful_security_caveats(self):
        page=(ROOT / "stories.html").read_text(encoding="utf-8")
        for term in ("출시 예정", "이미 복호화", "백그라운드", "앱을 다시", "kill.sec"):
            self.assertIn(term, page)
        for vendor in ("Firebase", "Firestore", "Polar", "Cloud KMS"):
            self.assertNotIn(vendor,page)

    def test_offline_preview_and_docs_updated(self):
        preview=(ROOT/"standalone-preview.html").read_text(encoding="utf-8")
        for term in HEADINGS:
            self.assertIn(term, preview)
        self.assertNotIn("만화 삽화에는 글자가 없습니다.", preview)
        self.assertIn("11개의 이야기를 보여드립니다.",preview)
        self.assertIn("11편", (ROOT/"README.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
