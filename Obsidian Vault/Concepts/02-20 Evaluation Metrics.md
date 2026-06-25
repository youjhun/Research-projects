# Evaluation Metrics

> 디코딩 성능을 측정하는 지표 계열. 하위 노드: [[02 - BCI Decoding]], [[Experiments - Baseline Decoding]]

## 핵심 지표

### Pearson r

- 선형 상관관계의 강도 + 방향.
- 스케일에 불변.
- 단점: 비선형 관계는 검출 못함.
- BCI에서 가장 자주 쓰임.

### R² (Coefficient of Determination)

- 분산 설명율.
- 스케일 의존.
- `r`과 `R²`는 다름:
  - `r=0.93`, `R²=0.7` 같은 경우가 흔함.
  - BCI에서 R² 0.7 이상이면 매우 좋음.

### VAF (Variance Accounted For)

- 여러 논문에서 R²와 유사하게 사용.
- `VAF = 1 - var(y - ŷ) / var(y)`.
- R²와 거의 동일.

## 해석 기준

| 지표 | 의미 |
| --- | --- |
| r > 0.9 | 매우 좋음 |
| r > 0.7 | 출판 가능 |
| r > 0.5 | 네비게이션 수준 |
| r < 0 | baseline 평균보다 나쁨 |

## 중요 주의점

- Trial-level CV에서 trial 단위로 계산 → aggregate 금물.
  - fold 내 r을 평균해야 leakage 없음.
- Scale bias 보정 후에도 r과 VAF를 같이 봐야 amplitude 오차와 shape 오차 분리 가능.
- 연결: `05 - Kinematic Consistency`
