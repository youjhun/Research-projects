# Experiments: Baseline Decoding

> 디코더 간 성능 비교 실험 (SER=0 기준)
> 결과 문서: [[Attention-based Neural Decoder: Transformer vs LSTM]]
> 기반 데이터: [[01 - pmd-1 Dataset]]
> 사용 개념: [[01 - Spike Train & Neural Coding]], [[02 - BCI Decoding]]

## 실험 Design

- 4 디코더 비교: Ridge / MLP / LSTM / Kalman
- 5-Fold trial-level CV
- SER=0 (noise 없음)

## 입력

- Ridge, MLP: lagged dynamic feature (20 lags × 161 dims)
- LSTM: sequential feature (N, 20, 161)
- Kalman: raw observation (N, 161)

## 핵심 결과 (trial-level CV)

| Decoder | r_neural | VAF | Scale Bias |
| --- | --- | --- | --- |
| Ridge | 0.8701 | 0.740 | 0.856 |
| MLP | 0.9209 | 0.842 | 0.880 |
| LSTM | 0.8945 | 0.789 | 0.842 |
| Transformer | 0.9097 | 0.819 | 0.813 |
| Paper SNN | 0.9324 | — | — |

## 해석

- MLP가 baseline 최고.
- Transformer는 baseline MLP보다 약간 낮음.
  - short seq(T=20)에서는 attention이 overkill.
  - SER 구간에서 MLP와 gap이 줄어드는 이유 분석이 필요.
  - 연결: [[03 - SER Robustness]]
