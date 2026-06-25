# Kalman Filter (State-Space Model)

> 선형 가우시안 가정 하 recursive state estimator. 하위 노드: [[02 - BCI Decoding]]

## 수식

- Predict: `z_prior = A * z_{t-1}`
- Update: `z_t = z_prior + K * (x_t - H * z_prior)`
- Steady-state Kalman gain `K`는 offline에서 수렴.

## Parameter fitting

- `A`: velocity transition (least squares).
- `H`: spike→velocity observation matrix.
- `Q`: process noise covariance.
- `R_diag`: observation noise variance.
  - spike variance 하한선 (`spike_var_floor`)으로 수치 안정성 확보.

## 특징

- 인과적.
- 실시간 칩에 가장 적합.
- 선형·가우시안 가정이 한계.
- 확장 가능:
  - EKF/UKF로 nonlinear model 수용.
  - 연결: `06 - Physics Regularization`

## 비교

- baseline r=0.8701 (4 디코더 중 가장 낮음).
- smoothness는 가장 좋음.
  - 상태공간 모델 특성상 자연 평활화.
