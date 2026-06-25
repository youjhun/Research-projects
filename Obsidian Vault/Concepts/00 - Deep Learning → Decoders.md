# Foundation Bridge: Deep Learning → Decoders

> 딥러닝 기초가 각 디코더 구조에 어떻게 반영되는지.
> Upstream: `00 - Deep Learning Foundations`
> Downstream: `02 - BCI Decoding`, `Experiments - Baseline Decoding`

## Expands To

### From Backprop → Ridge / MLP / LSTM / Transformer

- Ridge:
  - convex loss → closed-form.
  - gradient 필요 없음.
- MLP:
  - chain rule backprop: `∂L/∂w`.
  - ReLU + Adam.
  - Dual-stream: 두 개의 FC branch가 독립 backprop.
- LSTM:
  - BPTT (Backprop Through Time).
  - gate gradient flow 관리.
  - long sequence에서 gradient vanishing 문제가 LSTM 도입 계기.
- Transformer:
  - scaled dot-product attention backward.
  - residual connection이 gradient highway.

### From Activation → 모든 디코더

- 왜 ReLU / Leaky ReLU인가:
  - negative spike count feature가 그대로 전달되도록.
  - Sigmoid/Tanh는 정보 압축이 너무 강함.

## Expands From

- `00 - Deep Learning Foundations`
  - MLP / Backprop
  - Activation
  - RNN / LSTM gate
  - Attention Mechanism
  - VAE 기초
