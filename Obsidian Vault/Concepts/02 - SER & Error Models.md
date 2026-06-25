# Concepts: SER & Error Models

> spike 통신/측정에서 발생하는 error 정의와 두 가지 noise 모델.
> 관련 실험: [[03 - SER Robustness]], [[07 - Augmented Decoding]]
> 기반 개념: [[01 - Spike Train & Neural Coding]], [[02 - BCI Decoding]]

## 정의

- **SER (Spike Error Rate)**: signal-to-error ratio.
- 본 코드에서는 두 가지 정의가 병기됨:

### Random SER

- 기존 baseline 실험에서 사용.
- spike deletion + false alarm을 SER/2씩 주입.
- 의미: 무선 채널의 bit-flip error.
- 특성:
  - corrupted spike가 trial에 균등 분포.
  - single channel failure와는 거리가 있음.

### Burst SER

- 새로 추가된 hardware-failure 근사 모델.
- corrupted trial에서 연속 window에 burst spike 삽입/삭제.
- 의미: electrode stuck / dropout burst.
- 특성:
  - SER이 같아도 corrupted pattern이 random과 완전히 다름.
  - real implant에서 더 중요한 failure mode.

## 왜 두 모델이 필요한가

- Random SER = 통신 noise
- Burst SER = hardware failure
- 두 failure mode에 decoder가 어떻게 반응하는지가
  - event-driven BCI의 robustness design에 직접 연결.
- 연결: [[05 - Kinematic Consistency]]
