# Foundation Bridge: Optimization → BCI Decoding

> 최적화 기초가 디코더 학습에 어떻게 적용되는지.
> Upstream: `00 - Optimization Foundations`
> Downstream: `02 - BCI Decoding`, `02 - SER & Error Models`

## Expands To

### Loss Function

- Ridge: `J = ||y - Xw||² + λ||w||²`.
  - closed-form 해.
- MLP: MSE + Dynamic Weighting for burst sensitivity.
  - Huber Loss.
- LSTM / Transformer: Adam, cross-entropy or MSE depending on task.

### Regularization

- L2 (Ridge): 다중공선성 방지.
  - λ가 크면 underfit, 작으면 overfit.
- Early Stopping: SER 구간에서 validation loss가 먼저 증가하면 조기 종료.

### ELBO

- VAE objective:
  - `L = L_recon + β KL(q(z|x) || p(z))`.
  - KL divergence가 posterior collapse 방지.
  - 연결: `08 - VAE Architecture`.

## Expands From

- `00 - Optimization Foundations`
  - Loss & Objective
  - Gradient Descent
  - Regularization (L1/L2)
  - VAE objective (ELBO)
