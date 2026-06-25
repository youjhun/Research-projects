# Neuronal Encoding

> spike train을 디코더 입력 피처로 바꾸는 과정. 하위 노드: [[01 - Spike Train & Neural Coding]]

## Firing Rate 정의

- 단위: Hz (spikes / second).
- bin 기반: 10 ms bin에서 count → ×100 = Hz.
- 평균 발화율: 평탄한 window에서의 rate.
- 인스턴스 rate:ISI에 기반한 instantaneous rate.
  - trade-off: noise vs temporal resolution.

## Tuning Curve

- `r(θ) = r_0 + r_max * cos(θ - θ_pref)`
- cosine tuning:
  - motor cortex에서 흔한 형태.
  - 방향 뿐 아니라 속도에도 적용됨 (speed tuning).
- 본 데이터에서:
  - 161개 뉴런, 각각의 선호 direction/velocity 존재.
  - population decoder가 개개인의 오류를 평균화.

## Encoding to Decoding 연결

- Encoding: spike→movement.
- Decoding: spike→movement의 역방향 근사.
- linear decoder가 성립하는 이유:
  - cosine tuning + population vector = linear mapping에 가까움.
- 연결: `02 - BCI Decoding`
