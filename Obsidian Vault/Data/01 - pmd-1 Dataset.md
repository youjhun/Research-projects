# Data: pmd-1 Dataset

> 전체 분석의 데이터 소스.
> 관련 실험: [[01 - Baseline Decoding]], [[02 - SER Robustness]], [[03 - Attention Analysis]]
> 기반 개념: [[01 - Spike Train & Neural Coding]], [[02 - BCI Decoding]]

## 기본 정보

- 출처: CRCNS pmd-1 (원숭이 motor cortex)
- 총 trial 수: 496
- 총 bins 수: 59,742
- 뉴런 수: 161 (M1 67 + PMd 94)

## 데이터 행렬

| 항목 | shape | 설명 |
| --- | --- | --- |
| `X` | (N, 161) | time bin × 뉴런 spike count |
| `Vx`, `Vy` | (N,) | 손 velocity (cm/s) |
| `kinematics` | (97, 7) | trial별 kinematic feature |

## 구조적 특징

- 하나의 trial = 하나의 reaching movement
- 1 bin = 10 ms
- trial 길이: 97 bins = 970 ms
- 희소율: 93.89%
- 평균 발화율: 6.4 Hz

## 핵심 issue

- **저데이터 정책**: 실제 환자/임상 세팅에서는 50~100 trial만 사용 가능.
  - 현재 데이터 496 trial에서 의도적으로 일부만 써서 low-data regime 시뮬레이션
  - 연결: [[04 - Low-Data Augmentation Quality Gate]]

## Trial-level split

- Bin 단위가 아니라 trial 단위로 split해야 leakage 없음.
  - 같은 trial 내 bin은 kinematic continuity가 강해서 train/test 혼합 시 leakage.
- 현재 코드: `trial_cumlen` 기반 경계 설정 → `KFold`를 trial id에 적용.
