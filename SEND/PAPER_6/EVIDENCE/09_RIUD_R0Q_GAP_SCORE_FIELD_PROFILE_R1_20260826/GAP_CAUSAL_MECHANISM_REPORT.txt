# GAP SCORE-FIELD CAUSAL MECHANISM AUDIT R1

## 결론

GAP은 단순히 10 ms grid가 비워 만든 틈으로 확인되지 않았다. frozen map에서
앞 상태의 sharp local-frequency peak가 끝나고 뒤 상태의 peak가 나타나는 사이에,
중간층의 후보 지지가 일시적으로 사라지거나 양쪽을 연결할 주파수 후보가 없어지는
**ridge handoff / support-connection trough**가 반복된다.

이것이 현재 자료에서 확인되는 가장 구체적인 원인이다. 이는 representation-level
원인이며, 이 audit만으로 실제 raw 물리량의 원인(진폭 감소, mode interference,
mode redistribution 등)을 특정했다고 말하지 않는다.

## 수치 근거

- 감사 대상: 15 frozen path large-gap edges; 중간 10 ms layers: 16
- 후보 자체 소실: 8/15 edges. 모든 중간층에서 z>=1 후보 0개.
- 후보는 있으나 연결 불가: 7/15 edges. z>=1 후보는 존재하지만, 7/7에서 predecessor와 successor 양쪽에 동시에 주파수 jump <=60 Hz인 bridge 후보 0개.
- 중간층 max-z가 양 끝 중 작은 값보다 낮은 층: 13/16.
- 중간층 max-z 범위: 0.853281 .. 1.317389.
- candidate-extinction 중간층 max-z 범위: 0.853281 .. 0.999436.
- 시간 gap: 20 ms edges 14개, 30 ms edge 1개. 따라서 단일 10 ms spacing만으로 설명되지 않는다.

## 두 메커니즘

### 1. score-field extinction
GW230606_004305 [-0.08,-0.06), GW230708_053705 [-0.01,0.01), GW230712_090405 [-0.04,-0.02), GW230919_215712 [-0.09,-0.07), GW231005_021030 [-0.03,-0.01), GW231118_090602 [-0.11,-0.09), GW231223_032836 [-0,0.02), GW240413_022019 [-0.02,-0)

중간층의 최고 network-z가 0.853281~0.999436으로 frozen candidate threshold 1.0 아래에
있다. 즉 해당 시간에는 local peak/persistence 조건을 만족하는 node가 생성되지 않는다.

### 2. ridge relocation without bridge
GW230712_090405 [-0.02,-0), GW230922_040658 [-0,0.02), GW231004_232346 [-0.03,-0.01), GW231005_091549 [-0.07,-0.05), GW231018_233037 [-0.07,-0.05), GW231020_142947 [-0.03,-0.01), GW231118_005626 [-0.01,0.02)

중간층에는 z>=1 후보가 2~6개씩 존재하지만, 양 끝 path node를 동시에 잇는 후보가
없다. 따라서 점수가 완전히 없는 것이 아니라, 기존 ridge와 새 ridge가 frozen path의
주파수 연속성 조건 안에서 연결되지 않는다.

## 왜 특정 구간인가

그 구간이 두 상태의 경계이기 때문이다. path predecessor는 한 주파수/폭 phenotype에
있고 successor는 다른 phenotype으로 이동한다. 그 사이에는 (a) peak contrast가
threshold 아래로 눌리거나, (b) peak가 다른 주파수로 이동해 양쪽을 동시에 연결할
후보가 사라진다. 그래서 GAP은 임의 grid cell의 빈칸이 아니라, frozen score field가
한 ridge에서 다른 ridge로 넘어가는 동안 생기는 support trough로 나타난다.

## 경계

현재 결과는 왜 map/node가 비는지에 대한 frozen-observable 구조적 원인을 규명한다.
raw amplitude/phase/mode/energy를 이 파일에서 직접 계산하지 않았으므로 그 trough의
underlying physical cause까지 확정하지 않는다.

NO_NEW_NODE_DISCOVERY=TRUE
NO_NEW_PATH_RULE=TRUE
NO_REFIT=TRUE
HOLDOUT30_ACCESSED=FALSE
