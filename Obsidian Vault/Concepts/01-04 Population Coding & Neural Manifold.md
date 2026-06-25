# Population Coding & Cosine Tuning

> 여러 뉴런이 운동 변수를 함께 부호화하는 방식. 하위 노드: [[01 - Spike Train & Neural Coding]]

## Cosine Tuning

- 뉴런 i의 발화율:
  - `r_i(θ) = r_0 + r_max * cos(θ - θ_pref)`
- θ_pref: 선호 방향.
- Georgopoulos 1986: M1 뉴런의 방향 선택성.

## Population Vector

- 각 뉴런의 선호 방향 * 현재 발화율 합.
- 균등 분포 가정 하에서 unbiased estimator.
  - `v̂ = Σ r_i * d_i / Σ r_i`
  - d_i: 선호 방향 단위벡터.

## Neural Manifold

- 161개 뉴런이 완전히 독립적이지 않음.
- 운동 자유도 ≈ 7 → 저차원 매니폴드 존재 가정.
- PCA: 데이터 분산이 큰 축 순으로 추출.
  - 상위 PC = 운동 신호.
  - 하위 PC = 개별 뉴런 noise.
- Dimensionality reduction:
  - 차원 축소 → 다중공선성 해소.
  - decoder 입력으로 사용.
- 연결: `02 - BCI Decoding`, `08 - VAE Architecture`
