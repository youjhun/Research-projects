# Mathematics Foundations

> 연구 전반에 사용되는 수학적 기본 개념들.
> 연결:
>   - `01 - Spike Train & Neural Coding` (signal, probability, correlation)
>   - `02 - BCI Decoding` (linear algebra, least squares, norm)
>   - `02 - SER & Error Models` (probability, noise)
>   - `08 - VAE Architecture` (probability, KL divergence)

## 1. Linear Algebra

### 벡터 / 행렬 기초

- Vector norm:
  - L1 (Manhattan)
  - L2 (Euclidean)
  - L∞ (Max norm)
- 행렬:
  - `X^T X` 정역행렬 조건 (full rank).
  - Conditioning number: 다중공선성 민감도.
  - Eigenvector / SVD:
    - PCA의 수학적 기반.
    - `X = U Σ V^T`.
- QR, Cholesky:
  - Ridge closed form에 쓰이는 해법 후보.

### 최소자승법

- OLS: `w = (X^T X)^{-1} X^T y`.
- Ridge: `w = (X^T X + λI)^{-1} X^T y`.
- Moore-Penrose pseudo inverse도 같은 계열.

## 2. Probability & Statistics

### 기본 개념

- PMF / PDF.
- Expectation: `E[X]`.
- Variance: `Var(X) = E[(X - μ)^2]`.
- Gaussian:
  - `p(x) = N(x; μ, σ^2)`.
  - 선형 Gaussian system → Kalman filter 가능성.

### KL Divergence

- `D_KL(q || p) = ∫ q(z) log(q(z)/p(z)) dz`.
- VAE에서:
  - posterior `q(z|x)` ↔ prior `p(z)=N(0,I)`.
  - KL 항이 posterior collapse를 방지.

### Robust Statistics

- Median, MAD (Median Absolute Deviation):
  - `MAD = median(|x - median(x)|)`.
  - Spike thresholding에서 std 대신 사용.
  - `σ_n ≈ median(|x|) / 0.6745`.

## 3. Signal Processing 기초

### 푸리에 변환

- 시간 도메인 신호 → 주파수 도메인.
- `X(f) = ∫ x(t) e^{-j2πft} dt`.
- 신경 신호 필터 설계의 기반.

### Nyquist / Sampling

- 샘플링 주파수 ≥ 최대 주파수 × 2.
- Aliasing:
  - 부족 샘플링 → 저주파 ghost 신호.
- 본 데이터: 30 kHz → Nyquist 15 kHz.
- 300~3000 Hz bandpass로 spike 대역만 보존.

### 주요 지표

- Correlation (Pearson r).
- Covariance.
- Cross-correlation:
  - template matching 기반 spike detection.

## 개념 연결

- L1 → L2: Math foundations 뒤에 `01 - Spike Train & Neural Coding`이 온다.
- L1 → L4: Optimization과 VAE는 loss 정규화 항에서 만난다.
