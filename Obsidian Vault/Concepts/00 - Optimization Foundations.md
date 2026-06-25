# Optimization Foundations

> 모델 학습의 목적함수, 최적화 알고리즘, 정규화 방법.
> 연결:
>   - `02 - Loss Functions` (direct)
>   - `02-01 Ridge Regression & Regularization` (L2 regularization)
>   - `02-02 MLP` (MSE + Adam)
>   - `08 - VAE Architecture` (ELBO = reconstruction + KL)
>   - `06 - Physics Regularization` (auxiliary loss)

## 1. Optimization 이란

- 함수 f(x)를 최소/최대화 하는 x를 찾는 과정.
- 머신러닝에서는:
  - 모델 파라미터 θ를 데이터 분포에 맞도록 조정.
  - 손실 함수 J(θ)를 최소화.

### 데이터 표현

- Dataset: `D = {(x_i, y_i)}`.
- Empirical risk:
  - `J(θ) = 1/N Σ L(f(x_i; θ), y_i)`.
- True risk:
  - 실제 분포에 대한 기대.
  - 관측 불가 → empirical risk 최적화.

## 2. Gradient Descent 계열

### Batch Gradient Descent

- `θ ← θ - α ∇_θ J(θ)`.
- 안정적이지만 느림.

### SGD (Stochastic GD)

- 매 step마다 mini-batch 단위 gradient.
- noise → plateau 탈출 가능.
- learning rate에 매우 민감.

### Adam

- 1st moment (Momentum).
- 2nd moment (RMSProp).
- Adaptive learning rate.
- 현재 딥러닝 표준.

## 3. Regularization

### 목적

- Overfitting 방지.
- `J_reg = J_data + Ω(θ)`.

### L1 (Lasso)

- `Ω(θ) = λ Σ|w_i|`.
- Sparse solution.
- Feature selection 효과.

### L2 (Ridge)

- `Ω(θ) = λ Σ w_i^2`.
- Weight decay.
- 다중공선성 완화.

### Early Stopping

- Validation loss 증가 직전에 학습 중단.
- implicit regularization.

## 4. Loss Landscape

- Convex:
  - OLS, Ridge.
  - 전역 최적해 보장.
- Non-convex:
  - MLP, LSTM, Transformer, VAE.
  - Local minimum, saddle point 존재.

## 5. VAE objective (ELBO)

- `log p(x) ≥ E_q[log p(x|z)] - D_KL(q(z|x) || p(z))`.
- Recon + KL 두 항의 trade-off.
  - 연결: `08 - VAE Architecture`
