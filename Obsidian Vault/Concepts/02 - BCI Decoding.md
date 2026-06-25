# Concepts: BCI Decoding

> 스파이크 → 운동 속도/방향으로 매핑하는 디코딩 계열.
> 관련 개념: [[01 - Spike Train & Neural Coding]], [[03 - SER Robustness]], [[05 - Kinematic Consistency]]

## 디코더 계층

| 디코더 | 핵심 아이디어 | 강점 | 약점 |
| --- | --- | --- | --- |
| Ridge | 선형 매핑, L2 정규화 | 빠름, 해석 가능, 칩 이식 적합 | 비선형 표현 불가 |
| MLP | Dual-stream (PCA + Peak feature) | 비선형, burst 민감도 향상 | 저데이터에서 과적합 가능 |
| LSTM | 시계열 순차 처리 | 장기 의존 포착 가능 | short seq에서 overkill |
| Kalman | 상태공간 모델, 예측-보정 | 인과적, 실시간 적합 | 선형·가우시안 가정 |
| Transformer | Self-attention | 장거리 dependency, 생물 temporal pattern | short seq에서 비효율 |

## 평가 지표

- `r (Pearson)`: 선형 상관계수. 스케일 무관.
- `VAF`: 분산 설명율. 스케일 의존.
- `RMSE`: 절대 오차.
- `Scale Bias`: 예측 진폭 / 실제 진폭.
  - amplitude mismatch 문제.
  - 해결: Affine rescaling (train에서 fit).
- `r`과 `R²`는 다름.
  - r=0.93, R²=0.7 정도면 BCI 논문 충분.

## Time-Series CV

- Shuffle 금지. trial 경계 유지.
- leakage가 생기면 SER robustness curve 자체가 무의미.
