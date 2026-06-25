# Rate Coding vs Temporal Coding

> spike 정보 표현 방식의 두 축. 하위 노드: [[01 - Spike Train & Neural Coding]]

## Rate Coding

- 시간 bin 내 spike 개수 = 정보.
- 장점:
  - 구현 단순.
  - 노이즈 평균화에 강함.
  - SER=1e-2에서도 population averaging으로 robust.
- 단점:
  - spike timing 정보 손실.
  - bin 크기에 민감.

## Temporal Coding

- spike 발생 시각 자체가 정보.
- 장점:
  - timing-sensitive coding 보존.
  - event-driven BCI에서 latency가 중요할 때 유용.
- 단점:
  - sorting 정밀도 의존.
  - hardware jitter에 민감.

## 혼합 전략

- 본 연구의 baseline: Rate coding.
- SER/Attention 연구와의 연결:
  - rate-coded input을 Transformer가 어느 정도 temporal context로 복원하는가?
  - high SER에서 rate-coded가 temporal-coded보다 나은 이유:
    - population count = error dilution.
  - 연결: `02 - BCI Decoding`, `02 - SER & Error Models`
