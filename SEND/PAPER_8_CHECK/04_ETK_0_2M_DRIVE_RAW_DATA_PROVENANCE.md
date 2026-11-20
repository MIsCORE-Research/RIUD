# ETK 0–2M 확장 실행 원시 데이터 계보 및 감사 범위 명세 (Drive Provenance)

- **감사 일시**: 2026-11-20
- **대상 수치**: `ETK 0–2M trapezoid recovery = 99.151%` (Paper VIII §10.5)
- **보관 위치**: 구글 드라이브(Google Drive) 및 `E:\SEND\PAPER_8_CHECK`

---

## 1. 0–2M 시뮬레이션 원본 실행 확인 (Confirmed Execution)

구글 드라이브 및 로컬 대조를 통해 0–2M 확장 시뮬레이션의 파라미터 파일 및 원시 출력 데이터(Raw Output)가 실존함을 확인했습니다.

### 1) 확인된 원본 파일 목록
- **run-2M-local-phase-20260910.par** ([Drive 링크](https://drive.google.com/open?id=1tLxCyAKboa8w3_VQLECmI58en3guuoNh)):
  - 0–2M 시뮬레이션 실행 파라미터 파일 (`Cactus::cctk_final_time = 2.0`)
  - SHA-256: `20AEA9F1A4614271C0EC8ED9C1893E5898330626EDF04380CB716D9D42368FDD`
- **weylscal4-psi4r_group.maximum.asc** ([로컬 보관](file:///E:/SEND/PAPER_8_CHECK/weylscal4-psi4r_group.maximum.asc)):
  - $t = 0.00 \sim 2.00M$ (0 ~ 1024 iters, $\Delta t = 0.03125$)
  - Run ID: `run-run-2M-local-phase-20260910-DESKTOP-8EFF2TR.localdomain-mickey-2026.09.10-13.50.35-869`
- **quasilocalmeasures-qlm_shapes.x.asc** ([Drive 링크](https://drive.google.com/open?id=1GtLNvR77rT_xEVSnepeaU-LbDhbDqRMN) / [로컬 보관](file:///E:/SEND/PAPER_8_CHECK/quasilocalmeasures-qlm_shapes.x.asc)):
  - 지평면 좌표 형상(coordinate shape) 시계열 ($t = 0 \to 2M$)
- **quasilocalmeasures-qlm_shapes.y.asc** ([Drive 링크](https://drive.google.com/open?id=17cbZuRYAzmB0dvx8bI6bFlfYhldWPU3P))
- **quasilocalmeasures-qlm_newman_penrose.x.asc** ([Drive 링크](https://drive.google.com/open?id=1qp0VJ-FjVThggTlq3DnBbY_wetfJy61v)):
  - QuasiLocalMeasures가 출력한 Newman-Penrose 관련 스칼라 시계열
- **N16_AHFINDER_SPHERICALSURFACE_GEOMETRY_PROVENANCE_AUDIT.md** ([Drive 링크](https://drive.google.com/open?id=1XQxBEsHIGovKL48sh8yJeN77ovUKJ3gi)):
  - AHFinderDirect, SphericalSurface, QLM 간 형상 전달 및 기하학적 수렴성 감사 문서

---

## 2. 감사 한계 및 미수행 사항 (Limitations & Non-Executed Scope)

본 감사는 원본 실행 및 데이터의 실존 여부를 추적한 것이며, **원시 데이터로부터 99.151% 수치를 독립적으로 재적분·재계산(re-evaluation)하여 검증한 것이 아닙니다.**

1. **플럭스 매핑 미검증**:
   - `qlm_newman_penrose` 파일의 개별 컬럼이 Ashton-Krishnan(AK) 밸런스 식의 전단($\sigma$) 및 팽창($2\zeta$) 플럭스에 어떤 가중치와 게이지 정규화로 매핑되는지 본 감사 단계에서 엄밀히 분해·검증하지 않았습니다.
2. **고유 면적 반경(Areal Radius) 미산출**:
   - `qlm_shapes.x`에 기록된 수치는 39개 각도 그리드상의 좌표 반경($r_{\text{coord}}$)이며, 실제 물리적 지평선 팽창량 $\Delta R_{\text{obs}}$를 구하기 위해서는 2차원 유도 계량($q_{ab}$)을 적분하여 얻는 고유 면적 반경($R = \sqrt{A / 4\pi}$)이 필요합니다. 본 보고서에서는 이를 직접 적분하여 수치적 $\Delta R_{\text{obs}}$를 산출하지 않았습니다.
3. **적분 재계산 미수행**:
   - 시간 축($t = 0 \to 2M$)에 따른 사다리꼴 적분값($\Delta R_{\text{pred}}$) 및 관측 팽창량($\Delta R_{\text{obs}}$)의 구체적인 수치와 둘의 나눗셈 계산 과정을 본 보고서가 직접 산출하여 제시하지 않았습니다.

---

## 3. 결론 및 논문 수치에 대한 판단

1. **2M 원본 실행 확인**: 2M 시뮬레이션이 실제로 수행되었고 원시 데이터가 보존되어 있음은 확인되었습니다.
2. **재계산 검증 비성립**: 본 보고서가 원시 데이터를 사후 재적분하여 99.151%를 독립적으로 재현·검증한 것은 아니므로, 이를 "99.151% 완벽 확증"으로 서술하지 않습니다.
3. **논문 수치 유지**: 논문의 99.151%는 0–2M 확장 시뮬레이션의 고유 결과입니다. $0.25 \sim 0.50M$ 3점 벤치마크 수치(`99.1929%`)는 다른 구간의 결과이므로 이를 대체할 수 없으며, 본 보고서의 감사 결과를 근거로 논문의 99.151% 수치를 변경해서는 안 됩니다.
