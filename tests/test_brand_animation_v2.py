"""헤더 로고 애니메이션 v2 계약: 열린 자물쇠로 시작하고 잠긴 자물쇠만 남는다."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","stories.html","pricing.html","security.html","open-sec.html","incidents.html")
def read(p): return (ROOT/p).read_text(encoding="utf-8")

class BrandAnimationV2(unittest.TestCase):
    def test_all_public_headers_use_animation(self):
        for page in PAGES:
            with self.subTest(page=page):
                head=read(page).split("</header>",1)[0]
                for term in ("brand-header","brand-open-shackle","brand-final-lock-glyph","brand-full-name","brand-sec-name","SecBox",".sec"):
                    self.assertIn(term,head)

    def test_final_state_is_lock_only(self):
        css=read("styles.css").replace(" ","")
        self.assertIn("@keyframesbrandMarkBackground",css)
        self.assertIn("90%,100%{background:transparent",css)
        self.assertIn("@keyframesbrandShield",css)
        self.assertIn("82%,100%{opacity:0",css)
        self.assertIn("@keyframesbrandLockOnly",css)
        self.assertIn("90%,100%{width:0;opacity:0",css)
        self.assertIn("@keyframesbrandFinalLockGlyph",css)
        self.assertIn("82%,100%{opacity:1;transform:scale(1)",css)
        self.assertIn(".brand-final-lock-glyph{color:var(--mint)",css)

    def test_initial_state_uses_open_lock(self):
        css=read("styles.css").replace(" ","")
        self.assertIn(".brand-open-shackle{opacity:1",css)
        self.assertIn(".brand-closed-shackle{opacity:0",css)
        self.assertIn("0%,56%{opacity:1",css)

    def test_reduced_motion_finishes_on_lock_only(self):
        css=read("styles.css").replace(" ","")
        block=css.split("@media(prefers-reduced-motion:reduce)",1)[1]
        self.assertIn(".brand-header.brand-mark{background:transparent",block)
        self.assertIn(".brand-final-lock-glyph{opacity:1",block)

if __name__=="__main__": unittest.main()
