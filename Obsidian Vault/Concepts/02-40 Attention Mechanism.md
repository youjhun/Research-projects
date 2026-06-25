# Attention Mechanism

> Transformer 자기 자신에게 attention 하는 구조. 하위 노드: [[02 - BCI Decoding]], [[Experiments - Attention Analysis]]

## Core

- Query, Key, Value projection → scaled dot-product attention.
- `Attn(Q,K,V) = softmax(QK^T / √d_k) V`.

## Causal Masking

- 미래 step attention = 0.
- spike decoding에서는 필수.
- 인과성을 보존하는 유일한 방법.

## Multi-Head Attention

- 서로 다른 sub-space에서 temporal pattern을 병렬 학습.
- shallow layer: raw spike pattern.
- deep layer: motion-related aggregation.

## SER 환경에서의 attention

- SER가 높아질수록 attention이 diffuse 되는가?
  - 가설: high SER → noisy feature → attention이 어디에 집중해야 할지 흔들림.
- population averaging이 architecture를 덮으면:
  - attention pattern 변화가 적음.
  - 실험: SER=0 vs SER=5e-2 overlay.
- 연결: `Experiments - SER Robustness`, `Experiments - Attention Analysis`
