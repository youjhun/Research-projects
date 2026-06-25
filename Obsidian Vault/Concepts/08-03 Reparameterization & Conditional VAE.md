# Reparameterization & Training Stability

> reparameterization trick, KL annealing, conditioning. 하위 노드: [[08 - VAE Architecture]]

## Reparameterization Trick

- `z = μ + σ * ε, ε ~ N(0,1)`.
- gradient가 noise sampling을 우회.
- Backprop 가능 = end-to-end 학습.

## KL Annealing

- 초기 epochs: β=0 → decoder만 학습.
- 점점 β=1까지 증가.
- 효과:
  - 초기에는 reconstruction 먼저 확립.
  - posterior collapse 방지.

## Conditional Input Mixing

- cross-attention decoder도 가능.
- z를 query, velocity를 key/value.
- spike reconstruction target.
- 더 복잡하지만 latent space 해석성이 좋음.

## 주요 하이퍼파라미터

- latent dim.
- β_KL weight.
- velocity loss weight.
- burst_power.
- drop-out for regularization.
- 연결: `08 - VAE Architecture`
