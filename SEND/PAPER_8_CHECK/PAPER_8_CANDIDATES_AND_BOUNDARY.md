# CANDIDATES AND BOUNDARY — Paper VIII

## 1. 실행셋 확정 불가 선언

원본 트리의 PAPER_8 아래 147개 폴더 중 어느 것도 "Paper VIII 실행셋"으로 자기 지정돼 있지 않다(실행셋 선언 파일·루트 매니페스트 없음). 따라서 실행셋 전체의 조립은 하지 않았고, 본문 결합(§7 C01 인용, §10 provenance 8분류, 부록 B ETK 벤치마크)과 자체 매니페스트를 갖춘 종단 폴더들로 확정 가능 범위만 조립했다. 실행셋 전체의 확정은 저자 확인 항목으로 남는다.

## 2. 버킷 분류 (2026-10-27 실측, 147개)

- 실행 코드(.py) 보유: 61개
- 결과만 보유: 78개
- 공실: 8개 — MIsCORE_RAW_ONLY_OPEN_TEMPORAL_PHYSICAL_DISCOVERY_R0/R2, MIsCORE_RAW_ONLY_STATE_FINGERPRINT_R0, MIsCORE_TEOBPM_MT_PUBLISHED_TIME_CROSSWALK_R0, RIUD_DETECTOR_TO_R10G_PATH_PERTURBATION H1_ONLY_FOUR_EVENT_1WORKER(+_WORK), RIUD_GAP_RAW_FROZEN_FEATURE_MATCHED_WINDOW_AUDIT_R1, mpi-test3-recovered.

코드 보유 폴더 중 편입한 것: R8 물리 메커니즘 종단, R7F3, MECHANISM_REPLICATION_R1, R13, R14, R15, GAP_ALIGNED_MEMORY_LOCALIZATION, ETK 소스 감사 트리(벤치마크 결합만 추출). 결과만 폴더 중 편입한 것: R9_99EVENT_LAW_DISCOVERY(자체 매니페스트 보유).

## 3. C01 인용 결합 범위

- 본문 §7.1: 복구 연산자 = 원본 작업 트리의 run_eventwise_full_tf_change_separate.py, SHA-256 26B9F63F…EF45 → 실물 특정·해시 전자리 일치·편입 완료(OPERATORS\).
- 본문 §7.4: R0 생산자 byrun_raw_full_tf_change_landmarks.py → 전수 목록(포렌식 분류 533,512행 — E: 전역이 범위, 드라이브 미러 목록, E: 열거)과 원본 작업 트리 라이브 탐색에서 미발견. 미편입 — 이름과 역할만 본문에 근거해 기록한다.
- 복구 provenance(RECOVERY_PROVENANCE.md): 복원본은 재작성이 아니라 원본 스크립트이며 복원 해시가 본문 부록 B와 동일 — ETK_EXACT_BENCHMARK\recovered_exact\에 편입.

## 4. 미편입 주요 후보와 사유

- MIsCORE_RIUD_COMMON_HORIZON_RELAXATION_PHASE_R11 (6,529파일, .py 4,281): .py 대부분이 벤더링된 실행 환경 복사본이라 핵심 코드 특정 불가. REPLICATION의 입력 중 하나로 본문에 닿으나, 폴더째 편입은 추측 조립이 되어 제외하고 후보로 기록.
- PURE_GR_INJECTION_END_TO_END 계열(각 약 3.1~3.3GB)과 RIUD_DEV99 계열 다수: Paper VIII 본문의 증거가 아니라 상류 GR 대조·주입 실행 트리. 패키지 범위 밖으로 판정.
- GR_COARSEGRAINED_MEMORY_CLOSURE 계열(R7, R7F1, R7F2): R7F3의 상류 단계들. R7F3 패키지에 그 입력 마스터 CSV가 포함돼 있어 체인 하단은 닫히고, 상류 폴더들은 후보로 기록.
- MIsCORE_R6P9_EXECUTABLE_GR_CONTRACT_RECOVERY_R0 (27파일, .py 7): R7F3 입력(R6P9 마스터)의 계약 복구 폴더 — 후보로 기록.
- MIsCORE_ETK_DH_RERUN_SOURCE_AUDIT_R0 전체(26,671파일, 16.6GB): 소스 감사 트리. 본문 부록 B 결합 파일만 ETK_EXACT_BENCHMARK\로 추출했다.

## 5. 제외·외부 결합 규칙

- R8의 SXS 원본 .h5 79개 파일 제외: 외부 공개 수치상대론 데이터(SXS 카탈로그)이며 본문도 계약 기반 참조로 취급한다. SOURCE_INDEX.csv·DOWNLOAD_PROVENANCE.json·PROVENANCE.json·카탈로그별 metadata.json·Strain_N2.json·LICENSE 메모는 편입.
- cactus_cactus_sim (958,999,000B): 해시 외부 결합. 생존 위치 = MIsCORE_ETK_DH_RERUN_SOURCE_AUDIT_R0\gw150914-einstein-toolkit\qc0-b03-dh-0p5-sigma-dense-ah-20260909-waveform-rerun-20260910\bin\cactus_cactus_sim. 실측 SHA-256 9dfd62b8…12a — 본문 부록 B 및 파형 패키지 매니페스트 기재와 일치.
- 핸드오프 노트와 실행 로그(.log)는 전 패키지 공통 제외 규칙(3차와 동일).
- 파형 출력 대용량(output\ 하위 .h5·asc 등)은 제외하고 예상값·검증 문서만 편입.

## 6. R7F3 매니페스트 복구 기록

- R7F3 자체 매니페스트 기재 파일 중 4건은 원래 위치에서 소실됐으나, 삭제 로그의 정본 추적으로 동일 내용(해시 전자리 일치) 생존본을 찾아 편입했다:
  - R7F2_GR0_R6P9_IDENTITY_AUDIT.csv ← R7F2 폴더의 R7F2_GR0_EVENTWISE_REPLAY.csv (동일 내용)
  - R7F3_EVENTWISE_CONDITIONAL_LL.csv ← R7F3_OUTER_HELD_EVENT_RESULTS.csv (동일 내용)
  - R7F3_FULL_RIUD_PLUS_GR_AUGMENTATION.csv ← R7F3_MEMORY_ABLATION_SUMMARY.csv (동일 내용)
  - R7F3_FINAL_REPORT.md ← 같은 폴더 핸드오프 노트 사본 (동일 내용 — 삭제 당시 정본으로 지정된 사본)
- R7F3 사본의 자체 매니페스트 대조: 20/23 일치. 나머지 3건은 제외 규칙(실행 로그 2, 핸드오프 노트 1)이다.

## 7. 본문 provenance 8분류 대응

§10의 8분류(prior frozen RIUD map/GAP/R40 · RAW branches · SXS10/SXS5/SXS15 · two-anchor bridge · ETK dynamical-horizon + Psi4 · B06 forward branch · posterior-conditioned GW150914 analogue · recovered R0 operator) 중 패키지가 직접 닫는 범위: recovered R0 operator(C01), ETK dynamical-horizon(벤치마크 결합), SXS 계열(R8·R13의 소스 네이티브 산출과 인덱스). 나머지는 상류 동결 패키지(Paper IV·V·VII 공개본)와 소스 디렉터리를 가리키는 참조 결합으로 남는다.
