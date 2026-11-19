# ENTRYPOINT — Paper III Independent Replication (R1)

RIUD Paper III(독립 재현) 공개 패키지. 단계별로 흩어져 있던 결합을 단일 패키지 매니페스트(SHA256_MANIFEST.txt)로 통합했다. 정본 사본이며 원본은 수정하지 않았다.

## 구성

- FINAL_REPRO_PACKAGE\: 저자 최종 패키지 RIUD_INDEPENDENT_REPLICATION_FINAL_20260805 전량 사본 — 5,738개 파일 / 224,560,342B. 본체는 vendor\(R27 확증 트리: 코드·입력·기댓값)와 README·FINAL_PACKAGE_MANIFEST.csv·SHA256_MANIFEST.txt. work\는 원본에서도 공실이었다(아래 KNOWN_GAPS 참조).
- CLAIM_EVIDENCE\: 컴패니언 PAPER_III 슬라이스 30/30 — INDEPENDENT_REPLICATION\(MERGE_RESULT.json, PAPERIII_RESULTS.csv, INPUT_CLOSURE_AUDIT.md, R1 소스 바인딩), CANONICAL\(R1_COLD_INDEPENDENT_* 6종: 최종 비교·퍼뮤테이션 널·매니페스트·보고), MANIFESTS, CLAIM_EVIDENCE_MATRIX.
- NUMERICAL_RELEASE_PAPER_III\: 숫자 릴리스 PAPER_III 슬라이스 24/24 — R2A/R2A2/R2Q9 게이트 자산(잠금 스크립트·legacy 입력·게이트 정의·검증 요약).
- COLD_EXACT_REBUILD_R1\: 콜드 재현 복구 감사 6종(RECOVERY_REPORT, FINAL_AUDIT, ORIGINAL_ARTIFACT_INVENTORY, PATH_RECOVERY_LEDGER, COLD_HASH_MATRIX, COLD_VS_ORIGINAL_NUMERIC_COMPARISON).

## 검증·대조값

- 사전고정 보정 p: H1 0.005994 / H2 0.002997 / H3 0.026973.
- 재현 p: H1 0.009990 / H2 0.002997 / H3 0.045954.
- 최종 판정: VALIDATED_PARTIALLY_SHARED_DYNAMICS (원본·재현 공통).
- 최종 비교 산출의 정본은 컴패니언 슬라이스와 PUBLIC_MASTER R2(03_PAPER_III\FULL_INDEPENDENT_REPLICATION)에 생존 — 외부 패키지의 단계 폴더는 정리 후 공실이다(KNOWN_GAPS 참조).

## 알려진 결함

입력 폐쇄성 결함(외부검증 RAW 이벤트 5건 미발견)을 메우지 않고 KNOWN_GAPS.md에 그대로 기록했다.
