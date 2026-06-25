# Research Bridge: SER Robustness → VAE Augmentation

> 연구의 물리적 continuinity를 잇는 핵심 브릿지.
> Left: `Experiments - SER Robustness`, `Experiments - Attention Analysis`
> Right: `08 - VAE Architecture`, `Experiments - Quality Gate`

## Expands From

### SER 구간에서의 decoder gap

- Ridge: SER=1e-2에서도 retention 0.998.
  - population averaging 효과.
- MLP: SER=1e-2에서도 retention 0.9991.
  - deep model이 noise를 학습하는 게 아니라 robust하게 평균화.
- LSTM: SER=1e-2에서 retention 0.9979.
- Transformer: SER=1e-2 이상 → MLP/LSTM과 gap이 사라짐.
  - 가설: high SER → attention diffuse → architecture advantage 상실.

## Expands To

### "왜 VAE augmentation인가"

- SER=5e-2 ~ 1e-1 구간에서 모든 디코더가 급격히 성능 하락.
  - population averaging도 이 구간에서는 한계.
- 임상 BCI:
  - electrode drift, burst, 어려운 환경.
  - 50~100 trial만 사용 가능한 저데이터.
- 그래서 **"데이터 자체를 늘릴 수 있으면 SER 구간에서도 decoder가 버틴다"**.
  - VAE augmentation이 이 연구 질문에 대한 답.

### 데이터 품질 게이트로 연결

- "무작정 생성 데이터를 많이 넣으면 성능이 오를까?"
  - quality gate 없이 생성 spike를 섞으면:
    - mode collapse → outlier 샘플.
    - kinematics不一致 샘플.
    - decoder 성능 하락.
- 그래서 3가지 측정:
  1. 통계 유사성.
  2. Kinematic consistency (r > threshold).
  3. Latent space overlap.
- 연결: `Experiments - Quality Gate` → `Experiments - Augmented Decoding`.

## Expands From

- `Experiments - SER Robustness`
- `Experiments - Attention Analysis`
- `Experiments - Baseline Decoding`

## Expands To

- `08 - VAE Architecture`
- `Experiments - Quality Gate`
- `Experiments - Augmented Decoding`
- `06 - Physics Regularization`
