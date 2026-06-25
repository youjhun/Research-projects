# Feature Expansion for Neural Decoding

> 희소한 spike 신호를 decoder가 더 쉽게 활용하도록 변환. 하위 노드: [[01 - Spike Train & Neural Coding]], [[02 - BCI Decoding]]

## 문제

- 3220차원 lagged feature는:
  - 다중공선성 (adjacent bins correlated).
  - neuron별 noise 축적.
  - linear model numerical instability.

## 해결: Feature Engineering

### Dynamic Weighting (Burst Power)

- positive spike count에 exponential-like 변환.
  - `x' = x^burst_power`, 기본 1.3.
- 이유:
  - velocity peak 구간에서 spike rate가 비선형적으로 증가.
  - linear decoder는 peak 구간을 undershoot.
  - 비선형 weighting으로 보정.

### Peak-Aware Features (거시 피처)

- 5가지 추가 피처:
  1. `burst_score`: window 최대 population activity.
  2. `burst_mean`: 평균 activity.
  3. `max_spike`: 최대 single-neuron count.
  4. `active_ratio`: active neuron 비율.
  5. `onset_ratio`: 최근 50ms / 과거 150ms activity.
- 역할:
  - MLP가 peak, acceleration onset을 explicit signal로 학습.
  - deep feature와 shallow feature를 각각의 stream으로 융합.

### PCA (차원 축소)

- 3220차원 → 128차원.
- 상위 PC: 운동 신호.
- 하위 PC: noise.
- leakage 방지:
  - PCA는 train split에서만 fit.
  - test split에는 transform만 적용.
- 연결: `02 - BCI Decoding`
