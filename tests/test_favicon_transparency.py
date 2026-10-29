"""배경 투명 파비콘 계약: SVG 사각 배경이 없어야 하며 ICO 모든 크기에 알파가 있어야 한다."""
from pathlib import Path
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class TransparentFaviconTest(unittest.TestCase):
    def test_svg_has_no_full_canvas_background(self):
        tree = ET.parse(ROOT / "favicon.svg")
        self.assertFalse(any(
            node.tag.endswith("rect")
            and node.attrib.get("width") == "64"
            and node.attrib.get("height") == "64"
            for node in tree.iter()
        ))
    def test_ico_has_alpha_mask(self):
        data = (ROOT / "favicon.ico").read_bytes()
        self.assertEqual(data[:4], bytes([0,0,1,0]))
        count = struct.unpack_from("<H", data, 4)[0]
        self.assertGreaterEqual(count, 2)
        for i in range(count):
            w,h,_,_,_,_,length,offset = struct.unpack_from("<BBBBHHII",data,6+16*i)
            frame=data[offset:offset+length]
            self.assertEqual(frame[:8], b"\\x89PNG\\r\\n\\x1a\\n")
            self.assertEqual(frame[25],6, "PNG must use RGBA")
    def test_svg_and_ico_referenced(self):
        for name in ("index.html","features.html","stories.html","pricing.html","security.html"):
            head=(ROOT/name).read_text(encoding="utf-8").split("</head>",1)[0]
            self.assertIn('href="./favicon.svg"',head)
            self.assertIn('href="./favicon.ico"',head)
if __name__=="__main__": unittest.main()
