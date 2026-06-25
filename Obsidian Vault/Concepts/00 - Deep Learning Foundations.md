# Deep Learning Foundations

> MLP, RNN, Attention, VAE의 기초 이론.
> 연결:
>   - `02-02 MLP` (direct)
>   - `02-03 LSTM` (direct)
>   - `02-04 Transformer` (direct)
>   - `08 - VAE Architecture` (direct)

## 1. Universal Approximation

- Single hidden layer MLP with non-linear activation
  - 임의의 연속 함수 근사 가능.
- 하지만:
  - 층이 깊을수록 parameter 효율 좋음.
  - shallow로는 불가능한 표현도 deep로 가능.

## 2. Activation Functions

### Sigmoid / Tanh

- 역사적으로 중요.
- Gradient vanishing 문제.

### ReLU

- `f(x) = max(0, x)`.
- 양수 구간 gradient = 1.
- Sparse activation.
- 단점: Dying ReLU.

### Leaky ReLU / ELU

- 음수 영역에서 작은 기울기 허용.

## 3. Backpropagation

- Chain rule을 이용한 gradient 전파.
- `∂L/∂w = ∂L/∂y · ∂y/∂w`.
- Computational graph:
  - Forward pass → loss 계산.
  - Backward pass → 각 parameter의 gradient.

### Vanishing / Exploding Gradient

- RNN/LSTM 고질적 문제.
- LSTM gate 구조가 이 문제를 완화.
- Transformer는 residual connection이 이 문제를 완화.

## 4. RNN & LSTM

- 순차 데이터 처리.
- Hidden state h_t:
  - `h_t = f(x_t, h_{t-1})`.
- LSTM:
  - Cell state C_t (장기).
  - Hidden state h_t (단기).
  - Forget / Input / Output gate.

## 5. Attention Mechanism

### Scaling Dot-Product Attention

- `Attn(Q,K,V) = softmax(QK^T / √d) V`.
- Q, K, V 모두 입력으로부터 projection.

### Multi-Head Attention

- 여러 projection subspace에서 병렬 attention.
- 서로 다른 temporal scale capture 가능.

### Causal Masking

- 미래 step을 보지 못하게 masking.
- Autoregressive / decoding 필수.

## 6. VAE 기초

- Encoder → distribution → reparameterization → z.
- Decoder → z → x_hat.
- KL + Recon loss = ELBO.
- 연결:
  - `08 - VAE Architecture`
  - `08-01 VAE Encoder`
  - `08-02 VAE Decoder`
  - `08-03 Reparameterization & Conditional VAE`
