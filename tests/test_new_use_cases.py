"""새 활용 사례와 불필요한 안내문 제거 계약."""
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")

class StoriesExpansionTest(unittest.TestCase):
    def test_comics_include_recent_features(self):
        content=read("stories.html")
        for keyword in ("EPISODE 08","EPISODE 09","EPISODE 10","복호화 이력","파일별 자물쇠","일괄 비허용","가입자 ID","수신 알림","kill.md","kill.sec"):
            self.assertIn(keyword,content)
        self.assertEqual(content.count('class="comic-episode"'),10)
        self.assertIn("10개의 이야기를 보여드립니다.",content)

    def test_remove_requested_footer_note(self):
        content=read("stories.html")
        self.assertNotIn("만화 삽화에는 글자가 없습니다.",content)
        self.assertNotIn("상황·대사·해결 방법·주의사항은 바로 아래 텍스트 컨테이너에 표시합니다.",content)
        self.assertNotIn('class="comic-footnote"',content)

    def test_text_is_in_containers(self):
        content=read("stories.html")
        self.assertEqual(content.count('class="comic-copy"'),10)
        self.assertEqual(content.count('class="comic-caveat"'),10)
        self.assertNotIn("Firebase",content)
        self.assertNotIn("Firestore",content)

if __name__=="__main__":unittest.main()
