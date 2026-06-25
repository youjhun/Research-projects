# Concepts: Physics Regularization

> 신체 역학 제약을 VAE loss에 반영하여 생성 spike의 현실성 강제.
> 관련 개념: [[08 - VAE Architecture]], [[05 - Kinematic Consistency]]
> 다음 단계: [[VAE + Physics Regularization]]

## 핵심 아이디어

- 현재 VAE: spike MSE + velocity MSE + KL.
- 추가: 가속도 / jerk / minimum-jerk trajectory matching.

## 구현

- Loss 항 추가:
  - `L_physics = MSE(a_pred, a_true) + MSE(j_pred, j_true)`
- margin: minimum-jerk trajectory와의 divergence.
- 생성 샘플 중 physics mismatch 높은 샘플 → augmentation pool에서 filtering.

## 기대 효과

- Decoder generalizaion 향상.
- 생성 spike의 interpretability 향상.
- BCI 제어 환경에서의 실용성 강화.
- 연결: [[Experiments - Augmented Decoding]]
