# Concepts: Spike Train & Neural Coding

> 뇌 신호를 어떻게 숫자로 바꾸고, 디코더에 넣을지 정의하는 기초 층.
> 관련 개념: [[02 - BCI Decoding]], [[05 - Kinematic Consistency]], [[09 - SER & Error Models]]
> 기반 데이터: [[01 - pmd-1 Dataset]]

## Spike와 표현 방식

- **Rate coding**: time bin 내 spike 개수 = 발화율.
  - 현재 BCI 디코딩의 사실상 표준.
  - 장점: 노이즈에 강함, 구현 단순.
  - 단점: spike timing 정보 손실.
- **Temporal coding**: spike 발생 시각 자체가 정보.
  - SNN / LIF 기반 디코더가 여기에 해당.
  - 장점: timing-sensitive 정보 보존.
  - 단점: 하드웨어/정렬에 민감.

## Spike Train의 통계적 성질

- 희소성: 93.89% bin이 0.
- 평균 발화율: ~6.4 Hz.
- 이것이 VAE augmentation의 핵심 제약.
  - 너무 sparse → 생성 모델이 mode collapse에 취약.
  - 연결: [[08 - VAE Architecture]]

## Population Coding

- 여러 뉴런이 함께 운동 변수를 부호화.
  - M1 161개 뉴런이 7개 운동 자유도를 mapping.
- Population averaging:
  - 뉴런 수가 많아질수록 노이즈 평균화 효과.
  - SER에서 rate-coded decoder가 robust한 이유와 직결.
  - 연결: [[03 - SER Robustness]], [[04 - Low-Data Augmentation Quality Gate]]

## Motor Lag & Time-Lag Feature

- Spike가 실제 운동을 만들어내기까지 100~200ms 지연.
- 해결: 과거 20 bins (200ms)를 flatten해서 한 벡터로.
  - `(20, 161) → 3,220차원`
- 문제: 다중공선성.
- 해결: Dynamic Weighting (`burst_power=1.3`).
  - 연결: [[03 - SER Robustness]]
