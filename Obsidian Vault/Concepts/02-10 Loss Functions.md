# Loss Functions

> 디코딩/생성 모델 학습을 최적화하는 오차 함수 계열. 하위 노드: [[02 - BCI Decoding]], [[08 - VAE Architecture]]

## 회귀 손실

### MSE (Mean Squared Error)

- `L = 1/N Σ(y - ŷ)^2`.
- 가장 기본.
- 단점: outlier에 민감.

### MAE (Mean Absolute Error)

- `L = 1/N Σ|y - ŷ|`.
- outlier robust.
- 단점: 미분 불연속 → 최적화 불안정 가능.

### Huber Loss

- δ threshold 기준:
  - 오차 < δ: MSE 구간.
  - 오차 > δ: MAE 구간.
- BCI에서 burst peak를 outlier처럼 취급하지 않으면서
  - baseline 구간은 잘 학습.

## 정규화 항

### L2 (Ridge)

- `λ Σ w^2`.
- 다중공선성 완화.
- 뉴런 weight가 과도하게 커지는 것 방지.

### KL Divergence

- VAE에서 latent distribution이 N(0,1)에 가깝도록.
- `D_KL(q(z|x) || p(z))`.
- encoder가 posterior collapse 피하는 핵심.

## 생성 모델 손실

- spike component:
  - softplus 출력 → Poisson likelihood 근사.
  - MSE로 대체 가능.
- velocity component:
  - Gaussian NLL.
- physics regularization:
  - `acc_mse + jerk_mse + minjerk_div`.
  - 연결: `06 - Physics Regularization`
