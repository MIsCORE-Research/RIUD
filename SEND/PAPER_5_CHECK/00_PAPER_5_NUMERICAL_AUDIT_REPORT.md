# RIUD 논문 Paper V Short-Track 분기 수치 감사 및 원본 데이터 복원 보고서

- **감사 일시**: 2026-11-20
- **대상 수치**: Paper V §6 Short-Track 예외 분기 통계
  - 2×2 분할표: Short-track 7/0 vs Non-short-track 0/89 (총 96개 사건)
  - 단측 피셔 정확 검정(One-sided Fisher Exact Test): $p = 8.38983011 \times 10^{-11} \approx 8.3898 \times 10^{-11}$
  - 순열 검정(99,999-permutation test): $p = 1.0 \times 10^{-5}$
  - 스핀 비대칭성 중앙값: $0.458208$
- **보관 위치**: [E:\SEND\PAPER_5_CHECK](file:///E:/SEND/PAPER_5_CHECK/)

---

## 1. 배경 및 분리 보관 원인 규명

- **논문 기재 사실**:
  Paper V 본문 제6절 및 요약문에서 *"All seven exact short-track events are the seven events with GAP>t0, while no non-short-track event has GAP>t0 (one-sided Fisher p=8.3898e-11; permutation p=1e-5)."* 라고 명시되어 있습니다.
- **분리 보관 원인**:
  초기 `SEND/PAPER_5` 배포 패키지(128개 파일)는 전역 R40 시계 및 동결 룰셋 중심의 최소 단위로 패키징되면서, 해당 2×2 분할표 및 피셔 검정 결과 파일이 연구 마스터 코퍼스(`E:\ARCHIVE\...\09_RAW_RESULT_TABLES\`)에 보관되고 `SEND/PAPER_5` zip 패키지 생성 시점에는 복사되지 않았습니다.

---

## 2. 복원된 원본 파일 명세

마스터 아카이브로부터 확인된 원본 데이터를 경량 CSV 형태로 [E:\SEND\PAPER_5_CHECK\](file:///E:/SEND/PAPER_5_CHECK/)에 직접 배치하여, 외부 연구자가 저장소 내에서 즉시 1-클릭으로 확인할 수 있도록 조치 완료했습니다.

1. [GAP_POST_T0_SHORT_TRACK_2X2.csv](file:///E:/SEND/PAPER_5_CHECK/GAP_POST_T0_SHORT_TRACK_2X2.csv):
   ```csv
   GROUP,GAP_POST,GAP_PRE,TOTAL
   SHORT_EXACT,7,0,7
   NONSHORT,0,89,89
   ```

2. [GAP_POST_T0_SHORT_TRACK_STATS.csv](file:///E:/SEND/PAPER_5_CHECK/GAP_POST_T0_SHORT_TRACK_STATS.csv):
   ```csv
   N_TOTAL: 96
   N_SHORT_GAP_POST: 7, N_SHORT_GAP_PRE: 0
   N_NONSHORT_GAP_POST: 0, N_NONSHORT_GAP_PRE: 89
   FISHER_P_ONE_SIDED: 8.389830113725958e-11
   PERM_P_ONE_SIDED: 1e-05 (N=99,999)
   SHORT_SPIN_POST_MEDIAN: 0.4582079579083361
   ```

---

## 3. 결론

Paper V의 `Fisher p = 8.3898e-11` 및 `permutation p = 1e-5`는 완벽한 원본 실측 데이터(`GAP_POST_T0_SHORT_TRACK_STATS.csv`)를 기반으로 한 참값이며, 본 검증 폴더 배치를 통해 저장소 내부에서 완전한 재현과 확인이 가능하도록 해결되었습니다.
