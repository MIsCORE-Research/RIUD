# ENTRYPOINT — Paper VIII Mechanism Evidence (R1)

RIUD Paper VIII 공개 패키지. Paper VIII은 단일 실행셋 폴더를 자기 지정하지 않는다 — 본 패키지는 본문(§7 복구 연산자 인용, §10 provenance 8분류, 부록 B ETK 정확 벤치마크 결합)이 닿는 확정 가능 범위를 증거로 조립한 것이다. 확정 불가 항목과 후보는 CANDIDATES_AND_BOUNDARY.md에 남겼다. 정본 사본이며 원본은 수정하지 않았다.

## 구성과 진입점

- OPERATORS\run_eventwise_full_tf_change_separate.py — 본문 §7.1이 인용한 복구 연산자 C01. SHA-256 26B9F63F55D39C715E6DE907F7759A04C9C7427F7F039FDA9507A4AFBF76EF45 (본문 기재·감사 실측과 전자리 일치).
- R8_PHYSICAL_MECHANISM_CLOSURE\ — R8 물리 메커니즘 종단. 진입점: BUILD_R8_AUDIT.py, R8_MECHANISM_CLOSURE_TEST.py, R8_RUN_SECONDARY_MECHANISM.py, R8_FINALIZE_ACTIVE_AUDIT.py. 자체 매니페스트 대조 32/32 (핸드오프 노트 제외 규칙 1건). SXS 원본 .h5는 제외하고 인덱스·메타데이터·provenance만 편입(아래 경계 참조).
- R7F3_GR_MEMORY_CONDITIONAL_CLOSURE\ — 진입점 RUN_R7F3.py → FINALIZE_R7F3.py (REPORT_ONLY_R7F3.py는 보고 전용 변형). 입력 R6P9_DIRECT_SOURCE_ROW_MASTER_WITH_FROZEN_HAZARD.csv 포함. 자체 매니페스트 대조 20/23 일치 (소실 4건은 동일 내용 정본으로 복구, 경계 문서 §6 참조).
- MECHANISM_REPLICATION_R1\ — 진입점 build_replication.py 외 감사 스크립트 24개. 자체 매니페스트 대조 104/104.
- R13_SXS_NATIVE_MAP_RELAXATION\ — run_r13.py. 매니페스트 7/7 (핸드오프 노트 제외 1건).
- R14_EXTENDED_W0_W5_JOIN\ — join_row_score_interval.py. R15_EXTENDED_W0_W5_CONDITIONAL\ — build_conditional.py.
- GAP_ALIGNED_MEMORY_LOCALIZATION\ — RUN_GAP_ALIGNED_WINDOW_STATE.py 외 RUN_* 4개. 매니페스트 19/19.
- R9_99EVENT_LAW_DISCOVERY\ — 결과·법칙 패키지(코드 없음, 자체 매니페스트 23/23).
- ETK_EXACT_BENCHMARK\ — 본문 부록 B 결합. waveform_package\(파형 재현 패키지: run_waveform_exact.sh, 자체 매니페스트, 예상 수렴 CSV, QLM 소스 타르볼), exact_package\(run_exact.sh·복구 provenance), recovered_exact\(RECOVERY_PROVENANCE·매니페스트), dense_benchmark_par\(본문 기재 PARFILE_SHA256 32AD4496…와 일치하는 밀집 par 파일 실물).

## 대조값

- C01 SHA-256: 26B9F63F…EF45 (본문·실측 일치).
- ETK 밀집 par 파일 SHA-256: 32AD449642C8282D6F9E5F8FF8848AA84B3BA34943E9E44E60F51A202C24F547 (본문 부록 B 기재와 일치).
- ETK 실행 바이너리 cactus_cactus_sim: 패키지에 넣지 않고 해시로 외부 결합 — SHA-256 9dfd62b8e9cbd057422e13f1e090c55828985079b07f40f18f3a93083760a12a (본문·파형 패키지 매니페스트·생존본 실측 3자 일치, 958,999,000B). 생존 위치는 경계 문서에 기록.
- R8 최종 판정(R8_FINAL_REPORT): R8_OVERALL_STATUS=PASS_ACTIVE_MECHANISM_CAMPAIGN, 단 MICROSCOPIC_ORIGIN=UNRESOLVED, DIRECT_GR_DERIVATION=NOT_ESTABLISHED, NEXT=STOP_AND_FREEZE — 본문이 주장하지 않는 경계 그대로다.
- 본문 대표값: map consistency 13/13; fixed-path projection 0/100,000 (p=9.9999e-06); 방향 비등가 0/9,999 (p=0.0001); 스케일 반전 +0.4373 (10ms) → −0.7916 (80ms).
