# Foundation Bridge: Math → Neural Coding

> 수학 기초가 뇌 신호 개념으로 어떻게 연결되는지.
> Upstream: `00 - Math Foundations`
> Downstream: `01 - Spike Train & Neural Coding`

## Expands To

### Linear Algebra

- Popluation coding → `w = (X^T X)^{-1} X^T y` 최소자승.
- PCA → `X = U Σ V^T`: latent manifold 차원 축소.
- Conditioning number → Ridge의 λ 필요성.

### Probability

- Poisson spike generation: spike count가 Poisson process를 따름.
  - `p(k|λ) = λ^k e^{-λ} / k!`
  - mode collapse이 생기면 Poisson 분포가 깨짐 → VAE 품질 게이트.
- Gaussian NLL → VAE reconstruction loss.

### Signal Processing

- Bandpass filtering: LFP/MUA/spike 분리.
  - 300~3000 Hz Butterworth.
  - Nyquist: fs=30 kHz, f_max=15 kHz.

## Expands From

- `00 - Math Foundations`
  - Linear Algebra
  - Probability & Statistics
  - Signal Processing
