# Bridge: Method → Concept Graph

> 연구의 개념 확장 관계를 그래프 형태로 정리.
> 이 노트는 graph view에서의 hub 역할.

## 중심 노드

- `[[01 - Spike Train & Neural Coding]]`
- `[[02 - BCI Decoding]]`
- `[[08 - VAE Architecture]]`
- `[[02 - SER & Error Models]]`

## 개념 확장 방향

```
01 - Spike Train & Neural Coding
├── 02 - BCI Decoding (spike → velocity 매핑)
│   ├── Experiments - Baseline Decoding
│   ├── Experiments - SER Robustness
│   └── Experiments - Attention Analysis
├── 02 - SER & Error Models (noise 분해)
│   └── Experiments - SER Robustness
└── 08 - VAE Architecture
    ├── 05 - Kinematic Consistency
    ├── 06 - Physics Regularization
    └── Experiments - Augmented Decoding
```

## 연구의 진화 경로

- **연구 1**: pmd-1에서 rate-coded decoder가 SER에서 왜 robust한가?
  - Baseline → SER → Attention.
- **연구 2**: 저데이터 BCI에서 VAE augmentation이 효과적인가?
  - Quality Gate → Augmented Decoding → Conditional VAE.
- **연구 3 (차기)**: Conditional VAE + Physics Regularization.
  - SER + Burst + Kinematic Consistency로 일반화.
