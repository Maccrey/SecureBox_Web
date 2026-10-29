"""헤더 로고 애니메이션 계약: 열린 자물쇠로 시작해 닫힌 자물쇠만 남는다."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","incidents.html","stories.html","pricing.html","security.html","open-sec.html")
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class BrandAnimationContract(unittest.TestCase):
 def test_all_pages_have_animated_header(self):
  for p in PAGES:
   s=read(p)
   self.assertIn('class="brand brand-header"',s,p)
   self.assertIn("brand-open-shackle",s,p)
   self.assertIn("brand-final-lock-glyph",s,p)
   self.assertIn("brand-full-name",s,p)
   self.assertIn("brand-sec-name",s,p)
 def test_first_and_middle_copy(self):
  s=read("index.html")
  self.assertIn(">SecureBox<span",s)
  self.assertIn(">SecBox</span><span class=\"brand-ext\">.sec</span>",s)
 def test_css_sequence_and_final_state(self):
  s=read("styles.css")
  for term in ("brandOpenShackleClean","brandFullNameClean","brandSecNameClean","brandGlowClean","brandFinalLockClean",".brand-header.is-brand-final .brand-text-stage"):
   self.assertIn(term,s)
  self.assertIn("display:none!important",s)
 def test_js_latches_final_lock(self):
  s=read("script.js")
  self.assertIn("is-brand-final",s)
  self.assertIn("brandFinalLockClean",s)
if __name__=="__main__": unittest.main()
