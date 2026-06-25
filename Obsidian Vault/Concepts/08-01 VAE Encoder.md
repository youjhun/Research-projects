# VAE Encoder

> spike train + velocity를 잠재 분포로 압축. 하위 노드: [[08 - VAE Architecture]]

## 목표

- Input: `(batch, window, 161)` spike + `(batch, 2)` velocity.
- Output: `μ`, `logσ²` → reparameterization → `z`.

## 설계

- flatten spike → FC → shared hidden.
- velocity는 추가 condition으로 concat.
- latent dim:
  - 64 (현재 구현).
  - 너무 작으면 정보 압축 손실.
  - 너무 크면 mode collapse 위험.

## Posterior Collapse 위험

- kl_loss가 너무 강하면 decoder가 z를 무시.
- 방지:
  - KL annealing.
  - free bits (minimum KL per latent dimension).
- 연결: `08 - VAE Architecture`
