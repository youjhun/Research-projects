# Population Averaging in Presence of Spike Error

> population coding이 spike error에서 robustness를 제공하는 원리. 하위 노드: [[02 - SER & Error Models]], [[Experiments - SER Robustness]]

## 정의

- N개 뉴런의 spike error를 평균화 했을 때 남는 오차 비율.
- active/bin ≈ `λ_active` (Poisson process).
- corrupted spike fraction: `SER * λ_active / λ_active = SER`.

## Rate-coded decoder가 robust한 이유

- Rate coding은 count를 binning한다.
- random deletion/insertion이
  - mean firing rate의 estimate에 미치는 영향이 상대적으로 작음.
- population size 커질수록:
  - central limit에 가까워져 variance 감소.

## 하드웨어 burst와의 관계

- burst error는 single channel failure에 가까움.
- population averging만으로는 burst window bottom에 갇히기 때문에
  - VAE augmentation이 필요한 이유로 연결.
- 연결: `06 - Physics Regularization`, `04 - Quality Gate`
