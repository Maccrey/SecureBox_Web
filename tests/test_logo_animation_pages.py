"""GitHub Pages 로고 애니메이션 및 정적 자산 캐시 버전 계약."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","incidents.html","stories.html","pricing.html","security.html","open-sec.html")
VERSION="20261030-logo2"

def read(path): return (ROOT/path).read_text(encoding="utf-8")

class LogoPagesContract(unittest.TestCase):
    def test_requested_animation_sequence_exists(self):
        html=read("index.html")
        css=read("styles.css")
        js=read("script.js")
        for term in ("brand-open-shackle","brand-full-name","brand-sec-name","brand-ext","brand-glow","brand-final-lock-glyph"):
            self.assertIn(term,html+css)
        self.assertIn("SecureBox",html)
        self.assertIn("SecBox",html)
        self.assertIn(".sec",html)
        for keyframe in ("brandOpenShackleClean","brandFullNameClean","brandSecNameClean","brandGlowClean","brandFinalLockClean"):
            self.assertIn("@keyframes "+keyframe,css)
        self.assertIn("is-brand-final",js)
        self.assertIn(".brand-header.is-brand-final .brand-text-stage{display:none!important}",css)

    def test_all_pages_force_latest_css_and_js(self):
        for page in PAGES:
            with self.subTest(page=page):
                html=read(page)
                self.assertIn(f'href="./styles.css?v={VERSION}"',html)
                self.assertIn(f'src="./script.js?v={VERSION}"',html)
                header=html.split("</header>",1)[0]
                self.assertIn("brand-open-shackle",header)
                self.assertIn("brand-final-lock-glyph",header)

    def test_reduced_motion_finishes_locked(self):
        css=read("styles.css")
        reduced=css.split("@media(prefers-reduced-motion:reduce)",1)[1]
        self.assertIn(".brand-final-lock-glyph{opacity:1",reduced.replace(" ",""))
        self.assertIn(".brand-text-stage{display:none!important",reduced.replace(" ",""))

if __name__=="__main__": unittest.main()
