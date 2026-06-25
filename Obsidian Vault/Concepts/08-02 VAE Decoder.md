# VAE Decoder

> 잠재 벡터를 spike + velocity로 복원. 하위 노드: [[08 - VAE Architecture]]

## 출력 분포 가정

### spike

- softplus activation.
- implicit multinomial / Poisson likelihood.
- hard sparsity를 유지하려면 threshold 추가 가능.

### velocity

- linear layer 2D.
- Gaussian NLL.
- MSE approximation 가능.

## Conditional Decoder

- 단순 VAE decoder는 spike만 조건.
- Conditional VAE:
  - decoder에 velocity를 additional condition으로 입력.
  - multi-input conditioning:
    - `[z; velocity]` concat → FC → spike reconstruction.
- 장점:
  - kinematic consistency 향상.
  - control 가능한 생성.
  - 연결: `05 - Kinematic Consistency`

## 디코더 구조 확장

- pointwise FC → 1-layer 또는 2-layer.
- skip connection: encoder의 intermediate feature와 concat.
  - U-Net style이 rare이지만 spike reconstruction에서는 가능.
- 연결: `08 - VAE Architecture`
