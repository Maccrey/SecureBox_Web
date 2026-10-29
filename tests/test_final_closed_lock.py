"""로고 애니메이션 마지막 상태가 닫힌 자물쇠 하나로 고정되는지 검증."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class FinalClosedLockContract(unittest.TestCase):
    def test_script_forces_final_state(self):
        js=read("script.js")
        self.assertIn("is-brand-final",js)
        self.assertIn("animationend",js)
        self.assertIn("brandFinalLockGlyph",js)
    def test_css_final_state_hides_everything_except_closed_lock(self):
        css=read("styles.css").replace(" ","").replace("\n","")
        self.assertIn(".brand-header.is-brand-final.brand-shield{opacity:0",css)
        self.assertIn(".brand-header.is-brand-final.brand-open-shackle{opacity:0",css)
        self.assertIn(".brand-header.is-brand-final.brand-closed-shackle{opacity:0",css)
        self.assertIn(".brand-header.is-brand-final.brand-lock-body{opacity:0",css)
        self.assertIn(".brand-header.is-brand-final.brand-text-stage{width:0;opacity:0",css)
        self.assertIn(".brand-header.is-brand-final.brand-final-lock-glyph{opacity:1",css)
        self.assertIn(".brand-header.is-brand-final.brand-final-lock::before",css)
        self.assertIn("display:none",css)
    def test_final_glyph_is_a_closed_shackle(self):
        html=read("index.html")
        self.assertIn('class="brand-final-lock-glyph"',html)
        self.assertIn('A7 7 0 0 1 27 13.5V18',html)
if __name__=="__main__": unittest.main()
