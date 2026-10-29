# SecureBox 홍보 사이트 (실제 정적 웹 구현)

- HTML/CSS/JavaScript 정적 구성. PHP, 백엔드, 외부 CDN, 계정 생성, 결제 호출, 원본 파일 업로드가 **없음**.
- 개인정보 폼/실제 Polar checkout 연결 **미구현**. 앱 다운로드와 유료 기능 또한 아직 정식 출시 전임을 명시.
- 제품 기획·가격: `../PRD.md` (Contract Pass $4.90/전송 1건, Team $12/월 또는 $120/년, Business $24/월 또는 $240/년, 1인 기준). 수신자 무료 복호화. Contract Pass는 출시 전 기획 상품이며 실제 결제 불가.

## 미리보기

저장소 루트에서:

```bash
python -m http.server 8000 --directory site
# http://127.0.0.1:8000/
```

또는 `site` 폴더에서:

```bash
python -m http.server 8000
```

## Firebase Hosting 배포 (프로젝트 연결·승인 후)

```bash
npm install -g firebase-tools
firebase login
cd site
firebase use --add  # 실제 프로젝트 선택. 문서에 ID/키를 쓰지 않음.
firebase hosting:channel:deploy preview --expires 7d
# 보안 헤더 / 접근성 / 가격 콘텐츠 QA 완료 후:
firebase deploy --only hosting
```

- 현재 `firebase.json`은 **정적 사이트 전용**. 실제 운영 프로젝트 ID/도메인/Polar 링크가 입력되지 않았으므로 온라인 배포는 아직 하지 않음.
- 운영 시 `Strict-Transport-Security`와 CSP 헤더를 실제 HTTPS 응답에서 검사.
- 사용자 동의 없는 분석 스크립트/쿠키 및 외부 폰트 사용 금지.
- 도메인을 입력하고 크롤링 검수 후 sitemap, canonical URL, OpenGraph 이미지를 추가(현재 미확정이므로 임의 URL 생성 금지).
- JavaScript는 메뉴와 가격 계산 기능만 수행. 비밀번호/키/파일을 입력받지 않는다.

## 접근성 및 보안 확인

```bash
node --check site/script.js
python scripts/validate_site.py
```

- Playwright: 375px/768px/1440px 뷰포트 스크린샷, 메뉴 키보드 접근, 연간 요금/좌석 계산, FAQ `<details>`, 모든 앵커 유효 여부를 검증.
- 웹 보안 모의 점검: 개발자도구 Network에서 외부 요청 0건, 콘솔 오류 0건, Firebase Hosting CSP/기본 헤더 확인.

## 최신 제품 정책 표기

Team/Business 앱 경유 USB·SNS·카카오톡 등 메신저 공유 자동 `.sec` 암호화는 계획 기능입니다. Team은 PC/모바일 중 1대, Business는 PC 1대+모바일 1대 동시 로그인 정책입니다. PC 카카오톡 원본 직접 첨부까지 제어하거나 자동 첨부할 수 있는 기능으로 홍보하지 않습니다. 현재 웹사이트는 데모이며 자동 암호화 앱 및 실결제는 연결되지 않았습니다.


## 고객 중심 콘텐츠와 만화형 사용 시나리오

- 기업 기능 카드에는 내부 서비스 제공자·결제사의 기술명을 쓰지 않고, **팀 보안 관리·승인 이력·접근 시간·기기 슬롯**을 설명한다.
- 만화 7편(모두 가상 시나리오): `site/assets/stories/` 내부 WebP 7개와 각 카드의 상황·해결·효과·제약 표시. 분류 버튼은 전체/개인·학생/직장인·팀/사업가.
- 보안 범위: SecureBox 경유 암호문만 보호. 카카오톡 PC 직접 자동 첨부나 개인 PC의 모든 파일 공유/USB 복사 강제 차단을 주장하지 않는다.
- 내부 기술 공급자명은 이 개발자 README·PRD·보안 문서에서만 다룬다. 정적 공개 `site/index.html`에는 포함하지 않는다.

### TDD 공개 배포 게이트

```bash
# 먼저 실패할 테스트를 만들고 RED를 확인 후 구현
python -m pytest -q tests/site/test_public_marketing.py
node --check site/script.js
python scripts/validate_site.py
python scripts/build_standalone_preview.py && python scripts/verify_site_browser.py  # Playwright + Chromium
```

모든 검증과 접근성·보안 카피 수동 검토를 통과하고 개발 문서를 동기화한 뒤, 반드시 **한국어 Git 커밋 메시지**로 저장한다. 구현된 랜딩 페이지가 암호화·결제 제품의 출시를 의미하지 않음을 페이지에 고지한다.

- 단일 HTML 미리보기 생성: `python scripts/build_standalone_preview.py` (저장소 루트에서 실행). 이 파일은 로컬 시연용이므로 인라인 스타일/스크립트 CSP가 사용되며 **정식 배포는 `site/index.html`과 엄격한 CSP**를 사용한다.


## Business 분실 모바일 보호 (Stage 40, 공개 설명)

- 새 만화 EPISODE 06: 휴대폰 분실 → 등록 PC 분실 신고 → SecureBox 기업 보관함 신규 키 차단 → 회수 후 등록 PC 암호화 키 서명과 MFA로 해제 승인.
- **제공 예정**이며 일반 개인폰을 가로채 잠글 수 있는 OS 전역 기능으로 홍보하지 않는다. 휴대폰 오프라인 시 명령은 지연될 수 있고 이미 저장한 평문 파일은 회수할 수 없음.
- 회사 관리형 Android Enterprise·감독형 iOS의 MDM 기기 분실 모드는 별도 장치 관리 요건과 보안 고지 아래 지원 검토. Android는 관리형 모드에서도 사용자가 기기 암호로 OS 분실 모드를 종료할 수 있다는 점 표시.
- 공개 페이지는 공급업체명, API 주소, 원시 키·복구 토큰 입력 폼 또는 실제 잠금 콘솔을 노출하지 않음.
- 테스트: `python -m pytest -q tests/site/test_public_marketing.py tests/site/test_business_lost_device_marketing.py && python scripts/validate_site.py && python scripts/build_standalone_preview.py && python scripts/verify_site_browser.py`.


## Business 모바일 폴더 사전 암호화 · 텍스트 없는 만화(개정)

- 7편 만화 에피소드 이미지에는 글자를 넣지 않는다. 제목·대사·상황·주의사항은 접근 가능한 HTML `.comic-copy` 텍스트 컨테이너에 배치한다. 자산: `site/assets/stories/*.webp`, 자산 정책: `assets/stories/ARTWORK_NO_TEXT.md`.
- EPISODE 06: 휴대폰 분실 전 지정 폴더 사전 암호화·분실 신고/온라인 접근 차단. EPISODE 07: PC 공개키로 보호 후 검증·백업·사용자 동의 시 논리적 원본 삭제 요청, 등록 PC에서만 해독.
- 일반 스마트폰 OS 전체 잠금, 분실 후 강제 원격 암호화, 완전 소거, 클라우드 외부 사본 자동 삭제는 지원하지 않는다.
- 검증: `python -m pytest -q tests/site/test_protected_folder_marketing.py`; `python scripts/build_standalone_preview.py && python scripts/verify_site_browser.py`.


## 페이지 구조 개편 (2026-10-28)

**최종 결정: 짧은 홈 + 주제별 상세 페이지**. 고객의 핵심 질문에 즉시 답할 수 있도록 `index.html`의 제품 소개와 CTA를 간결하게 하고, 기능·만화 사례·요금제·보안 안내는 `features.html`, `stories.html`, `pricing.html`, `security.html`로 구분한다. 5개 URL은 정적 접근 가능한 `<a href>` 링크로 이동하며 JS 라우팅 의존이 없다.

- 공개 사이트에 내부 인프라/결제사명·운영 구조·개발자 디버깅 API는 노출하지 않는다. 출시 전 구매와 앱 다운로드는 연결하지 않는다.
- 이미지 속 대사/문장 대신 `.comic-copy` HTML 텍스트로 접근 가능한 설명을 제공한다.
- 홈→가격, 홈→사례, 사례→기능, 기능→가격의 구매 의사 결정 경로와 상세 5페이지 SEO/접근성, 가격 토글·모바일 메뉴가 회귀 테스트 대상.
- 업데이트 기능도 '서명 검증된 공식 배포 경로로 안전하게 갱신'하는 고객 혜택만 설명. 실제 업데이트 가능하다는 표현은 개발 상태와 함께 표시한다.

## Business 모바일 분실 후 원격 암호화 기획 (2026-10-29 변경)

- 이전의 '항상 사전 암호화'를 기본 시나리오로 제시하는 문구를 교체했습니다. 사용자는 모바일에서 보호 폴더를 지정하고, 분실 후 등록 PC에서 **조건부 원격 암호화 요청**을 보냅니다.
- 이 기능은 아직 개발·실기기 검증 전이며, 모바일이 원격 명령을 받아 실행할 수 있는 상태에서만 동작합니다. 푸시 전달은 암호화 완료를 뜻하지 않습니다. 특히 iOS 백그라운드 실행은 보장되지 않습니다.
- 원본 삭제는 검증·백업·사전 동의가 필요하고, PC 전용 키 + 관리자 온라인 승인 정책을 유지합니다.
- 내부 설계: [docs/REMOTE_LOSS_ENCRYPTION_CONTRACT.md](docs/REMOTE_LOSS_ENCRYPTION_CONTRACT.md). 공개 웹페이지에는 Firebase·Polar 등 내부 기술명을 노출하지 않습니다.
- TDD 재검증: `python -m unittest discover -s tests -p "test_*.py"` → HTML 구조·가격 계산·링크·모바일 브라우저 회귀 검사 → 한국어 커밋.

## 문서 폴더 파비콘 (2026-10-29)

- `favicon.svg`: 문서 폴더 + 보안 확인 표시를 담은 기본 벡터 파비콘.
- `favicon.ico`: 호환 브라우저용 **16×16 / 32×32 PNG 프레임**을 포함한 ICO 폴백. SVG의 폴더·문서 구성을 작은 크기에 맞게 단순화했다.
- `index.html`, `features.html`, `stories.html`, `pricing.html`, `security.html`의 `<head>`에서 SVG와 ICO를 함께 참조한다. `standalone-preview.html`은 오프라인 단일 HTML을 유지하기 위해 SVG 데이터 URI 아이콘을 사용한다.
- TDD: `python -m unittest discover -s tests -p 'test_*.py' -v`. `tests/test_favicon.py`는 파일 헤더, PNG 프레임, 5개 HTML 참조, 독립 미리보기를 검사한다.
- 배포: GitHub 반영은 사이트 공개 배포와 다르다. Hosting 배포 후 응답 코드·콘텐츠 유형 및 브라우저 캐시/탭 아이콘을 별도로 확인한다.
