# Physics Regularization

> 신체 역학 제약을 VAE 생성 loss에 반영. 하위 노드: [[06 - Physics Regularization]], [[Experiments - Quality Gate]]

## Motivation

- 단순 MSE로 spike+velocity를 맞추는 것은
  - distributionally realistic할 뿐 physically consistent하지 않음.
- 인간/원숭이 움직임은 minimum-jerk trajectory에 가까움.
  - 최대속도·가속도·감속도의 연속성 제약.

## Loss Terms

- `L_physics = MSE(a_hat, a_true) + MSE(j_hat, j_true)`
- `a = dv/dt` (가속도).
- `j = da/dt` (jerk).
- minimum-jerk reference와 divergence도 추가 가능:
  - `L_minjerk = MSE(ŷ, y_MJ)`.
  - y_MJ는 polynomial trajectory model.

## 적용 위치

- VAE training:
  - decoder velocity reconstruction에 penalty 항 추가.
  - 생성 spike의 velocity component가 물리적으로 가능한 trajectory만 생성.
- decoder fine-tuning:
  - VAE 생성 데이터로 decoder 학습할 때,
  - 생성 샘플 중 physics mismatch 높은 샘플은 augmentation pool에서 filtering.
- 연결: `Experiments - Augmented Decoding`
