"""공식 출처 기반 보안 사고 페이지와 고객 안내 계약 (RED 우선)."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGES=("index.html","features.html","stories.html","pricing.html","security.html","open-sec.html","incidents.html")
def read(p):return (ROOT/p).read_text(encoding="utf-8")
class SecurityIncidentMarketingContract(unittest.TestCase):
 def test_official_incident_page(self):
  s=read("incidents.html")
  for keyword in ("Microsoft","2023","25개","ICO","286명","USB","이메일","SecureBox","암호화","원문","출처"):
   self.assertIn(keyword,s)
  self.assertIn("https://blogs.microsoft.com/on-the-issues/2023/07/11/mitigation-china-based-threat-actor/",s)
  self.assertIn("https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/security/encryption/encryption-and-data-storage/",s)
  self.assertIn("피싱",s)
  self.assertNotIn("SecureBox가 막았습니다",s)
 def test_navigation_and_home_conversion_path(self):
  for p in PAGES:
   self.assertIn('href="./incidents.html"',read(p),p)
  self.assertIn("실제 사고 사례",read("index.html"))
 def test_no_unverified_impact_claims(self):
  s=read("incidents.html")
  for item in ("사고 당시 SecureBox가 사용되었다는 뜻이 아닙니다","이미 복호화된","비밀번호","출시 예정"):
   self.assertIn(item,s)
 def test_standalone_preview_has_incident_page(self):
  p=read("standalone-preview.html")
  self.assertIn('data-page="incidents.html"',p)
  self.assertIn('"incidents.html"',p)
 def test_public_no_internal_vendors(self):
  for p in PAGES:
   for name in ("Firebase","Polar","Firestore","Cloud KMS"):
    self.assertNotIn(name,read(p))
if __name__=="__main__":unittest.main()
