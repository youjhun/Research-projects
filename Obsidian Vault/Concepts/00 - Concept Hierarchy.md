# Concept Hierarchy: BCI Decoding + VAE Augmentation

> 모든 개념 노드의 상위-하위 연결을 한눈에 보는 트리.
> 이 파일은 Obsidian Graph View의 root 참조용.
> 각 노트는 `[[파일명]]` 형태로 연결됨.

---

## L0: Foundation (기초 이론)

- `00 - Math Foundations`
  - Linear Algebra
  - Probability & Statistics
    - Normal distribution, KL divergence
  - Signal Processing
    - Fourier transform, Nyquist, filter
- `00 - Optimization Foundations`
  - Loss & Objective
  - Gradient Descent
  - Regularization (L1/L2)
- `00 - Deep Learning Foundations`
  - MLP / Backprop
  - Activation
  - RNN / LSTM gate
  - Attention mechanism
  - VAE (Encoder-Decoder + Reparameterization)

## L1: Neuroscience & Neural Signal

- `01 - Spike Train & Neural Coding` (`[[01 - Spike Train & Neural Coding]]`)
  - `01-01 Action Potential & Hodgkin-Huxley`
  - `01-02 Extracellular Recording & Spike Sorting`
  - `01-03 Neuronal Encoding`
  - `01-03 Rate Coding vs Temporal Coding`
  - `01-04 Population Coding & Neural Manifold`
  - `01-04 Temporal Integration & Motor Lag`
  - `01-05 Feature Expansion for Neural Decoding`

## L2: Decoding & Error Models

- `02 - BCI Decoding` (`[[02 - BCI Decoding]]`)
  - `02-01 Ridge Regression & Regularization`
  - `02-02 MLP`
  - `02-03 LSTM`
  - `02-04 Transformer`
  - `02-05 Kalman Filter`
  - `02-10 Loss Functions`
  - `02-20 Evaluation Metrics`
- `02 - SER & Error Models` (`[[02 - SER & Error Models]]`)
  - `02-01 Random SER & Burst SER`
  - `02-02 Population Averaging & Noise Dilution`
  - `02-40 Attention Mechanism`

## L3: Experiment & Pipeline

- `Experiments - Baseline Decoding`
- `Experiments - SER Robustness`
- `Experiments - Attention Analysis`
- `Experiments - Quality Gate`
- `Experiments - Augmented Decoding`

## L4: Generative Augmentation

- `08 - VAE Architecture` (`[[08 - VAE Architecture]]`)
  - `08-01 VAE Encoder`
  - `08-02 VAE Decoder`
  - `08-03 Reparameterization & Conditional VAE`
- `06 - Physics Regularization` (`[[06 - Physics Regularization]]`)
  - `06-01 Physics Regularization`

## 데이터 계층

- `01 - pmd-1 Dataset` (`[[01 - pmd-1 Dataset]]`)

## 메타 노드 (연구 흐름)

- `00 - Research Flow`
- `00 - Concept Map`

---

## Graph 순서 (좌→우 / 상→하)

```
00 Math/Optimization/DL Foundations
    ↓
01 Spike Train & Neural Coding
    ↓
02 BCI Decoding + SER
    ↓
03 Experiments (Baseline → SER → Attention → Quality Gate)
    ↓
04 VAE + Physics Regularization
    ↓
05 Augmented Decoding
```

- 이 순서로 Graph View를 보면,
  왼쪽 위: 기초 수학, 오른쪽 아래: 연구 주제.
- `index.md`에서 `[[00 - Concept Hierarchy]]`를 진입점으로 잡고
  각 레벨을 좌클릭으로 따라가면 된다.
