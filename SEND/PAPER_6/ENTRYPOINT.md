# ENTRYPOINT — Paper VI Frequency Timing Geometry (R1)

RIUD Paper VI 공개 패키지. 저자 폴더 MIsCORE_PAPER_VI_FREQUENCY_TIMING_GEOMETRY_R1을 자체 매니페스트 기준으로 전량 재조립한 사본이다. 원본은 수정하지 않았다.

## 구성과 재조립

- 자체 SHA256_MANIFEST 227항목 전량 편입(잔존 8 + 삭제 로그 정본 복원 53 + 이름 탐색 정본 153 + 포렌식 정본 13).
- 루트 문서 8종: README, NUMERICAL_SUMMARY.csv, CLAIM_EVIDENCE_MATRIX.csv, GAP_CAUSAL_MECHANISM_REPORT, FREQUENCY_FAMILY_LAW_SUMMARY, GAP_MECHANISM_FINAL_REPORT, GAP_ALIGNED_A_TF_GEOMETRY_REPORT, FINAL_INDEPENDENT_AUDIT_SUMMARY.
- EVIDENCE 01~20: 소스 바인딩·PROVENANCE가 가리키는 20개 증거 항목(감사·법칙·하위 맵·전환·불일치 포렌식 등).

## 실행 진입점 판정

- 이 패키지는 증거 조립본이다 — MASTER_REPORT 기준 신규 과학 실행·재적합 없음. 패키지 안에 있는 생산 스크립트는 3개뿐이다:
  - EVIDENCE\14_...\03_SOURCE_SCRIPTS\cross_audit_freq_k_abc_geometry.py — 12개 소스 파일 교차 감사.
  - EVIDENCE\14_...\03_SOURCE_SCRIPTS\free_explore_freq_k_abc_geometry.py — 자유 탐색.
  - EVIDENCE\16_MISMATCH_FORENSIC_SELECTED\04_SOURCE_SCRIPTS\assemble_mismatch_forensic.py — 불일치 포렌식 조립.
- 나머지 증거의 생산 스크립트는 PROVENANCE.json이 기재한 20개 소스 디렉터리(PAPER_6·PAPER_7에 생존)에 있으며 패키지 범위 밖이다. 위 스크립트들의 입력 경로는 소스 디렉터리 기준 하드코딩이라 패키지 단독 재실행 진입점은 없다.
- 검증 진입점 = 패키지 매니페스트 전수 대조: 저자 매니페스트 227/227 해시 일치로 재조립을 검증했다.

## 대조값 (NUMERICAL_SUMMARY.csv)

- FREQ_RATE_P = 5.131479928700461e-11; PRETRANSITION_ACC = 0.3956043956043956; POST_G_GAP_P = 0.009900990099009901; GEOMETRY_GLOBAL_PC1_S = 0.34345682137670865.
- H5 재생: MAG 5/5 · SHAPE 4/4 · ABC/GAP 4/4 PASS. H1 rate ratio CI [1.0909, 1.5454].
- CLAIM_EVIDENCE_MATRIX의 경계 표기(NOT_SUPPORTED 항목 포함)를 원문 그대로 유지했다.

## 특이 기록

- EVIDENCE\18·19의 SOURCE_* 파일 5종은 원본 소스 폴더 정본과 동일 바이트(포렌식 정본에서 편입). EVIDENCE\19는 하위 증거 묶음의 재전송 사본이다.
- 보고서 .txt 2건(GAP_CAUSAL_MECHANISM_REPORT.txt, FREQUENCY_FAMILY_LAW_SUMMARY.txt)은 동일 내용 .md 정본과 바이트 동일(포렌식 표 확인) — 정본에서 편입했다.
- FINAL_MISMATCH_FORENSIC_REPORT.md는 EVIDENCE\16의 SOURCE_MISMATCH_FORENSIC_REPORT.md와 동일 바이트다.
