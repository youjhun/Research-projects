# Experiments: Attention Analysis

> Transformer가 spike window를 해석하는 시공간 패턴 분석.
> 결과 문서: [[Attention-based Neural Decoder: Transformer vs LSTM]]
> 기반 데이터: [[01 - pmd-1 Dataset]]
> 사용 개념: [[02 - BCI Decoding]], [[05 - Kinematic Consistency]]

## 구조

- `CausalTransformerDecoder` (학습용, fast)
- `CausalTransformerWithAttn` (시각화용, need_weights=True)
- 학습 후 weight만 로드해서 attention 추출.

## 현재 결과

| Layer | Attention @ now | Peak lag |
| --- | --- | --- |
| L1 | 0.0670 | 0 ms |
| L2 | 0.0612 | -20 ms |
| L3 | 0.0702 | -10 ms |

- 현재 bin과 최근 과거 bin에 집중하는 경향.
- 생물학적 해석: 운동 실행 직전 motor buildup 구간 집중.

## 추가되어야 할 분석

- SER 조건별 attention 변화.
  - baseline SER=0 vs SER=5e-2 vs SER=1e-1 overlay.
  - noise가 많아질수록 attention이 diffuse 되는가?
- Layer별 temporal shift:
  - shallow layer = 먼 과거, deep layer = 최근.
  - 계층적 temporal integration의 증거.
- 연결: [[03 - SER Robustness]], [[06 - Low-Data Augmentation Quality Gate]]
