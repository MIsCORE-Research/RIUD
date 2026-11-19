# ENTRYPOINT — Paper I Numerical Companion (R1)

RIUD Paper I 공개 패키지. 정본 사본이며 원본(E:)은 수정하지 않았다.

## 구성

- 루트: 저자 클레임-증거 컴패니언(2026-08-18)의 PAPER_I 슬라이스 전량 — 컴패니언 SHA256SUMS의 PAPER_I 항목 53/53. 하위: INPUTS(동결 스냅샷·권위 스펙·잠금 계약), FROZEN_DISTRIBUTION(R10J 타이밍/주파수 카운트·게이트), MAGNITUDE_SHAPE(HOLDOUT5 종단·해저드·스케일), AUDITS, MANIFESTS(SOURCE_BUNDLE_MANIFEST.csv 포함), PAPER_I_CLAIM_NARRATIVE·CLAIM_EVIDENCE_MATRIX.
- COMPANION_ROOT\: 컴패니언 루트 공유 문서 9종 + 00_AUDIT 4항목 + INTEGRATED 5항목(전 논문 공유 층이라 I·II 패키지 양쪽에 동일하게 포함).
- SHARED_NUMERICAL_RELEASE_PAPER_I_II\: 숫자 릴리스의 PAPER_I_II 블록 16항목 전량 + RELEASE_ROOT\(릴리스 README·PACKAGE_SCOPE·verify_numbers.py).

## I·II 분리 판정

숫자 릴리스는 I·II를 `01_NUMERICAL_RESULTS/PAPER_I_II` 단일 블록으로만 결합한다(릴리스 설계상 분리 없음 — verify_numbers.py의 ORIGIN 검사가 이 블록을 한 단위로 센다). 따라서 릴리스 층은 분리 불가로 판정해 공유 층으로 양 패키지에 포함했고, 청구-증거 층(컴패니언)은 논문별로 분리 가능해 PAPER_I 53항목을 본 패키지의 본체로 조립했다.

## 검증 (사본 재조립 실행)

- 컴패니언 전량(987항목)을 임시 재조립해 동봉 VERIFY_COMPANION.py 실행 → 종료 코드 0, VERDICT=PASS, CLAIMS_PASS=28/28, HASH_FAIL=0, P1P2 권위 해시 폐쇄 340/340, MISSING19 복구 19/19, PAPER_I~IV 전 판정 PASS. 저자 기록 VERIFY_COMPANION_RESULT.txt와 동일.
- 릴리스 전량(108항목) 임시 재조립에서 verify_numbers.py 실행 → 종료 코드 0, NUMERICAL_CHECK=PASS, CHECKS=133, FAILED=NONE.

## 대조값 (Paper I)

- 동결 분포(374 이벤트): FAIL 31 / PASS 162 / STRONG_PASS 150 / VERY_STRONG_PASS 31.
- 타이밍 윈도우 W1–W4 hazard 배율 1.371953262430, 로그우도 이득 31.165977028298.
- 주파수 윈도우: 정확 이항 p 2.36536443692032e-05, KS p 0.000288636135170212, rate ratio 1.30738373303485.
- 규모·형상: Spearman 0.342974072052, p 8.77275956124e-12 / KS 0.180544, p 3.63188149582e-09.
- Paper II 지표 결합: 물리 중첩 타이밍 정확 p 0.0402254.

## 이상 기록 1건

COMPANION_ROOT\PACKAGE_MANIFEST.csv: 컴패니언 SHA256SUMS는 이 파일의 해시를 d239efde…(217,698B)로 기재하나, 생존 원본 실측은 7718a4dc…(217,827B)다 — 합 동결 이후 CSV 자체가 재생성·확장된 흔적이다. 패키지에는 생존 원본을 그대로 넣었고, VERIFY_COMPANION 판정은 이 항목에 의존하지 않는다(전량 재조립 PASS로 확인).
