# Temporal Integration & Motor Lag

> spike가 운동으로 구현되기까지의 시간 지연 보정. 하위 노드: [[01 - Spike Train & Neural Coding]], [[02 - BCI Decoding]]

## Motor Lag

- Spike onset → velocity 반응까지 약 100\~200ms.
- 원인:
  - cortical processing delay.
  - muscle activation delay.
  - 측정/전송 delay.
- 결과:
  - t시점 spike로 t시점 velocity를 예측하는 것은 causal mismatch.

## Time-Lag / Tap-Delay Line

- 현재 시점 t를 기준으로 과거 `num_lags` bins만큼 묶어 입력.
  - `num_lags=20` → 200ms window.
- shape: `(N - 20, 20 × 161) = (N - 20, 3220)`
- 효과:
  - model이 spike→movement의 temporal delay를 학습.
  - spike count 하나만 쓰는 것보다 성능 대폭 향상.

## Window 크기 선택

- 너무 작음: motor lag이 window 밖으로 나감.
- 너무 큼: 다중공선성 증가, irrelevant history 포함.
- 현재 선택: 20 bins = 200ms.
  - 이 값은 SER, attention 분석에서도 고정되어야 함.
- 연결: `02 - BCI Decoding`
