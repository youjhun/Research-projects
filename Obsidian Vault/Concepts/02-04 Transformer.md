# Transformer (Causal Self-Attention)

> 짧은 spike window에 attention pattern을 적용하는 디코더. 하위 노드: [[02 - BCI Decoding]]

## 구조

- Causal mask: 미래 bin attention = 0.
- 3-layer, 4-head.
- 입력: `(N, 20, 161)` sequential tensor.

## Attention 결과

- L1 peak: 0ms.
- L2 peak: -20ms.
- L3 peak: -10ms.
- 최근 과거 bin에 집중.
- 생물학적 해석:
  - movement 직전 motor buildup 구간에서 spike가 예측력을 가짐.

## SER 구간에서의 특징

- Baseline: MLP보다 약간 낮음.
- SER=1e-2 이상: MLP/LSTM과 gap이 거의 사라짐.
- 가설:
  - high SER에서는 attention이 diffuse.
  - population averaging 효과가 architecture 차이를 덮음.
- 연결: `02 - SER & Error Models`, `03 - Attention Analysis`
