# Business: 분실 후 원격 암호화 계약 (구현 전 검증 필요)

> **사용자 의도:** 휴대폰에서 보호할 폴더를 먼저 지정하고, 분실 후 **등록 Windows/macOS PC에서 원격 명령**을 전송하면 모바일 앱이 해당 파일들을 암호화하도록 시도한다. 평상시 사전 암호화 방식과 구분한다.

## 보안 범위 및 제한

- 일반 휴대폰 전체 잠금, 다른 앱 전용 디렉터리 무단 접근, 즉각 암호화 보장, 완전 삭제, 다른 앱과 백업에 남은 평문 회수는 비목표.
- 모바일이 오프라인·꺼짐·앱 삭제·권한 철회·OS 백그라운드 실행 불가 상태면 원격 암호화할 수 없다. **명령 접수는 보호 완료가 아니다.**
- Android는 SAF 권한을 받은 지정 폴더/앱 저장소만 접근하고, iOS는 security-scoped URL/앱 컨테이너에 한정된다. OS 전체 파일을 가로채는 훅은 금지한다.
- 즉시 기밀성이 요구되는 자료는 **별도 선택적 사전 암호화 보관함** 사용을 권장한다.

## API·키 계약

1. 등록 PC 서명 요청: `command_id`, `tenant_id`, `device_id`, `folder_policy_ids`, `action=ENCRYPT_ON_LOSS`, `nonce`, `expires_at`, `issued_at`, `signer_key_id`, `policy_version`. 파일 암호화 키를 서명용 키로 재사용하지 않는다.
2. 서버는 Business 구독·본인/MFA·PC 슬롯·조직 권한·서명·만료·정책 버전 검증. 서명 위조·타 조직 접근·nonce 재사용·중복 명령은 거부. `(tenant_id,device_id,command_id)` 기준 **멱등성** 보장.
3. FCM(Android)·APNs(iOS)는 **알림 힌트**만 전달하며 원문 파일명, 경로, 키, 삭제 명령을 넣지 않는다. 모바일은 TLS로 서버에서 서명된 명령을 조회해 추가 검증한다.
4. Android: FCM 수신 콜백은 단기 작업만 수행하고 WorkManager(또는 조건에 맞는 foreground worker)에 암호화를 예약한다. OS 제한으로 지연/중단 가능.
5. iOS: background push는 전달 보장이 없고 BGTask 실행 시각도 OS가 결정한다. 앱이 실행되면 보류 명령을 다시 확인한다. background 실행 불가 시 상태를 `PENDING_ON_DEVICE`로 유지한다.
6. 모바일은 미리 허가된 폴더만 청크 단위 AEAD(AES-256-GCM)로 암호화하고, 데이터 키는 등록 PC 공개키 키 슬롯으로 보호한다. PC 비밀키는 모바일에 저장하지 않는다. 기업 관리자 온라인 승인 없이는 PC에서도 복호화할 수 없도록 한다.
7. 암호화 검증 및 별도 백업/복구 경로 검증이 성공하고 사용자가 **사전 동의**한 경우에만 원본 삭제 요청을 시도한다. 용량 부족·앱 중단·검증 실패·권한 부족 시 원본 보존. 플래시 원본 삭제는 복구 불가능한 완전 삭제가 아니다.

## 상태 머신

`CREATED(명령 접수)` → `DELIVERED(기기 수신)` → `RUNNING(암호화 진행)` → `VERIFIED(암호화 완료)`; 예외 상태 `PENDING_ON_DEVICE`, `PARTIAL`, `FAILED`, `EXPIRED`, `CANCELED`.

- 기기 수신과 암호화 완료를 분리해 표시한다. 보호 완료는 앱이 암호화 결과의 인증·복구 가능성 검증을 끝낸 경우에만 표시한다.
- 재시도/중복 푸시는 명령 ID의 멱등성을 유지하고 중간 산출물로 평문을 유출하지 않는다.
- 상태 변경에는 조직 분리, 서버 측 권한, 서명된 결과 보고/ACK, 감사 로그를 적용한다.

## TDD 출시 게이트

1. 실패 테스트: 서명 위조, 잘못된 조직·구독, 만료/재사용 명령, 중복 전달, 앱 삭제, 원격 전송 지연, 파일 변경, 용량 부족, 권한 철회, 강제 종료, 부분 성공, ACK 위조, 검증 전 원본 삭제, 키 단독 복호화 우회.
2. 최소 구현 → 리팩터링 → Android·iOS 통합 및 계약 테스트 → **실기기** 시험 → 회귀 테스트 → 문서 → 한국어 커밋.
3. Android Doze/SAF/WorkManager 중단, iOS APNs 무전달/앱 강제 종료/잠금/BGTask 중단, 대용량 파일 등 시험.
4. 비인가 실행 0건, 검증 전 삭제 0건, 완료되지 않은 작업을 완료로 오표시 0건, 관리자 공동 승인 우회 0건.

## 공식 근거

- https://firebase.google.com/docs/cloud-messaging/android/receive-messages
- https://developer.android.com/training/data-storage/shared/documents-files
- https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/long-running
- https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app
- https://developer.apple.com/documentation/backgroundtasks
- https://developer.apple.com/documentation/uikit/providing-access-to-directories
