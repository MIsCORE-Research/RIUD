# KNOWN GAPS — Paper III Independent Replication

메우지 않고 기록만 한다. (공개본 제작 지침: 입력 폐쇄성 결함은 보완하지 않는다.)

## 1. 입력 폐쇄성 결함 — 외부검증 RAW 이벤트 5건 미발견

- 감사 기록(INPUT_CLOSURE_AUDIT): INPUT_CLOSURE_INCOMPLETE — 기대 RAW 29건 중 24건 회수, 5건 미발견. 러너 상태 NOT_YET_FULLY_VALIDATED.
- 미발견 이벤트 5건:
  - GW241109_033317
  - GW241230_233618
  - GW241230_084504
  - GW240530_012417
  - GW240916_184352
- 본 제작의 복구 과정(삭제 로그 정본 추적·이름 탐색·포렌식 정본 대조)에서도 이 5건의 RAW 입력은 발견되지 않았다.
- 영향 범위: 최종 비교·판정 산출 자체는 정본이 생존한다(CLAIM_EVIDENCE 참조). 결함은 "입력이 전량 닫혀 있지 않다"는 재현 폐쇄성의 한계로 남는다.

## 2. 외부 패키지의 단계 폴더 공실

- 원본 패키지 RIUD_INDEPENDENT_REPLICATION_FINAL_20260805의 단계 폴더들(00_SOURCE_SNAPSHOT, 02_DESIGN_LOCK, 04_FINAL_COMPARISON, 07_MANIFESTS, 08_SHA256, 99_ORIGINAL_PATH_RECORDS 등)은 2026-10-27 정리 이후 공실이다.
- FINAL 패키지의 work\ 폴더는 삭제 로그에 기록이 없어, 삭제된 것이 아니라 조립 시점부터 비어 있었던 것으로 판정했다.
- 단계 산출의 정본은 컴패니언 PAPER_III 슬라이스(본 패키지 CLAIM_EVIDENCE)와 PUBLIC_MASTER R2에 생존한다.

## 3. 범위 제외 (결함 아님)

- Paper III 런타임 트리(118,855개 파일, 대조군 13,000 등)는 저자 릴리스 범위에서 원래 제외됐다(컴패니언 README의 릴리스 범위 선언). 본 패키지의 제외는 그 설계를 따른 것이다.
