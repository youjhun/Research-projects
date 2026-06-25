# Concepts: VAE Architecture

> Spike train + motion representation를 latent space로 압축·재생성하는 생성 모델.
> 관련 실험: [[07 - Augmented Decoding]], [[04 - Low-Data Augmentation Quality Gate]]
> 기반 개념: [[01 - Spike Train & Neural Coding]], [[05 - Kinematic Consistency]]

## 목표

- (spike window, velocity) 쌍을 latent space로 압축.
- 생성된 spike로 decoder 학습 성능 향상.

## 기본 VAE 구조

- Encoder: spike flatten → FC → z ~ N(μ, σ²)
  - z 차원: 64
- Decoder: z → spike + velocity
  - spike: softplus (Poisson)
  - velocity: linear (Gaussian)
- Loss:
  - spike MSE
  - velocity MSE (kinematic weight ↑)
  - KL divergence

## Conditional VAE (개선 방향)

- Decoder에 velocity를 condition으로 추가.
  - "이 velocity일 때의 spike를 생성해줘"
- 장점:
  - unconditional 대비 kinematic consistency 월등 향상.
  - latent space에서 의미 있는 control.
  - 연결: [[05 - Kinematic Consistency]]

## 생성 데이터 품질 게이트

3가지 검증:
1. **통계적 유사성**: sparsity / mean firing rate 비교.
2. **Kinematic consistency**: 생성 데이터만으로 decoder r > 0.5 (low-data baseline r의 80% 이상 목표).
3. **Latent space overlap**: UMAP으로 실제·생성 z 분포 비교.

## Augmentation Degradation 위험

- 생성 데이터 비율이 너무 높으면:
  - mode collapse로 outlier 생성.
  - 실제 분포에서 멀어져 decoder 성능 하락.
- 최적 비율 탐색 자체가 연구 contribution.
  - 연결: [[07 - Augmented Decoding]]
