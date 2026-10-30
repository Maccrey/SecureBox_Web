"""헤더 로고의 문구 중복 방지 및 4단계 애니메이션 계약."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","incidents.html","stories.html","pricing.html","security.html","open-sec.html")

class LogoSingleLabelContract(unittest.TestCase):
    def test_logo_has_exactly_one_of_each_stage_label(self):
        for path in PAGES:
            header=(ROOT/path).read_text(encoding="utf-8").split("</header>",1)[0]
            self.assertEqual(header.count('class="brand-text-stage brand-morph"'),1,path)
            self.assertEqual(header.count('class="brand-extension"'),1,path)
    def test_frames_do_not_overlap(self):
        css=(ROOT/"styles.css").read_text(encoding="utf-8")
        self.assertIn("@keyframes brandRemoveLetters{",css)
        self.assertIn("35%,100%{max-width:0;opacity:0",css)
        self.assertIn("@keyframes brandExtensionReveal{",css)
        self.assertIn("50%,61%{max-width:3.2ch;opacity:1",css)
        self.assertIn("71%,100%{max-width:3.2ch;opacity:1",css)
        self.assertIn("brandGlowClean",css)
        self.assertIn("brandFinalLockClean",css)
    def test_cache_key_on_every_page(self):
        for path in PAGES:
            content=(ROOT/path).read_text(encoding="utf-8")
            self.assertIn("styles.css?v=20261030-logo5",content,path)

if __name__=="__main__": unittest.main()
