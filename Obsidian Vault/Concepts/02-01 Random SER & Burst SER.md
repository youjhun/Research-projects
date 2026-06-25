# Random SER & Burst SER

> spike error를 주입하는 두 가지 실험 모델. 하위 노드: [[02 - SER & Error Models]], [[Experiments - SER Robustness]]

## Random SER

- 기존 baseline 연구에서 사용.
- spike deletion + spike insertion.
- SER/2씩 양방향에 분포.
- 성향:
  - corrupted spike가 trial에 균등 분포.
  - electrode stuck과 거리가 먼 통신 bit-flip에 가까움.

## Burst SER

- 새로 추가된 hardware failure 근사.
- corrupted trial에서 burst window에 연속적으로 spike 삽입/삭제.
- 성향:
  - electrode dropout burst, channel failure.
  - SER level이 같아도 random과 완전히 다른 corrupted pattern.

## 왜 두 모델이 필요한가

- Random SER는 통신 채널 오차.
- Burst SER는 하드웨어 임플란트 오차.
- 두 failure mode에 decoder가 어떻게 다른지 측정하는 것이
  - event-driven BCI 설계에 직접 연결.
- 연결: `02 - SER & Error Models`, `Experiments - SER Robustness`
