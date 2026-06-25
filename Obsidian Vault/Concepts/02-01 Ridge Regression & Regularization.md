# Ridge Regression & Regularization

> 디코더 중 가장 단순한 baseline. 하위 노드: [[02 - BCI Decoding]], [[Experiments - Baseline Decoding]]

## Closed-form Solution

- `W = (X^T X + λI)^{-1} X^T Y`
- L2 penalty로 overweight 방지.

## λ (Regularization Strength)

- 다중공선성 클수록 λ ↑.
- log-scale search: `np.logspace(-4, 4, 100)`.
- BCI에서 보통 λ=1~10 범위.

## 특성

- 해석 가능: 각 뉴런 weight = contribution.
- 속도: GPU 상에서 `torch.linalg.solve`로 instant.
- 임플란트 이식성: 단순 MAC로 동작.
  - AP 이동에 가장 적합한 후보.

## 한계

- linear 가정.
- burst peak 구간 undershoot.
  - Dynamic weighting으로 부분 보완.
- SER 구간에서 population averaging으로 robust.
  - 연결: `02 - SER & Error Models`
