# ENTRYPOINT — Paper II Numerical Companion (R1)

RIUD Paper II 공개 패키지. 정본 사본이며 원본(E:)은 수정하지 않았다.

## 구성

- 루트: 저자 클레임-증거 컴패니언(2026-08-18)의 PAPER_II 슬라이스 전량 — 컴패니언 SHA256SUMS의 PAPER_II 항목 221/221. 하위: SXS_GR(궤도 물리 감사·미러/대리 대조·패널 감사), NULLS(R26 계열 널 대조·per-window 요약·원시 산출), OBSERVED_DEV99(물리 관계 맵), SHARED_FROZEN_AUTHORITY_PACKAGE(자체 SHA256SUMS 내장, 08_EXPECTED_RESULTS 포함), CLAIM_EVIDENCE_MATRIX·PAPER_II_MANUSCRIPT.
- COMPANION_ROOT\: 컴패니언 루트 공유 문서 9종 + 00_AUDIT 4항목 + INTEGRATED 5항목(I 패키지와 동일 공유 층).
- SHARED_NUMERICAL_RELEASE_PAPER_I_II\: 숫자 릴리스의 PAPER_I_II 블록 16항목 전량 + RELEASE_ROOT\(릴리스 README·PACKAGE_SCOPE·verify_numbers.py). 이 블록 안의 표 8종은 paper2_manuscript_package 산출이며, R26C37/R26C42H source_frozen + 예상 결과가 함께 들어 있다.

## I·II 분리 판정

숫자 릴리스는 I·II를 단일 블록(PAPER_I_II 16항목)으로만 결합해 분리 불가 — 공유 층으로 포함했다. 청구-증거 층은 분리 가능해 PAPER_II 221항목을 본체로 조립했다. II 단독 숫자 층이 없는 것은 결함이 아니라 릴리스 설계다.

## 검증 (사본 재조립 실행)

- 컴패니언 전량(987항목) 임시 재조립에서 VERIFY_COMPANION.py → VERDICT=PASS (CLAIMS 28/28, 해시 실패 0, P1P2 폐쇄 340/340). PAPER_II 판정 PASS 포함.
- 릴리스 전량(108항목) 임시 재조립에서 verify_numbers.py → NUMERICAL_CHECK=PASS, CHECKS=133, FAILED=NONE.
- SHARED_FROZEN_AUTHORITY_PACKAGE 자체 SHA256SUMS는 편입 파일 전량과 해시 일치.

## 대조값 (Paper II)

- 07 NULLS expected result: DEV97 n_common 83 / q 0.034557629469027 / permutation p 0.000199960007998 / Spearman 0.104525783775 / Rayleigh p 0.971843407824.
- 08 NULLS expected result: dev97 DEV97 Observed Rho 0.104525783775511.
- Paper II 원고: paper2_manuscript_package (릴리스 공유 층의 표 8종과 결합).

## 이상 기록 2건

1. 매니페스트 항목 `SHARED_FROZEN_AUTHORITY_PACKAGE/08_EXPECTED_RESULTS/R26C42G` — 확장자 없는 이름으로 기재됐으나, 기재 해시는 `NULLS\R26C42H\SOURCE_BINDINGS.json`의 내용과 일치한다. 그 정본에서 해시 대조 후 기재된 이름 그대로 편입했다.
2. PACKAGE_ASSET_MANIFEST.csv 2건(SXS_GR·NULLS)은 PAPER_I\MANIFESTS\SOURCE_BUNDLE_MANIFEST.csv와 동일 바이트 — 그 정본에서 편입했다.
3. (공유) PACKAGE_MANIFEST.csv 자체 불일치는 Paper I 패키지 ENTRYPOINT의 이상 기록 참조.
