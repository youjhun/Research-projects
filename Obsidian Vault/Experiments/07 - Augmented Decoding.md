# Experiments: Augmented Decoding

> VAE 생성 데이터를 decoder 학습에 추가하는 실험.
> 기반 실험: [[04 - Quality Gate]], [[01 - Baseline Decoding]]
> 다음 연구로 연결: [[VAE + Physics Regularization]]

## 실험 조건

- Full data: 496 trial (상한선)
- Low-data: 100 trial
- Low-data + Aug: 100 trial + VAE 생성 N trial

## 생성 비율 sweep

| ratio | 실제 trial | 생성 trial |
| --- | --- | --- |
| 0 | 100 | 0 |
| 1 | 100 | 100 |
| 3 | 100 | 300 |
| 9 | 100 | 900 |

- x축: 생성 비율
- y축: MLP r_neural
- peak 지점 = 최적 비율.
- degradation = 생성 데이터 과다로 인한 성능 하락.

## augmentation degradation의 의미

- negative result가 아니라 **"어떤 비율에서 효과가 있는가"** 에 대한 발견.
- Simple VAE는 어디서 한계가 나오는지 → conditional VAE 필요성으로 연결.
  - 연결: [[08 - VAE Architecture]]

## SER × Augmentation 조합

- 생성 spike에 SER(1e-3, 1e-2) 부여 → noisy augmentation.
- 두 가지 질문:
  1. Clean augmentation만 vs noisy augmentation도: baseline 어느 쪽이 높은가?
  2. SER=1e-2 test에서 noisy augmentation이 robustness를 높이는가, 낮추는가?
  - 연결: [[02 - SER & Error Models]]
