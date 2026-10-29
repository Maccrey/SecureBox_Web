"""문서 폴더 favicon.ico + favicon.svg 회귀 검증."""
from pathlib import Path
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "features.html", "stories.html", "pricing.html", "security.html")


class FaviconContract(unittest.TestCase):
    def test_svg(self):
        svg = (ROOT / "favicon.svg").read_text(encoding="utf-8")
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib.get("viewBox"), "0 0 64 64")
        self.assertIn("문서 폴더", svg)

    def test_ico(self):
        data = (ROOT / "favicon.ico").read_bytes()
        self.assertEqual(data[:4], bytes((0, 0, 1, 0)))
        count = struct.unpack_from("<H", data, 4)[0]
        sizes = set()
        for i in range(count):
            off = 6 + 16 * i
            w, h, colors, reserved, planes, bpp, length, start = struct.unpack_from("<BBBBHHII", data, off)
            sizes.add((w or 256, h or 256))
            self.assertLessEqual(start + length, len(data))
            self.assertEqual(data[start:start + 8], bytes((137, 80, 78, 71, 13, 10, 26, 10)))
        self.assertTrue({(16, 16), (32, 32)}.issubset(sizes))

    def test_pages(self):
        for page in PAGES:
            with self.subTest(page=page):
                head = (ROOT / page).read_text(encoding="utf-8").split("</head>", 1)[0]
                self.assertEqual(head.count('href="./favicon.svg"'), 1)
                self.assertEqual(head.count('href="./favicon.ico"'), 1)
                self.assertIn('type="image/svg+xml"', head)
                self.assertIn('type="image/x-icon"', head)

    def test_standalone(self):
        head = (ROOT / "standalone-preview.html").read_text(encoding="utf-8").split("</head>", 1)[0]
        self.assertIn('data:image/svg+xml,', head)
        self.assertIn('rel="icon"', head)

if __name__ == "__main__":
    unittest.main()
