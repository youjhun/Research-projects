# KAIST NEP Lab 6 papers report

# 6 papers from KAIST NEP LAB

[Distributed Wireless Microimplant Brain-Machine Interfaces: A Synthesis of Six Neurograin Studies.pdf](KAIST%20NEP%20Lab%206%20papers%20report/Distributed_Wireless_Microimplant_Brain-Machine_Interfaces_A_Synthesis_of_Six_Neurograin_Studies.pdf)

## **1. Patterned electrical brain stimulation by a wireless network of implantable microdevices**

[https://www.nature.com/articles/s41467-024-54542-1](https://www.nature.com/articles/s41467-024-54542-1)

[Patterned electrical brain stimulation by a wireless network of implantable microdevices.pdf](KAIST%20NEP%20Lab%206%20papers%20report/Patterned_electrical_brain_stimulation_by_a_wireless_network_of_implantable_microdevices.pdf)

### 연구 목적/ 문제

폐루프 BCI에서 **뇌에 의미있는 정보를 써넣는 (write-in)** 기능 구현을 위해서 여러 피질 영역에 걸쳐 공간-시간적으로 구조화된 국소 전류 자극을 전달하는 확장 가능한 무선 시스템 구현

### 핵심 방법

- **소자** : 65nm 저전력 RF CMOS 공정의 SoC(System on Chip) 칩, 크기 300/400/500μm (주로 500), 무게 약 300μg. 각 칩에 100μm 간격의 텅스텐 미세전극 쌍(길이 1500μm)을 후공정으로 부착
- **전력** : 약 1GHz RF 근접장 유도 결합, 3-코일 시스템 (체외 Tx 코일 + 피하 relay 코일 + 칩 마이크로코일)  Unregulated 전압공급 + 과전압보호(OVP) 다이오드
- **통신** : **Daisy-chain**(충돌 없는 low duty cycle) **protocol**, 다운링크 ASK-PWM 변조, 1Mbps. ‘sync’ 시퀀스 후 칩당 3bit Command(7가지 유형). 칩당 3μs에 자극 파라미터(진폭, 위상폭, 반복률) 프로그래밍 → 원리적으로 1000개 칩을 3ms 내 접근. 업링크는 BPSK Backscattering
- **전하 균형** : 능동 charge balancing, 잔류 전하 불균형 총 주입전하의 2% 미만

### 주요 결과(수치)

- 단일 칩 최대 120μA peak-to-peak Biphasic 전류
- ASK-PWM 복조는 클록 변동 23% 이내에서 100% 성공률, 자극 주파수 최대 2kHz까지 안정.
- Tx 전력 10배 증가 시 주입 전하는 13.7%(Command 3) ~ 38.8%(Command 6)만 증가
    
    → 비조절 전원의 변동 완화
    
- 만성 실험 : 쥐에 30개 칩 3개월 이식. Motor cortex  단일칩 120μA 자극으로 머리 움직임 유발; 3개 칩 동시 자극으로 Whisker movement
- 2개 Lever 지각 과제 : 30개 칩 동시 50Hz 자극 시 정답률 96%, 감각피질 2개 칩 86%, 운동피질 2개 칩 62%
- Low duty cycle : 9.5 duty에서 90% 정답률; 1.4% duty(20Hz, 100μs/phase)에서도 82% 정답률. 행동 유발 평균 RF 전력 1.45mW
- 안정성 : 100mW 연속 Tx에서 피크 공간 평균 SAR 1W/kg. 이는 IEEE Std C95.1-2005/2019 에서 controlled/occupational 환경 국소(10g 평균) 한계로 규정한 10 W/kg의 약 1/10 수준. 1.4% duty 시 0.0145 W/kg까지 감소. 898MHz 공진, LCP 225μm 밀봉으로 70일 이상 안정

### 논의점

**혁신점 :** Low duty cycle RF로 평균 전력을 1자릿수 이상 절감하면서 다중점 패턴 자극 실현, 만성 자유행동 모델 입증

**한계 :** 쥐 뇌 크기로 칩 수 제한, 텅스텐 전극의 비수직성, 에폭시 곡면으로 평탄 접촉 어려움, 대형동물 적용시 조직 두계 증가로 결합효율 1자릿수 감소 (최대 1W 전송 필요)

## **2. An asynchronous wireless network for capturing event-driven data from large populations of autonomous sensors**

[https://www.nature.com/articles/s41928-024-01134-y](https://www.nature.com/articles/s41928-024-01134-y)

[An asynchronous wireless network for capturing event-driven data from large populations of autonomous sensors.pdf](KAIST%20NEP%20Lab%206%20papers%20report/An_asynchronous_wireless_network_for_capturing_event-driven_data_from_large_populations_of_autonomous_sensors.pdf)

### 연구 목적/ 문제

수천 개 분산된 무선 센서(특히 스파이크 기록)에서 sparse 이벤트 데이터를 충돌없이 확장성 있게 전송하는 통신 프로토콜. 기존 random-access / 고정 타임슬롯 방식은 희소성의 이점을 살리지 못함.

### 핵심 방법

- **ASBIT Protocol**(Asynchronous Sparse Binary Identification Transmission): 뉴런 발화처럼 이벤트 발생 시에만 Backscatter. 각 노드가 고유 Gold code(준직교 PN 시퀀스)로 스파이크를 인코딩, 수신부에서 matched filter로 복조. CDMA 변형이나 희소성의 통계적 다중화 활용.
- **Chip :** TSMC 65nm, 300x300μm. 디지털 FSM(35x65μm)에 Gold code 생성기, BPSK 변조기. 13-bit PUF(물리적 복제불가 함수)를 시드로 511-bit Gold code(8191 중 선택). ~900 MHz
- **클록 비교**
    - Free-running 발진기(~30MHZ, +-1000ppm 드리프트, 저전력)
    - RF 캐리어 주파수 분주(드리프트 무시 가능, 전력 증가)
- **디코딩** : SNN(스파이크 신경망) 모델로 영장류 피질 스파이크에서 커서 속도 (손 운동) 예측

### 주요 결과(수치)

- 78개 칩 제작, 평균 SNR 1.7 dB
- Free-running: 50Hz 이벤트율에서 750노드 EER 1.19e-3, 희소 이벤트 시 최대 2500노드

### 논의점

**혁신점 :** Low duty cycle RF로 평균 전력을 1자릿수 이상 절감하면서 다중점 패턴 자극 실현, 만성 자유행동 모델 입증

**한계 :** 쥐 뇌 크기로 칩 수 제한, 텅스텐 전극의 비수직성, 에폭시 곡면으로 평탄 접촉 어려움, 대형동물 적용시 조직 두계 증가로 결합효율 1자릿수 감소 (최대 1W 전송 필요)

## **3. Versatile On-Chip Programming of Circuit Hardware for Wearable and Implantable Biomedical Microdevices**

[https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202306111](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202306111)

## **4. Neural recording and stimulation using wireless networks of microimplants**

[https://www.nature.com/articles/s41928-021-00631-8](https://www.nature.com/articles/s41928-021-00631-8)

## **5. Wireless Addressable Cortical Microstimulators Powered by Near-Infrared Harvesting**

[https://pubs.acs.org/doi/10.1021/acssensors.1c00813](https://pubs.acs.org/doi/10.1021/acssensors.1c00813)

## **6. Decoding speech from spike-based neural population recordings in secondary auditory cortex of non-human primates**

[https://www.nature.com/articles/s42003-019-0707-9](https://www.nature.com/articles/s42003-019-0707-9)

**Key IDEA : 기존의 단일 모놀리식 미세 전극 Array를 대체하여, 수백 ~ 수천 개의 sub mm 크기 자율(autonomous) 실리콘 칩을 대뇌 피질 표면/내부에 공간적으로 분산 배치하고, 이들을 무선으로 전력 공급, 통신, 제어 하는 것.**

# 중요성, 맥락

Monolithic array의 한계

1. 고정된 전극 배치
2. 유한한 채널 수
3. 비연속적(non-contigous) 영역 동시 접근 불가
4. 경피적(percutaneous) 연결의 감염, 내구성 문제

분산형 접근이 이들을 해결하지만 새로운 난제 발생

1. 극소형 칩에 대한 무선전력전송(WPT) 효율
2. 수천 노드의 충돌 없는 통신 프로토콜
3. 안전한 전자기 노출(SAR)
4. 미세조립, 밀봉 공정
5. 대규모 신경 데이터의 디코딩

## 6편 구조

Paper 4 : 출발점. “Neurograin”의 개념과 ~1GHz 양방향 무선 링크 도입, 기록(recording), 자극(Stimulation)을 모두 처음 in vivo 입증

paper 1 : 자극(Write-in) 측면의 발전. 30개 칩을 자유행동 쥐에 3개월 만성 이식하여 공간-시간 패턴 자극과 행동 변화 입증

paper 2 : 기록(read-out) 측면의 통신 확장성. ASBIT(비동기 희소 이진 식별 전송) protocol → 수천 Node 통신 + SNN(스파이크 신경망) 디코딩

paper 3 : 공통 Enabling 기술. 금속 퓨즈 / 안티 퓨즈 + 레이저 어블레이션 / FIB 기반 칩 후공정 프로그래밍

- Paper 1, 5 칩 주소 부여 기반

paper 5 : 대안적 전력, 통신 방식. RF 대신 근적외선(NIR) 광 Harvesting 기반 “Optical Neurograin”

paper 6 : 신경과학적 동기/비동기 디코딩 토대. 영장류 청각 피질 스파이크에서 음성 복원 - 향후 “패턴 자극 기반 Write in” 근거