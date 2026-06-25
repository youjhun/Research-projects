# Experiments: Attention Analysis

> Transformer attention의 시공간 집중 패턴 분석.
> 결과 문서: [[Attention-based Neural Decoder: Transformer vs LSTM]]
> 기반 데이터: [[01 - pmd-1 Dataset]]
> 사용 개념: [[02 - BCI Decoding]], [[02 - SER & Error Models]]

## 구조

- `CoralTransformerDecoder` (학습용)
- `CoralTransformerWithAttn` (시각화용)
  - `forward_with_attn()` 메서드로 attention weight 반환.
  - 학습된 weight만 로드해서 inference-only 호출.
  - 연결: [[06 - SER × Attention Analysis]]

## 결과

| Layer | Attention @ now | Peak lag |
| --- | --- | --- |
| L1 | 0.0670 | 0 ms |
| L2 | 0.0612 | -20 ms |
| L3 | 0.0702 | -10 ms |

- 최근 과거 bin에 집중.
- 생물학적 해석: movement 구동 직전 motor buildup.

## 추가되어야 할 비교

- SER=0 / 1e-3 / 5e-2 / 1e-1 overlay.
- high SER일수록 attention이 diffuse 되는지 검증.
- LSTM hidden state attention 유사성 비교.
  - 연결: [[Experiments - SER Robustness]]
