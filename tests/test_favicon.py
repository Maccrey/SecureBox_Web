"""SecureBox 문서 폴더 파비콘의 배포 회귀 테스트."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = ("index.html", "features.html", "stories.html", "pricing.html", "security.html")
LINK = r'<link\b(?=[^>]*\brel=["\']icon["\'])(?=[^>]*\bhref=["\']\./favicon\.svg["\'])[^>]*>'
PREVIEW_LINK = r'<link\b(?=[^>]*\brel=["\']icon["\'])(?=[^>]*\bhref=["\']data:image/svg\+xml,)'


class FaviconContract(unittest.TestCase):
    def test_icon_file_is_valid_svg(self):
        icon = ROOT / "favicon.svg"
        self.assertTrue(icon.is_file(), "favicon.svg 누락")
        root = ET.fromstring(icon.read_text(encoding="utf-8"))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 64 64")
        self.assertIn("폴더", icon.read_text(encoding="utf-8"))

    def test_public_pages_reference_one_local_favicon(self):
        for page in PUBLIC_PAGES:
            with self.subTest(page=page):
                html = (ROOT / page).read_text(encoding="utf-8")
                head = html.split("</head>", 1)[0]
                self.assertEqual(len(re.findall(LINK, head, re.I)), 1)
                self.assertIn('type="image/svg+xml"', head)

    def test_single_file_preview_has_self_contained_favicon(self):
        html = (ROOT / "standalone-preview.html").read_text(encoding="utf-8")
        head = html.split("</head>", 1)[0]
        self.assertRegex(head, PREVIEW_LINK)


if __name__ == "__main__":
    unittest.main()
