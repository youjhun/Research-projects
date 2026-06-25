# Concepts: Kinematic Consistency

> 생성된 spike가 실제 운동 역학과 맞는지 검증하는 품질 게이트.
> 관련 실험: [[07 - Augmented Decoding]], [[06 - Attention Analysis]]
> 기반 개념: [[01 - Spike Train & Neural Coding]], [[02 - BCI Decoding]]

## 정의

- Velocity-conditioned spike generation에서 가장 중요한 조건.
- 생성된 (spike, velocity) 쌍이 의미 있게 연결되어야 함.
- 평가: 생성 spike만으로 decoder 학습 → r > threshold면 quality pass.

## Velocity Rescaling

- 문제: MLP/LSTM 출력 velocity의 진폭이 실제보다 작음.
  - Scale Bias < 1.0.
- 해결: train split에서 affine rescaling fit → test predict에 적용.
  - `y_pred_rescaled = a * y_pred + b`
- 주의: train에서만 fit (test leakage 아님).
- 연결: [[02 - BCI Decoding]]

## Physics Regularization 가설

- 단순 MSE로 spike와 velocity를 복원하는 것보다,
  - dynamics (acceleration, minimum-jerk trajectory)를 추가로 match시키면
  - 생성 spike의 생성 모델 generalization이 올라감.
- 연결: [[08 - VAE Architecture]]
