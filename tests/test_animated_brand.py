"""SEC 브랜드 로고의 도입·변형·잠금 애니메이션 회귀 테스트 (RED 우선)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "features.html", "stories.html", "pricing.html",
         "security.html", "open-sec.html", "incidents.html")

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class AnimatedBrandContract(unittest.TestCase):
    def test_every_header_uses_same_accessible_animated_brand(self):
        for page in PAGES:
            with self.subTest(page=page):
                html = read(page)
                self.assertEqual(html.count('class="brand brand-animated"'), 1)
                self.assertIn('aria-label="SecureBox 홈"', html)
                self.assertIn('class="logo-lock-shackle"', html)
                self.assertIn('class="logo-original"', html)
                self.assertIn('class="logo-secname"', html)
                self.assertIn('class="logo-extension"', html)
                self.assertIn("SecureBox", html)
                self.assertIn("SecBox", html)
                self.assertIn(".sec", html)
                self.assertIn('href="./index.html"', html)

    def test_keyframes_have_open_then_closed_shackle_and_only_icon_final(self):
        css = read("styles.css")
        for name in ("secbox-lock-close", "secbox-original-out", "secbox-name-in-out",
                     "secbox-light-beam", "secbox-icon-glow"):
            self.assertIn("@keyframes " + name, css)
        self.assertRegex(css, r"(?s)@keyframes secbox-lock-close\s*\{.*?rotate\(-\d+deg\).*?rotate\(0deg\)")
        self.assertIn("animation-fill-mode: forwards", css)
        self.assertIn(".logo-wordstage", css)
        self.assertIn(".brand-animated::before", css)

    def test_reduced_motion_resolves_directly_to_closed_icon(self):
        css = read("styles.css")
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn(".brand-animated .logo-wordstage", css)
        self.assertIn(".brand-animated .logo-lock-shackle", css)

    def test_no_external_script_or_inert_logo(self):
        for page in PAGES:
            html = read(page)
            self.assertNotIn("cdn.jsdelivr.net", html)
            self.assertEqual(html.count('class="brand brand-animated"'), 1)

if __name__ == "__main__":
    unittest.main()
