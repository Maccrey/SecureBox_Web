"""활용 사례 추가 및 안내 문단 삭제 회귀 테스트."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class StoryContract(unittest.TestCase):
 def test_latest_examples(self):
  s=read("stories.html")
  for phrase in ("EPISODE 08","EPISODE 09","EPISODE 10","복호화 이력","일괄 비허용","가입자 ID","수신 알림","백그라운드"):
   self.assertIn(phrase,s)
 def test_no_footnote(self):
  s=read("stories.html")
  self.assertNotIn("만화 삽화에는 글자가 없습니다.",s)
  self.assertNotIn('class="comic-footnote"',s)
 def test_case_count(self):
  s=read("stories.html")
  self.assertEqual(s.count('class="comic-episode"'),10)
  self.assertIn("10개의 이야기를 보여드립니다.",s)
 def test_illustration_and_text_separate(self):
  s=read("stories.html")
  self.assertEqual(s.count('class="comic-copy"'),10)
  self.assertEqual(s.count('class="comic-art'),10)
if __name__=="__main__":unittest.main()
