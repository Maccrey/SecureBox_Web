"""로고 v2 회귀: 열린 자물쇠→SecBox.sec→빛→잠긴 자물쇠."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class BrandAnimationV2(unittest.TestCase):
 def test_initial_open_lock(self):
  html=read("index.html").split("</header>",1)[0]
  css=read("styles.css").replace(" ","")
  self.assertIn("brand-open-shackle",html)
  self.assertIn(".brand-open-shackle{opacity:1",css)
  self.assertIn("rotate(-13deg)",css)
 def test_middle_secbox_and_glow(self):
  html=read("index.html").split("</header>",1)[0]
  css=read("styles.css")
  self.assertIn('class="brand-extension"',html)
  self.assertIn('class="brand-extension">.sec',html)
  self.assertIn("@keyframes brandGlowClean",css)
 def test_final_only_lock_and_reduced_motion(self):
  css=read("styles.css").replace(" ","")
  self.assertIn(".brand-header.is-brand-final{gap:0!important;width:34px!important",css)
  self.assertIn(".brand-header.is-brand-final.brand-text-stage{display:none!important}",css)
  block=css.split("@media(prefers-reduced-motion:reduce)",1)[1]
  self.assertIn(".brand-final-lock-glyph{opacity:1",block)
if __name__=="__main__":unittest.main()
