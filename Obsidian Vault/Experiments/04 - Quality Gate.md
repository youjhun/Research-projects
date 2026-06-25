# Experiments: Low-Data Augmentation Quality Gate

> 생성 spike의 품질을 정량 검증하는 게이트.
> 기반 개념: [[08 - VAE Architecture]], [[05 - Kinematic Consistency]]
> 후속 실험: [[07 - Augmented Decoding]]

## 평가 지표 (3가지)

### 1) 통계적 유사성

- Sparsity: 실제 93.89% vs 생성 sparsity.
- Mean firing rate: 실제 6.4 Hz vs 생성 FR.
- tolerance: ±10%.

### 2) Kinematic consistency

- 생성 spike만으로 Ridge decoder 학습 → r.
- 기준:
  - low-data 100 trial baseline r 대비 80% 이상.
  - 즉 low-data r이 0.88이면 생성 r > 0.70 목표.
  - 연결: [[01 - Baseline Decoding]]

### 3) Latent space structure

- 실제 trial z와 생성 trial z를 UMAP overlay.
- 겹치면 quality pass.
- 완전 분리 = mode collapse → VAE 구조 재설계.

## 검증 순서

```bash
1. VAE train (100 trial)
2. generate 100/300/900 trial
3. run Ridge on generated-only → check r
4. UMAP check
5. pass → go to [[07 - Augmented Decoding]]
```
