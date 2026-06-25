# Experiments: SER Robustness

> Spike error에 따른 디코더 성능 붕괴 곡선 측정.
> 결과 문서: [[Attention-based Neural Decoder: Transformer vs LSTM]]
> 기반 데이터: [[01 - pmd-1 Dataset]]
> 사용 개념: [[02 - SER & Error Models]], [[02 - BCI Decoding]], [[01 - Spike Train & Neural Coding]]

## 실험 Design

- Random SER sweep: [0, 1e-4, 1e-3, 1e-2, 1e-1, 2e-1]
- Burst SER sweep: 같은 grid.
- 각 조건에서 4 디코더 trial-level CV.
- Retention ratio 계산.

## Population Averaging 효과

- N=161일 때 SER=1e-2에서도 retention 0.998 수준.
- 이유:
  - active/bin ≈ 10.
  - corrupted feature fraction ≈ 1% 이하.
  - 노이즈가 population에 희석.
- 주의: 이 효과는 SER=1e-2까지는 유효.
  - SER=5e-2 이상 구간이 보강되어야 breakdown point 정확히 측정 가능.
  - 연결: [[04 - Low-Data Augmentation Quality Gate]]

## Attention + SER overlay

- SER=0 / 1e-3 / 5e-2 / 1e-1에서 attention heatmap overlay.
  - 왜 필요한가:
    - SER=1e-2 이상에서 Transformer와 LSTM 성능이 비슷해짐.
    - Attention pattern이 diffuse 되는지 검증.
  - 이것이 있으면 mechanistic account 가능.
  - 연결: [[06 - Attention Analysis]]

## 미해결 질문

- WHY는 Transformer가 SER=1e-2 이상에서 MLP/LSTM과 비슷한가?
  - 가설 1: population averaging이 architecture difference를 덮음.
  - 가설 2: short seq에서 attention이 의미를 잃음.
