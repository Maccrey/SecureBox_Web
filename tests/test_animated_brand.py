"""SecureBox 헤더 로고 애니메이션 계약 테스트."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","stories.html","pricing.html","security.html","open-sec.html")

def read(p): return (ROOT/p).read_text(encoding="utf-8")

class AnimatedBrandContract(unittest.TestCase):
    def test_header_uses_animated_brand(self):
        for page in PAGES:
            with self.subTest(page=page):
                html=read(page)
                head_logo=html.split("</header>",1)[0]
                self.assertIn("brand-animated",head_logo)
                self.assertIn("brand-open-shackle",head_logo)
                self.assertIn("brand-closed-shackle",head_logo)
                self.assertIn("brand-square-lock-glyph",head_logo)
                self.assertIn("brand-full-name",head_logo)
                self.assertIn("brand-sec-name",head_logo)
                self.assertIn("SecBox",head_logo)
                self.assertIn(".sec",head_logo)

    def test_css_animation_sequence(self):
        css=read("styles.css")
        for term in (
            "@keyframes brandFullName",
            "@keyframes brandSecName",
            "@keyframes brandOpenShackle",
            "@keyframes brandClosedShackle",
            "@keyframes brandShield",
            "@keyframes brandGlow",
            "@keyframes brandLockOnly",
            "prefers-reduced-motion"
        ):
            self.assertIn(term,css)
        self.assertIn("animation-fill-mode:forwards",css.replace(" ",""))

    def test_final_state_is_lock_only_and_fills_square(self):
        css=read("styles.css").replace(" ","")
        self.assertIn("@keyframesbrandFinalLockPulse",css)
        self.assertIn("@keyframesbrandClosedShackle",css)
        self.assertIn("@keyframesbrandLockBody",css)
        self.assertIn("@keyframesbrandFinalLockGlyph",css)
        self.assertIn(".brand-final-lock-glyph",css)
        self.assertIn("transform:scale(.55)",css)
        self.assertIn("82%,100%{opacity:1;transform:scale(1)",css)
        self.assertIn("82%,100%{opacity:0",css)
        self.assertIn("brand-final-lock",css)
        self.assertIn("brand-square-lock-glyph",css)
        self.assertIn("@keyframesbrandSquareBlackLock",css)
        self.assertIn("color:var(--navy)",css)
        self.assertIn("72%,78%{opacity:1;transform:scale(1)",css)
        self.assertIn("82%,100%{opacity:0;transform:scale(.9)",css)

    def test_footer_stays_static(self):
        for page in PAGES:
            with self.subTest(page=page):
                html=read(page)
                footer=html.split("<footer",1)[1]
                self.assertNotIn("brand-animated",footer)
                self.assertIn("SecureBox",footer)

if __name__=="__main__": unittest.main()
