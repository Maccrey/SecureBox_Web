"""헤더 로고의 문구 중복 방지 및 4단계 애니메이션 계약."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","incidents.html","stories.html","pricing.html","security.html","open-sec.html")

class LogoSingleLabelContract(unittest.TestCase):
    def test_logo_has_exactly_one_of_each_stage_label(self):
        for path in PAGES:
            header=(ROOT/path).read_text(encoding="utf-8").split("</header>",1)[0]
            self.assertEqual(header.count('class="brand-text brand-full-name"'),1,path)
            self.assertEqual(header.count('class="brand-text brand-sec-name"'),1,path)
    def test_frames_do_not_overlap(self):
        css=(ROOT/"styles.css").read_text(encoding="utf-8")
        self.assertIn("@keyframes brandFullNameClean{0%,24%{opacity:1",css)
        self.assertIn("27%,100%{opacity:0",css)
        self.assertIn("@keyframes brandSecNameClean{0%,30%{opacity:0",css)
        self.assertIn("34%,57%{opacity:1",css)
        self.assertIn("60%,100%{opacity:0",css)
        self.assertIn("brandGlowClean",css)
        self.assertIn("brandFinalLockClean",css)
    def test_cache_key_on_every_page(self):
        for path in PAGES:
            content=(ROOT/path).read_text(encoding="utf-8")
            self.assertIn("styles.css?v=20261030-logo3",content,path)

if __name__=="__main__": unittest.main()
