"""헤더 로고 애니메이션 최신 계약."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","incidents.html","stories.html","pricing.html","security.html","open-sec.html")
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class AnimatedBrandContract(unittest.TestCase):
 def test_header_markup(self):
  for page in PAGES:
   head=read(page).split("</header>",1)[0]
   for term in ("brand-animated","brand-open-shackle","brand-final-lock-glyph","brand-morph","brand-removed","SecBox",".sec"):
    self.assertIn(term,head,page)
 def test_clean_timeline(self):
  css=read("styles.css")
  for term in ("brandRemoveLetters","brandExtensionReveal","brandOpenShackleClean","brandGlowClean","brandFinalLockClean"):
   self.assertIn("@keyframes "+term,css)
  self.assertIn("--brand-duration:8.4s",css)
 def test_final_lock_only(self):
  css=read("styles.css").replace(" ","").replace("\n","")
  self.assertIn(".brand-header.is-brand-final.brand-text-stage{display:none!important}",css)
  self.assertIn(".brand-header.is-brand-final.brand-final-lock-glyph{opacity:1!important",css)
 def test_footer_static(self):
  for page in PAGES:
   footer=read(page).split("<footer",1)[1]
   self.assertNotIn("brand-animated",footer)
if __name__=="__main__":unittest.main()
