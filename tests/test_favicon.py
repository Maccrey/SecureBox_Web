"""SecureBox 문서 폴더 파비콘의 배포 회귀 테스트."""
from pathlib import Path
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = ("index.html", "features.html", "stories.html", "pricing.html", "security.html")
SVG_LINK = r'<link\b(?=[^>]*\brel=["\']icon["\'])(?=[^>]*\bhref=["\']\./favicon\.svg["\'])[^>]*>'
ICO_LINK = r'<link\\b(?=[^>]*\\brel=["\\']icon["\\'])(?=[^>]*\\bhref=["\\']\\./favicon\\.ico["\\'])[^>]*>'
PREVIEW_LINK = r'<link\b(?=[^>]*\brel=["\']icon["\'])(?=[^>]*\bhref=["\']data:image/svg\+xml,)'


class FaviconContract(unittest.TestCase):
    def test_icon_file_is_valid_svg(self):
        icon = ROOT / "favicon.svg"
        self.assertTrue(icon.is_file(), "favicon.svg 누락")
        root = ET.fromstring(icon.read_text(encoding="utf-8"))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 64 64")
        self.assertIn("폴더", icon.read_text(encoding="utf-8"))

    def test_ico_contains_16_and_32_pixel_png_frames(self):
        ico = ROOT / "favicon.ico"
        self.assertTrue(ico.is_file(), "favicon.ico 누락")
        raw = ico.read_bytes()
        self.assertGreater(len(raw), 100)
        self.assertEqual(raw[:4], b"\\x00\\x00\\x01\\x00")
        count = struct.unpack_from("<H", raw, 4)[0]
        self.assertGreaterEqual(count, 2)
        sizes = set()
        for index in range(count):
            start = 6 + index * 16
            size, _, _, _, _, byte_count, offset = struct.unpack_from("<BBBBHHII", raw, start)
            width, height = raw[start], raw[start + 1]
            sizes.add((width or 256, height or 256))
            self.assertLessEqual(offset + byte_count, len(raw))
            self.assertEqual(raw[offset:offset + 8], b"\\x89PNG\\r\\n\\x1a\\n")
        self.assertTrue({(16, 16), (32, 32)}.issubset(sizes))

    def test_public_pages_reference_svg_and_ico_favicons(self):
        for page in PUBLIC_PAGES:
            with self.subTest(page=page):
                html = (ROOT / page).read_text(encoding="utf-8")
                head = html.split("</head>", 1)[0]
                self.assertEqual(len(re.findall(SVG_LINK, head, re.I)), 1)
                self.assertEqual(len(re.findall(ICO_LINK, head, re.I)), 1)
                self.assertIn('type="image/x-icon"', head)
                self.assertIn('type="image/svg+xml"', head)

    def test_single_file_preview_has_self_contained_favicon(self):
        html = (ROOT / "standalone-preview.html").read_text(encoding="utf-8")
        head = html.split("</head>", 1)[0]
        self.assertRegex(head, PREVIEW_LINK)


if __name__ == "__main__":
    unittest.main()
