"""브랜드 애니메이션은 상태 간 겹침 없이 단일 타임라인으로 전환한다."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
class CleanBrandTimeline(unittest.TestCase):
    def test_single_timeline_contract(self):
        css=read("styles.css")
        self.assertIn("--brand-duration:8.4s",css)
        for name in ("brandRemoveLetters","brandExtensionReveal","brandOpenShackleClean","brandFinalLockClean","brandGlowClean"):
            self.assertIn("@keyframes "+name,css)
        self.assertNotIn("brandPersistentLock",css)
        self.assertNotIn("brandSquareBlackLock",css)
    def test_no_duplicate_final_lock_layers(self):
        css=read("styles.css")
        self.assertNotIn(".brand-final-lock::before",css)
        self.assertNotIn(".brand-final-lock::after",css)
        self.assertIn(".brand-square-lock-glyph{display:none",css)
    def test_final_lock_only_state(self):
        css=read("styles.css")
        self.assertIn(".brand-header.is-brand-final .brand-text-stage{display:none!important}",css)
        self.assertIn(".brand-header.is-brand-final .brand-final-lock-glyph{opacity:1!important",css)
    def test_js_uses_css_duration(self):
        js=read("script.js")
        self.assertIn("brandDurationMs",js)
        self.assertNotIn("7400",js)
if __name__=="__main__": unittest.main()
