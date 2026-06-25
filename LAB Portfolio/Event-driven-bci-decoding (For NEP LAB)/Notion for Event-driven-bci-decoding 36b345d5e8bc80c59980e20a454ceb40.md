# Notion for Event-driven-bci-decoding

---

## 1. 신경과학 기초

**활동전위 (Action Potential)**

- 호지킨-헉슬리 모델: Na⁺/K⁺ 채널 dynamics
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%201.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%202.png)
    
    뉴런에서 활동 전위가 어떻게 시작되고 전파되는지 설명.
    
    근육 세포와 같은 흥분성 세포의 전기 공학적 특성을 근사적으로 나타내는 비선형 미분 방정식의 집합. (연속 시간 동적 시스템)
    
    - 지질 이중층 :  C_m
    - 전압 계폐형 이온 채널 : g_n(n은 특정 이온 채널) ← 전압과 시간에 모두 의존하는 전기 전도도
    - 누출 채널 : 선형 전도도 g_l
    - 이온 흐름 유도 전기 화학적 기울기 : E_n
    - 이온 펌프 : I_p
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%203.png)
    
    - 활동 전위 발생 순서
    
    ```jsx
    휴지막 전위 (약 -70mV)
          ↓
    역치 도달 (약 -55mV) ← 이 아래로는 AP 발생 안 함
          ↓
    ① 탈분극 (Depolarization)
       Na⁺ 채널 m 게이트 빠르게 열림
       Na⁺ 유입 → 전압 급상승 (+40mV까지)
          ↓
    ② 재분극 (Repolarization)
       Na⁺ 채널 h 게이트 닫힘 (불활성화)
       K⁺ 채널 n 게이트 열림 (느리게)
       K⁺ 유출 → 전압 하강
          ↓
    ③ 과분극 (Hyperpolarization, AHP)
       K⁺ 채널이 늦게 닫혀서 -70mV 아래로 내려감
       → 이 구간이 상대 불응기(RRP)
          ↓
    ④ 휴지막 전위 복귀
       Na⁺/K⁺ 펌프가 이온 농도 복원
    
    - Code
    waveform = -1.0 * np.exp(-t**2 / 0.15)   # ① 탈분극 (음의 피크)
             + 0.3 * np.exp(-(t-1.0)**2 / 0.4)  # ③ 과분극 (양의 후전위)
    ```
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%204.png)
    
- 절대/상대 불응기 (ARP/RRP)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%205.png)
    
- 세포외 기록(extracellular recording)에서 파형이 음의 피크로 나타나는 이유
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%206.png)
    
- HH 모델의 한계
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%207.png)
    

**신경 신호 구성**

**Extracellular Recording의 신호 분리 구조**

```jsx
[ Raw Neural Signal (1 Hz ~ 10 kHz) ]
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 [ Low-pass Filter ]           [ High-pass Filter ]
    (< 300 Hz)                    (> 300 Hz)
        │                             │
        ▼                             ▼
   [ LFP 신호 ]                  [ MUA 신호 ]
                                      │
                                      ▼
                        [ Spike Sorting (기법) ]
                                      │
                                      ▼
                                 [ SUA 신호 ]
                         (단일 뉴런 #1, #2, #3...)
```

- 뇌 상태 반영 : 수면, 각성, 주의 집중 등 뇌의 전반적인 상태나 네트워크 동기화를 분석하는데 필수적임. (ex. 알파파, 베타파, 감마파 등)
    - Delta(1~4Hz), Theta(4~8Hz) : 수면 상태, 기억의 저장(의식적인 인지 작업), 공간 탐색 시 활성화. (특히 해마에서 강하게 관찰)
    - Alpha(8~12Hz), Beta(12~30Hz) : 주의 집중, 시각적 휴식, **운동 계획 및 실행**(운동피질에서 beta 감소 → 움직임 시작)
    - Gamma(30~200) : 고도의 인지 작업, 정보 통합, 지각 가공 시 발생
        
        → MUA와 높은 상관관계
        
- LFP (Local Field Potential): 1~300Hz 저주파 집합적 신호
    
    LFP는 전극 주변(수백 마이크로미터 내외)에 있는 **수많은 뉴런들의 집합적인 활동**을 나타내는 저주파 신호.
    
    - 대역 : 대략 1 ~ 300 Hz
    - 기원 : 뉴런의 입력 및 통합 과정. Pre-synaptic에서 온 신호가 Post-synaptic 밀집 지역에서 저항과 커패시턴스를 거치며 필터리된 결과물
    - 특징
        - EEG : 두개골 밖에서 재는 EEG나 피질 표면에서 재는 ECoG와 유사하나, 뇌 조직 깊숙이 찔러 넣은 전극 근처의 신호이므로 **공간 해상도(Spatial Resolution)이 훨씬 높음.**
    
    LFP의 **낮은 주파수의 위상(Phase)**에 따라 **높은 주파수(ex. Gamma)의 진폭**이 변하는 현상을 중요하게 다룸. 
    
    뇌의 넓은 영역(낮은 주파수) → 국소적인 지역(높은 주파수)의 뉴런 활동 통제 및 통신
    
- MUA (Multi-Unit Activity): 300~3000Hz 스파이크 대역
    
    **여러 개의 뉴런들이 방출하는 활동 전위의 합.**
    
    - 주파수 대역 : 대략 300 ~ 3000Hz
    - 기원 : 전극 반경 수십 마이크로미터 내 존재하는 **뉴런들의 탈분극 현상 = Spike**
    - 특징 :
        - 집단적 발화율 : 단일 뉴런 하나하나를 구별해 내기 전, 전극 주변 Firing rate를 종합적으로 봄.
        - 디지털화 가능성 : LFP → Analog. MUA는 임계값을 넘는 순간 포착 → Digital
        - SUA : MUA 신호에서 수학적 기법 사용하여 개별 뉴런의 신호 떼어내는 과정을 Spike Sorting이라 하며, 단일 뉴런 신호 = SUA(Single-Unit Activity(
- 열잡음(Thermal noise) 특성
    
    뉴런 신호 방해하는 물리적 한계 ← 도체 내부 전자가 열적 교란에 의해 무작위로 운동하며 발생
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%208.png)
    
    - 특성 및 영향
        - White Noise : 열잡음은 모든 주파수 대역에 걸쳐서 균일한 에너지. 따라서 LFP보다는 크기가 상대적으로 작은 **고주파(MUA/SUA) 대역에서 치명적.**
        - 전극 임피던스(R)의 딜레마 : SUA 정밀하게 잡으려면 전극 크기 작아짐 → 전극 작아지면 저항(R) 커짐 → 열잡음 증가.

| **분류** | **LFP** | **MUA** | **SUA** |
| --- | --- | --- | --- |
| **장기 안정성** | **우수함.** 전극이 미세하게 움직여도 주변 집합 신호이므로 신호가 유지됨. | **보통.** 뉴런 집단의 위치가 크게 변하지 않으면 안정적임. | **낮음.** 전극이 수 마이크로미터만 틀어져도 타겟 뉴런을 놓침. |
| **정보의 밀도** | 전체적인 뇌 영역의 흐름 및 의도(예: "움직이고 싶다") 파악에 용이. | 빠르고 직관적인 운동 제어(예: "좌측으로 속도 50으로 이동")에 용이. | 가장 정밀하고 디테일한 코드(예: "검지손가락을 15도 구부림") 해석 가능. |
| **연산 요구량** | 낮음 (샘플링 레이트가 ~1kHz 수준으로 충분) | 보통 (스파이크 카운팅 위주) | **매우 높음** (실시간 대용량 스파이크 소팅 알고리즘 필요) |

**집단 부호화 (Population Coding)**

- Sparse coding: 뉴런이 왜 희소하게 발화하는가
    
    CRCNS 데이터를 직접 봤을 떄
    
    전체 데이터 행렬: 59,742 time bins × 161 neurons
    0이 아닌 원소: 6.11%
    → 93.89%가 0 (스파이크 없음)
    
    즉, **어느 시점에 특정 뉴런이 발화할 확률은 6%**
    
    **이유1: 에너지 효율** 
    뇌는 체중의 2%이지만 전체 에너지의 **20%** 를 소비합니다. 스파이크 하나를 발생시키는 데 드는 비용을 생각해보면:
    
    ```python
    스파이크 발생 과정:
    Na⁺ 유입 → K⁺ 유출 → Na⁺/K⁺ 펌프로 복원
                            ↑
                     ATP를 직접 소모하는 단계
    
    뇌 전체 ATP의 약 50%가 이온 펌프 유지에 사용됨
    ```
    
    ```python
    뉴런 하나의 평균 발화율:
      Dense coding:  100Hz (항상 발화)
      Sparse coding: 6Hz   (가끔 발화)
    
    에너지 절약: 약 94%
    
    뇌 전체 160억 뉴런 기준으로는 천문학적인 차이
    ```
    
    **이유2 : 정보 용량 극대화**
    
    Shannon 정보 이론
    
    ```python
    n개의 뉴런이 있고, 각각 발화(1) or 침묵(0)이라면
    가능한 패턴 수 = 2ⁿ
    
    Dense coding (50% 발화율):
      평균적으로 n/2개 뉴런이 발화
      → 패턴이 서로 비슷해서 구별이 어려움
    
    Sparse coding (5% 발화율):
      평균적으로 n×0.05개 뉴런이 발화
      → 각 패턴이 매우 독특해서 구별이 쉬움
    ```
    
    ```python
    뉴런 100개, 발화율 50% vs 5%
    
    Dense (50%): C(100,50) ≈ 10²⁹가지 패턴
    Sparse (5%): C(100,5)  ≈ 75,287,520가지 패턴
    
    숫자만 보면 Dense가 더 많아 보이지만...
    
    실제 정보량(Shannon entropy) 계산 시:
    → 노이즈 대비 구별 가능한 패턴은 Sparse가 더 많음
    → 에너지 효율까지 고려하면 Sparse가 압도적으로 유리
    ```
    
    이유 3: 표현의 독립성 - 간섭 방지
    
    Dense coding의 치명적 문제
    
    ```python
    상황: "사과"를 기억하는 뉴런 집합 A
          "오렌지"를 기억하는 뉴런 집합 B
    
    Dense coding: A와 B가 많이 겹침
    → "사과" 기억이 "오렌지" 기억을 덮어씀
    → 새로운 걸 학습하면 이전 기억이 망가짐
       (Catastrophic Interference)
    
    Sparse coding: A와 B가 거의 안 겹침
    → 독립적인 표현 가능
    → 새로운 학습이 기존 기억을 방해하지 않음
    ```
    
    이게 **해마(hippocampus)** 에서 특히 중요. 해마는 매일 새로운 기억을 저장해야 하므로, 기존 기억과의 간섭을 최소화하기 위해 극단적으로 희소한 발화(1~5%)진행
    
    **이유4 : 노이즈 간섭성**
    
    ```python
    Dense coding 상황:
      신호: [1,1,0,1,1,0,1,1]
      노이즈로 하나 오류: [1,1,0,1,0,0,1,1]  ← 5번째가 바뀜
      → 전체 패턴의 12.5%가 틀림 → 큰 오류
    
    Sparse coding 상황:
      신호: [0,0,0,1,0,0,0,1]  (2개만 발화)
      노이즈로 하나 오류: [0,0,0,1,0,0,1,1]  ← 7번째가 바뀜
      → 발화한 뉴런 중 하나가 틀림 → 여전히 부분 복원 가능
    ```
    
    **이유5: Efficient coding Hypothesis**
    
    **"뇌는 외부 세계의 통계적 구조를 학습하여, 자연 신호에서 자주 나오는 패턴을 가장 적은 뉴런 발화로 표현하도록 최적화되어 있다.”**
    
    자연 이미지의 통계:
    픽셀들은 서로 강한 상관관계가 있음
    (인접 픽셀은 비슷한 색깔일 가능성이 높음)
    
    V1 뉴런(1차 시각피질)의 특성:
    특정 방향의 edge에만 반응
    → 자연 이미지에서 edge가 가장 많은 정보를 담고 있음
    → 결과적으로 뉴런들이 sparse하게 발화
    
    수학적으로:
    자연 신호의 중복성 제거(decorrelation)
    = sparse representation 생성
    = 정보 이론적으로 최적 부호화
    

---

## 2. 신호처리

[https://youtu.be/Mc9PHZ3H36M?si=NqazpuzsV1m4l1Lv](https://youtu.be/Mc9PHZ3H36M?si=NqazpuzsV1m4l1Lv)

**필터링**

**핵심 정의:**

특정 주파수 성분은 통과시키고 나머지는 차단하는 시스템

**주파수 영역으로 보는 이유:**

시간 영역에서의 복잡한 신호를 주파수로 분해하면 각 성분을 독립적으로 다룰 수 있음.

$$
X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi ft} dt

$$

| 종류 | 영어 | 통과 대역 | 신경과학 용도 |
| --- | --- | --- | --- |
| 저역통과 | LPF | 낮은 주파수 | LFP 추출 |
| 고역통과 | HPF | 높은 주파수 | DC 제거 |
| 대역통과 | BPF | 특정 대역 | 스파이크 검출 |
| 대역저지 | BSF/Notch | 특정 대역 제외 | 60Hz 전원 노이즈 제거 |

```python
필터 목적: 주파수 선택
    │
    ├── 주파수 특성 기준
    │   ├── LPF / HPF / BPF / BSF
    │
    ├── 구현 방식 기준
    │   ├── FIR: 피드백 없음, 안정, 선형위상, 계산 많음
    │   └── IIR: 피드백 있음, 효율적, 비선형위상
    │       ├── Butterworth (평탄)
    │       ├── Chebyshev (급격한 전이)
    │       ├── Elliptic (최고 성능)
    │       └── Bessel (위상 보존)
    │
    ├── 적용 방식
    │   ├── lfilter: 인과적, 위상지연, 실시간 가능
    │   └── filtfilt: 비인과적, zero-phase, 오프라인
    │
    └── 수학적 도구
        ├── Z 변환: 디지털 필터 분석
        ├── 극점/영점: 안정성 판단
        └── 푸리에 변환: 주파수 분석
```

- 필터
    - FIR 필터 (Finite impulse response filter)
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%209.png)
        
        ```python
        장점
        ├── 항상 안정 (피드백 없으므로 발산 불가)
        ├── 선형 위상 가능 → 모든 주파수 동일한 시간 지연
        └── 설계 직관적
        
        단점
        ├── 같은 성능을 내려면 IIR보다 계수 훨씬 많이 필요
        └── 계산량 많음, 지연 큼
        ```
        
        FIR필터는 디지털 필터의 한 종류로 입력신호의 일정한(유한한, finite) 값들만을 가지고 필터링을 수행한다.
        
        따라서, 필터의 특성함수인 임펄스 응답을 구해보면 유한한 길이를 가지게 된다.
        
        필터의 식의 형태에서 보면 회귀(feedback)성분을 갖지 않는다.
        
        그러므로 동일한 특성을 구현할 때 차수가 IIR필터에 비하여 높아져서 구현비용(부품가격, 실행시간 등)이 많이 들지만
        
        위상변이(즉, 입력과 출력간의 파형의 형태유지)가 중요한 경우에는 반드시 FIR필터를 사용해야 한다.
        
        설계법으로는 윈도우에 의한 방법, 주파수 표본화 방법, 컴퓨터에 의한 최적 설계법 등이 있다.
        
    - IIR 필터 (Infinite Impulse response)
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2010.png)
        
        ```python
        장점
        ├── 적은 계수로 높은 성능 (FIR보다 계산 효율적)
        └── 아날로그 필터를 그대로 디지털로 변환 가능
        
        단점
        ├── 불안정 가능성 (피드백 → 발산 위험)
        ├── 비선형 위상 → 주파수마다 다른 시간 지연
        └── 설계 복잡
        ```
        
        입력 신호의 값과 출력 신호의 값이 재귀적으로 사용됨. 
        
        IIR필터는 디지털 필터의 한 종류로 입력신호의 값과 출력신호의 값이 재귀적으로(recursive, feedback) 적용되어
        
        필터링이 수행된다. 따라서 구현식의 형태로 반복식이 되며 특성함수인 임펄스 응답은 무한한 길이를 갖는다.
        
        동일한 특성을 갖는 FIR필터에 비해 차수가 적어져서 경제성이 있으나 위상특성의 측면에서는 비선형성을 가지므로
        
        (즉, 각 주파수 성분마다 위상의 차이가 비선형적으로 달라서) 입력 파형과 출력 파형이 유사한 파형을 갖지 않는다.
        
        설계법으로는 bilinear transform에 의한 방법, 임펄스 응답 불변법등이 있다.
        
        이러한 방법은 공통적으로 차단 주파수 근방에서 진폭이나 주파수 축의 왜곡이 발생할 가능성이 있으므로
        
        원하는 필터링 대역보다 표본화 주파수를 크게 잡는 것이 좋다.
        
        ### Butterworth
        
        ```python
        특징: 통과대역 최대한 평탄 (Maximally flat)
        위상: 비선형
        용도: 신경 신호, 일반 오디오
        ```
        
        ### Chebyshev Type I
        
        ```python
        특징: 통과대역에 ripple 허용 → 전이대역 더 급격
        위상: Butterworth보다 더 비선형
        용도: 좁은 전이대역이 필요할 때
        ```
        
        $$
        ∣H(jω)∣^2=\frac{1}{1+(ω/ωc)^{2n}}
        $$
        
        ### Chebyshev Type II
        
        ```python
        특징: 저지대역에 ripple → 통과대역은 평탄
        용도: 통과대역 평탄 + 급격한 차단 필요 시
        ```
        
        ### Elliptic (Cauer)
        
        ```python
        특징: 통과대역 + 저지대역 모두 ripple
        장점: 같은 차수에서 가장 급격한 전이
        단점: 위상 왜곡 가장 심함
        ```
        
        ### Bessel
        
        ```python
        특징: 위상 선형성 최우선
        장점: 파형 모양 보존 최고
        단점: 전이대역 가장 완만
        용도: 파형 왜곡이 치명적인 경우
        ```
        
        ```python
        성능 비교 (같은 차수):
        전이대역 급격함: Elliptic > Chebyshev > Butterworth > Bessel
        위상 선형성:     Bessel > Butterworth > Chebyshev > Elliptic
        파형 보존:       Bessel > Butterworth > Chebyshev > Elliptic
        ```
        
    - FIR VS IIR
        
        
        | 항목 | FIR | IIR |
        | --- | --- | --- |
        | 피드백 | 없음 | 있음 |
        | 안정성 | 항상 안정 | 설계에 따라 불안정 가능 |
        | 위상 | 선형 위상 가능 | 비선형 위상 |
        | 계산량 | 많음 | 적음 |
        | 임펄스 응답 | 유한 | 이론적 무한 |
        | 아날로그 대응 | 없음 | 있음 (Butterworth 등) |
        | 실시간 적합성 | 지연 큼 | 지연 작음 |
        | 신경과학 사용 | 오프라인 분석 | 실시간 BCI |
        - FIR 필터는 IIR 필터에 비해 구조가 간단하다.
        - FIR 필터는 항상 안정성이 보장되지만, IIR 필터는 그렇지 않다.
        - FIR 필터의 위상은 선형이고, IIR 필터의 위상은 비선형이므로 FIR 필터의 위상이 왜곡에 강건하다.
        - FIR 필터를 사용하여 원하는 필터를 각이 지게 설계하려면 필터의 계수들이 IIR 필터를 사용했을 경우보다 더 많이 필요하게 된다.
        - IIR 필터는 아날로그 필터의 구조와 비슷하므로 아날로그 필터로 변환이 쉬운 반면에 FIR 필터는 상대적으로 어렵다.
    - Z 변환과 전달 함수
        
        Z-변환은 라플라스 변환의 discrete time 버전이라고 할 수 있다.
        
        pole, zero로 신호 분석하려고 쓰는거다.
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2011.png)
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2012.png)
        
        <aside>
        💡
        
        영점(Zero): H(z) = 0이 되는 z값 → 해당 주파수 완전 차단
        극점(Pole): H(z) = ∞이 되는 z값 → 해당 주파수 증폭
        
        안정 조건: 모든 극점이 단위원 내부에 있어야 함
        |pole| < 1 → 안정
        |pole| ≥ 1 → 불안정 (발산)
        
        </aside>
        
        ```python
        # scipy로 확인
        from scipy.signal import butter, tf2zpk
        b, a = butter(3, [300/15000, 3000/15000], btype='bandpass')
        zeros, poles, gain = tf2zpk(b, a)
        # 모든 poles의 절댓값 < 1이면 안정
        print(all(abs(poles) < 1))  # True여야 안정
        ```
        
    - 필터링 실제 문제들
        1. Gibbs 현상 → 완벽한 사각형을 구현하면, 차단 주파수 근처에서 ringing 발생 : 윈도우 함수로 부드럽게 처리
        2. 위상 지연과 그룹 지연
            1. 위상 지연 = 각 주파수 성분이 얼마나 지연?
            2. 그룹 지연 = 신호 봉투 (envelope)의 지연
            
            IIR : 주파수 마다 그룹 지연 다름 → 파형 왜곡
            
            FIR 선형위상 : 모든 주파수 동일 지연 → 파형 보존
            
        3. filtfilt로 위상 제거
            
            ```python
            # lfilter: 위상 지연 τ 발생
            # filtfilt: 앞→뒤→앞 두 번 필터링
            # 위상이 서로 상쇄 → zero-phase
            
            # 대신 effective order가 2배
            # butter(3) + filtfilt = 6차 필터 효과
            ```
            
        4. Edge dffect
            
            신호 시작/끝 부분에서 부정확한 필터 출력
            
            원인 : 필터가 과거 데이터 필요한데 없음
            
            해결 : 패딩 추가 후 필터링, 가장자리 제거
            
    
    ```python
    실시간 BCI 디코딩
    └── IIR (Butterworth order 3~4)
        └── lfilter 사용
    
    오프라인 스파이크 sorting
    └── IIR (Butterworth) + filtfilt
        또는 FIR (Hamming) + lfilter
    
    LFP 분석 (감마, 세타 밴드)
    └── FIR (선형 위상 중요)
        └── 위상 정보가 신경과학적 의미 있음
    
    60Hz 전원 노이즈 제거
    └── IIR Notch 필터
        b, a = iirnotch(60, Q=30, fs=30000)
    ```
    
- Gaussian Smoothing
    
    ```
    가우시안 스무딩 필터링 이란?
           - 가우시안 분포를 영상처리에 적용한 것
           - 정규분포, 확률분포에 의해 생성된 잡음을 제거하기 위한 필터
    
    자세히
    Gaussian smoothing의 basic idea는 컨볼루션(convolution)을 통해 point-spread function(PSF, 점 확산 함수)처럼 2D 가우시안 분포를 사용하는 것이다. 이미지는 이산(discrete) 픽셀들의 집합으로 구성되어 있기 때문에, 컨볼루션을 수행하기 전 가우시안 함수를 통하여 근사한 이산값을 생성해야 한다.
    
    이론적으로 가우시안 분포는 전 지점에서 0이 아닌 값을 갖지만, 실제로 평균에서 약 3σ이상 떨어진 값은 0으로 취급하는 것이 효율적이다. 따라서 우리는 이 점에서 커널을 잘라낼 수 있다.
    
    ```
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2013.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2014.png)
    
    Gaussian smoothing의 적용 효과는 mean filter와 유사하다. 스무딩의 강도는 Gaussian의 표준편차 값에 따라 조정된다. (표준편차 값이 클수록 강한 스무딩 효과)
    
    가우시안은 각 인접 픽셀의 `가중 평균(weighted average)`을 출력하는데, **중심 픽셀으로 갈수록 더 많은 가중치가 부여**된다. 
    
    반면, mean filter는 모든 픽셀에 **균일한 가중 평균**이 부여된다. 이로써 Gaussian filter가 동일한 크기의 mean filter보다 엣지를 더 잘 보존할 수 있게 된다.
    
    가우시안을 스무딩 필터로 사용하는 이유 중 하나는 **주파수 응답(frequency response)** 때문이다. 대부분의 컨볼루션 기반 스무딩 필터는 low-pass frequency filter인데, low-pass filter는 high spatial frequency 성분을 제거한다. 
    
    가우시안의 퓨리에 변환(Fourier Transform)도 역시 가우시안이기 때문에, 가우시안 블러를 적용하면 이미지의 **고주파 성분을 줄이는 효과**가 있다.
    
    mean filter와 gaussian filter는 모두 고주파수 성분을 감소시키지만, mean filter는 주파수 응답에서 oscillation(진동)이 발생한다. 반면, gaussian filter는 진동이 발생하지 않는다. 실제로, 주파수 응답의 곡선 자체가 half gaussian 형태이다. 따라서, 적절한 크기의 **Gaussian filter를 선택하면 필터링 후 이미지에 어떤 주파수 성분이 포함되어 있는지 예측하기가 더 쉽다.**
    
    ```python
    from scipy.ndimage import gaussian_filter1d
    y_pred_smooth = gaussian_filter1d(y_pred, sigma=3)
    ```
    
    물리적 사실:
    
    - 손의 질량 > 0
    - 따라서 가속도는 유한
    - 따라서 속도는 연속함수
    - 따라서 순간 텔레포트 불가능
    
    Ridge 예측값의 문제:
    
    - 매 10ms bin마다 독립적으로 예측
    - bin 간 연속성 보장 없음
    - 결과: 예측값이 지그재그로 튀는 현상
    
    → 가우시안은 이 물리적 제약을 사후에 부과 
    
    **σ=3의 의미**
    
    ```python
    σ=3 bins = 3 × 10ms = 30ms 시간 창
    
    이 창 안의 예측값들을 가우시안 가중치로 평균:
      현재 bin 가중치: 가장 높음 (중심)
      ±1 bin(±10ms): 중간 가중치
      ±2 bin(±20ms): 낮은 가중치
      ±3 bin(±30ms): 매우 낮은 가중치
     
    ```
    
    ### 더 엄밀한 방법
    
    | 방법 | 설명 | 특징 |
    | --- | --- | --- |
    | Gaussian smoothing (현재) | 사후 평활화 | 간단하지만 비인과적 |
    | Kalman Filter | 예측-보정 반복 | 인과적, BCI 표준 |
    | Velocity → Position 적분 제약 | 속도 예측값이 position과 일치하도록 | 물리 일관성 보장 |
- Butterworth bandpass filter 설계 원리
    
    **왜 Butterworth인가:**
    
    | 필터 종류 | 특징 | 단점 |
    | --- | --- | --- |
    | Butterworth | 통과대역 최대한 평탄 | 전이대역 완만 |
    | Chebyshev | 전이대역 급격 | 통과대역 ripple |
    | Bessel | 위상 선형 | 전이대역 매우 완만 |
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2015.png)
    
    신경 신호에 Butterworth를 쓰는 이유: **파형 왜곡 최소화**가 우선이기 때문입니다.
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2016.png)
    
- Nyquist 정리, 샘플링 주파수
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2017.png)
    
    **나이퀴스트 이론(Nyquist Theorem)**은 **아날로그 신호를 디지털 데이터로 변환할 때, 원본 신호를 왜곡 없이 완벽하게 복원하기 위해 필요한 최소한의 표본 추출(샘플링) 주파수를 정의한 정리**
    
    → 모든 신호는 그 신호에 포함된 가장 높은 진동수의 2배에 해당하는 빈도로 일정한 간격으로 샘플링하면 원래의 신호를 완벽하게 기록가능.
    
    ADC (아날로그 → 디지털) 충실하게 재생하려면 아날로그 파형의 샘플 필요
    
    → 이때 취득하는 초당 샘플 수를 Rate 혹은 샘플링 주파수라고 한다.
    
    - 샘플링
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2018.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2019.png)
    
    ```jsx
    # 코드에서
    nyq = 0.5 * fs          # Nyquist 주파수 = 15000 Hz
    low = 300 / nyq         # 정규화: 0~1 범위로 변환
    high = 3000 / nyq
    b, a = butter(order=3, [low, high], btype='bandpass')
    ```
    
    Why 300~3000Hz
    
    < 300Hz  → LFP 영역 (제거 대상)
    300~3000Hz → MUA/스파이크 영역 (보존 대상)
    
    > 3000Hz → 고주파 노이즈 (제거 대상)
    
    **Aliasing (앨리어싱):**
    
    샘플링이 부족하면 고주파 신호가 저주파로 **잘못 복원**됩니다.
    
    `실제 신호: 20kHz
    샘플링:    25kHz  
    앨리어싱: 25000 - 20000 = 5kHz로 보임 (가짜 신호)`
    
- `lfilter` vs `filtfilt` 차이 (위상 지연)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2020.png)
    
    filtfilt → 위상 지연 X 하지만 실시간 불가, lifilter → 위상지연 O, 실시간 가능
    
    lfilter: 인과적(causal) 필터
    
    `lfilter`는 Python의 SciPy, PyTorch 등 신호 처리(Signal Processing) 라이브러리에서 제공하는 **선형 디지털 필터(Linear Digital Filter) 적용 함수**입니다. 차분 방정식(Difference Equation)을 사용하여 데이터 시퀀스에 IIR 또는 FIR 필터를 적용합니다.
    
    ```jsx
    입력:  [1, 2, 3, 4, 5, ...]
    출력:  과거 + 현재 데이터만 사용
    결과:  위상 지연(phase delay) 발생
    ```
    
    ```jsx
    filtered[:, ch] = lfilter(b, a, data[:, ch])
    # 실시간 디코더 모사이므로 lfilter가 맞음
    # 오프라인 분석이면 filtfilt가 더 정확
    ```
    
    ```jsx
    실제 스파이크 시점:    t = 100ms
    lfilter 검출 시점:     t = 100ms + Δt (지연)
    → 타임스탬프 오차 발생
    → 실시간 BCI에서는 허용, 오프라인에서는 보정 필요
    ```
    
    filtfilt: 비인과적(zero-phase) 필터
    
    ```jsx
    1단계: 앞→뒤 방향으로 필터링
    2단계: 뒤→앞 방향으로 다시 필터링
    결과:  위상 지연 = 0, 하지만 실시간 불가
    ```
    
    |  | lfilter | filtfilt |
    | --- | --- | --- |
    | 위상 지연 | 있음 | 없음 |
    | 실시간 처리 | 가능 | 불가 |
    | 파형 왜곡 | 있음 | 적음 |
    | 사용 상황 | 실시간 BCI | 오프라인 분석 |

**스파이크 검출**

- MAD 기반 threshold: `σ_n = median(|x|) / 0.6745`
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2021.png)
    
    **중앙값 절대 편차**(MAD, Median Absolute Deviation)는 **데이터의 흩어짐을 측정하는 통계 지표**입니다. 각 데이터 값에서 중앙값을 뺀 절대값들의 '새로운 중앙값'을 구하는 방식입니다. 이상치(Outlier)에 크게 영향을 받지 않는 '강건성(Robustness)'을 갖춘 것이 가장 큰 특징.
    
    스파이크가 섞인 신호에서
    
    signal = [노이즈(작음) x 99% + 스파이크 x 1%]
    
    std(signal) → 스파이크가 std를 크게 올림 → threshold 너무 높아짐
    
    MAD(signal) → 중앙값 기반이기에 스파이크에 영향 안 받음
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2022.png)
    
    - 자세한 유도
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2023.png)
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2024.png)
        
    
    ```python
    데이터: [1, 1, 1, 1, 1, 100]  ← 100이 스파이크
    
    mean = 17.5   std = 40.1   → threshold 높아짐 (스파이크 놓침)
    median = 1    MAD = 0      → threshold 낮게 유지 (스파이크 검출)
    ```
    
    ```python
    sigma_n = np.median(np.abs(signal)) / 0.6745
    threshold = -4.0 * sigma_n
    ```
    
    정규분포에서 4σ 이상의 확률 = 0.0032%
    → 노이즈가 threshold를 넘을 확률 매우 낮음
    → 신경과학 논문의 경험적 표준값: 3σ~5σ
    
- Dead time / refractory period 구현
    
    ```python
    # 방식 1: 고정 dead time 
    idx = local_min + dead_time_samples
    # 장점: 단순, 빠름
    # 단점: 생리학적 RRP 무시
    
    # 방식 2: ARP + RRP 분리
    ARP_samples = int(1.5 * fs / 1000)   # 절대 불응기
    RRP_samples = int(2.5 * fs / 1000)   # 상대 불응기
    
    if idx - last_spike < ARP_samples:
        continue  # 완전 차단
    elif idx - last_spike < RRP_samples:
        if amplitude > threshold * 1.5:   # 더 강한 자극만 통과
            accept()
    
    # 방식 3: 진폭 기반 (논문에서 종종 사용)
    # 불응기 구간에서 진폭이 이전 스파이크의 X% 이상이면 허용
    ```
    
    Dead time이 너무 짧으면
    
    스파이크 파형(60샘플) > dead time(45샘플)
    → 하나의 스파이크를 2번 검출
    
    Dead time이 너무 길면
    
    빠른 연속 발화(burst firing) 검출 불가
    → 실제 뉴런의 burst: 5~10ms 간격으로 연속 발화
    
- 차원 축소 (Dimensionality Reduction)와 잠재 공간 (Latent Space)
    
    뉴런들이 공유하는 공통의 움직임 패턴이나 규칙을 신경 매니폴드(Neural Manifold)라고 부르며, 이 매니폴드가 존재하는 가상의 압축된 공간을 잠재 공간(Latent Space)이라고 합니다.
    
    M1에 161개 뉴런이 있지만, 이들이 **완전히 독립적으로 움직이지 않습니다.** 
    
    이유:
    
    **1. 해부학적 연결:** M1 내 뉴런들은 시냅스로 연결되어 있어서 함께 활성화되는 경향.
    
    **2. 공통 입력:** 모든 M1 뉴런은 SMA, PMd 등 상위 운동 피질에서 공통 입력
    
    **3. 운동 자유도 제약:** 사람 손목의 자유도는 약 7개. 161개 뉴런이 7가지 운동 변수를 부호화한다면, 정보의 본질적 차원은 7 이하.
    
    ```python
    발견: M1 뉴런들의 발화 패턴은 운동 전 준비 기간에
          저차원 회전 궤적(rotational dynamics)을 그린다
    
    의미: 161개 뉴런이 마치 하나의 저차원 시스템처럼
          움직인다는 것 → Neural Manifold 존재의 증거
    ```
    
    현재 코드에서는 `NUM_LAGS=20`을 적용해 3,220차원의 피처를 Ridge 회귀. 
    
    문제점
    1. **다중공선성(Multicollinearity):** 인접한 뉴런들이 서로 비슷한 타이밍에 발화하므로, 입력 피처들 간의 상관관계가 극도로 높음. 
    
    수학적으로 변수 간 상관관계가 너무 높으면 역행렬 계산이 불안정해져 모델이 아주 작은 통신 노이즈(SER)에도 예측값이 널뛰게 됩니다.
    
    2. **신경 잡음(Neural Noise)의 누적:** 161개 뉴런 중에는 진짜 운동 지령과 상관없이 혼자 제멋대로 튀는 독립적인 노이즈를 가진 뉴런들이 많음. 차원이 커질수록 이 무작위 노이즈들이 축적되어 디코딩 성능(R^2) 하락.
    
    - **수학적 해결책: PCA(주성분 분석)를 통한 노이즈 필터링**
    이때 디코더 바로 앞에 PCA(Principal Component Analysis)라는 차원 축소 기법
        
         
        PCA는 161차원의 데이터 공간에서 "데이터의 변동성(분산)이 가장 크게 일어나는 축"을 순서대로 찾아낸다.
        • **PC 1, PC 2, PC 3 (상위 주성분):** 수많은 뉴런들 중 진짜 운동 신호(신경 매니폴드)'가 투영됨. 
        
        이 상위 몇 개의 축이 전체 데이터 표현력의 70~80% 이상을 설명합니다.
        • **PC 150, PC 161 (하위 주성분):** 뉴런 개별의 독립 노이즈만 남음.
        따라서 우리가 161차원의 스파이크 데이터를 받아서 상위 10개 내외의 PC 축으로만 압축(Projection)해 버리면, 수학적으로 **진짜 신호(시그널)는 보존하고, 개별 뉴런의 불필요한 잡음(노이즈)은 통째로 잘라버리게 되는 거임.**
        이렇게 압축된 10차원 정도의 잠재 공간(Latent Space) 데이터를 가지고 다시 타임랙(NUM_LAGS=20)을 만들면, 최종 입력 피처는 200차원 수준으로 획기적으로 줄어듭니다.
        
    
- **운동 지연 (Motor Lag)과 타임 랙 (Time Lag) 피처**
    
    t_spike와 t_movement 사이에는 물리적인 시차 존재. 대략 100~200ms(Motor lag)
    
    시간적 통합 (Temporal Integration) : 뇌는 순간적인 스파이크 한 번으로 근육을 움직이지 않음. 누적된 뉴런 집단(Population)의 발화 패턴을 누적하고 통합하여 점진적인 지령 생성.
    
    - t 시점 1:1 매핑 한계
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2025.png)
    
    모순 : t 시점의 스파이크는 t+15에 일어날 움직임의 원인
    
    - 해결책 : **Time lag, Tap-Delay line**
    
    현재 시점 t를 기준으로 과거 일정 시간 동안의 스파이크 이력을 전부 윈도우로 묶어서 입력 피처로 제공. : Tap-Delay Line
    
    코드 :  현재 시점에서 161개 뉴런의 스파이크 카운트(161x1)만 보는 것이 아니라, t, t-1, t-2 … t-19 시점까지의 데이터를 일렬로 쫙 펼쳐서 **161 x 20 = 3,220 차원의 거대한 입력 벡터**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2026.png)
    
    윈도우 크기 - 과거 20개 빈 (1개 빈 10ms이므로 총 200ms의 과거 이력 반영)
    
    - Code
        
        ### 1. `create_lagged_features` 함수 코드 완벽 쪼개기
        
        이 함수는 원시 데이터(`X_raw`, `Y_vx`, `Y_vy`)를 받아서 타임랙이 적용된 새로운 행렬들을 뱉어냅니다.
        
        ```
        def create_lagged_features(X_raw, Y_vx, Y_vy, num_lags=NUM_LAGS):
            X_lag, vx_lag, vy_lag = [], [], []
        ```
        
        `num_lags` 변수는 맨 위에 `NUM_LAGS = 20`으로 설정되어 있습니다. 즉, "과거 20개 빈(200ms)을 묶겠다"
        
        새로운 타임랙 피처들을 담을 빈 리스트들을 선언합니다.
        
        ```
            for t in range(num_lags, len(X_raw)):
        ```
        
        **루프의 시작점:** 인덱스 `t`가 `0`이 아니라 `num_lags(20)`부터 시작합니다.
        
        ```
                X_lag.append(X_raw[t - num_lags:t, :].flatten())
        ```
        
        - **(Tap-Delay Line의 핵심)**
        
        `X_raw[t - num_lags:t, :]`은 현재 시점 `t`를 기준으로 **바로 직전 과거 20개 빈의 스파이크 데이터**를 슬라이싱(Slicing)한 것입니다. 이 행렬의 shape는 `(20, 161)` 즉, 20개 시간축 161개 뉴런입니다.
        
        여기에 `.flatten()`을 적용합니다. 2차원 행렬 `(20, 161)`이 한 줄로 길게 펴지면서 **`3,220`차원의 1차원 벡터**가 됩니다.
        
        이 1차원 벡터를 `X_lag` 리스트에 차곡차곡 쌓아(append) 거대한 행렬을 만듭니다.
        
        ```
                vx_lag.append(Y_vx[t])
                vy_lag.append(Y_vy[t])
        ```
        
        입력 피처(`X_lag`)는 **과거 20개 빈의 누적 데이터**를 사용하지만, 예측하려는 정답지(`vx_lag`, `vy_lag`)는 오직 현재 시점 `t`의 속도 하나만 매핑합니다.
        
        이 구조 덕분에 모델은 자연스럽게 "과거 200ms 동안의 신경 발화 패턴(원인) → 현재 시점의 손 속도(결과)"라는 생물학적 인과율(Motor Lag)을 정방향으로 학습할 수 있게 됩니다.
        
        ### 2. 차원의 이동으로 보는 데이터의 변화
        
        이 함수를 거치고 나면, 전체 데이터의 형태(Shape)가 다음과 같이 극적으로 변하게 됩니다. (총 시간 빈의 수가 60,000개라고 가정해 봅시다.)
        
        - **함수 통과 전 (원시 데이터):**
            - `X` shape: `(60000, 161)` → 오직 현재 시점의 뉴런 정보만 있음.
            - `Vx` shape: `(60000,)`
        - **함수 통과 후 (타임랙 피처 데이터):**
            - `X_lag` shape: `(59980, 3220)` → 행의 수는 20개 줄어들었지만, **열(변수)의 개수가 161개에서 3,220개로 대폭 확장됨.**
            - `vx_lag` shape: `(59980,)`

**보간 (Interpolation)**

보간법(Interpolation, 내삽)은 **알려진 데이터 점들 사이의 빈 공간을 채워 연속적인 새로운 값을 추정하는 수학적 기법**

- `interp1d` kind: `previous` vs `linear` vs `cubic` 차이
    
    ```python
    from scipy.interpolate import interp1d
    
    # previous: 계단형, 마지막 이벤트 값 유지
    # 이벤트 기반 신호 → 동기 시간축 변환에 적합
    f = interp1d(time_B, traj_B, kind='previous')
    
    # linear: 두 점 사이 직선 보간
    # 연속적 변화 가정 시 사용
    
    # cubic: 3차 스플라인
    # 부드러운 곡선, 하지만 스파이크 같은 급격한 변화에서 오버슈트
    ```
    
- 비동기 신호를 동기 시간축으로 정렬하는 이유
    
    A조: 0, 50, 100, 150ms ... (규칙적)
    
    B조: 10, 23, 47, 91ms ... (불규칙)
    
    R² 계산은 같은 시간축 필요
    
    → B조를 A조 시간점에서의 값으로 보간
    

---

## 3. 디코딩 & 머신러닝

- Binning decoder: 시간 빈 기반 발화율 추정
    
    “일정 시간 구간 내 스파이크 개수 = 발화율”
    
    ```python
    시간 →
    |──50ms──|──50ms──|──50ms──|──50ms──|
    
    bin 1: 스파이크 2개 → 발화율 = 2/0.05 = 40 Hz
    bin 2: 스파이크 0개 → 발화율 = 0 Hz
    bin 3: 스파이크 3개 → 발화율 = 60 Hz
    bin 4: 스파이크 1개 → 발화율 = 20 Hz
    ```
    
    ```python
    bin_size_ms = 50
    time_bins = np.arange(0, duration*1000, bin_size_ms)
    
    for i in range(len(time_bins)-1):
        start_t, end_t = time_bins[i], time_bins[i+1]
        bin_events = [ev for ev in detected_events 
                      if start_t <= ev['timestamp_ms'] < end_t]
        # bin_events의 개수 = 발화율의 proxy
    #총 스파이크수 측정
    ```
    
    문제점
    
    ```python
    실제 스파이크:  t=1ms, t=49ms → 같은 bin
                    t=51ms       → 다음 bin
    
    → 1ms 차이인데 다른 bin으로 분류
    → 시간 정보 손실
    → bin 경계에서 인위적 불연속 발생
    ```
    
- Population Vector Algorithm (PVA)
    
    ### 배경: Georgopoulos 1986
    
    원숭이가 여러 방향으로 팔을 움직일 때 각 뉴런이 **특정 방향에서 가장 강하게 반응**
    
    ```python
    채널 0: 오른쪽(0°)으로 움직일 때 가장 많이 발화
    채널 1: 위쪽(90°)으로 움직일 때 가장 많이 발화
    채널 2: 왼쪽(180°)으로 움직일 때 가장 많이 발화
    채널 3: 아래쪽(270°)으로 움직일 때 가장 많이 발화
    ```
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2027.png)
    
    ```python
    #내 코드에서 스파이크 1개 = 발화율 1단위로 최소화해서 구현
    preferred_directions = {
        0: np.array([1.0,  0.0]),   # 오른쪽
        1: np.array([0.0,  1.0]),   # 위
        2: np.array([-1.0, 0.0]),   # 왼쪽
        3: np.array([0.0, -1.0])    # 아래
    }
    
    # 스파이크 1개 = 발화율 1단위로 단순화
    for ev in detected_events:
        pos_B += preferred_directions[ev['channel']] * weight
    ```
    
    보완점
    
    가정: 뉴런이 정확히 4방향만 선호
    현실: 선호 방향이 연속적으로 분포
    발화율이 코사인 튜닝 곡선을 따름
    
    r(θ) = r_max · cos(θ - θ_preferred) + b
    
    **왜 발화율이 코사인 튜닝 곡선을 따르는가?**
    
    1. 실험적 관찰
        
        원숭이에게 8방향으로 팔을 뻗게 하면서 M1 뉴런을 기록했더니:
        
        `방향      0°   45°  90°  135° 180° 225° 270° 315°
        뉴런 A   30   25   15    8    3    8   15   25  (Hz)`
        
        이 발화율 패턴을 그래프로 그리면 정확히 코사인 곡선
        
    2. 뉴런은 Dot product 계산기
        
        ```python
        뉴런 A의 선호 방향 벡터: d_A = [1, 0]  (오른쪽)
        실제 운동 방향 벡터:     v   = [cos θ, sin θ]
        
        내적: d_A · v = 1×cos θ + 0×sin θ = cos θ
        ```
        
        즉, 뉴런의 발화율(Firing Rate) = 자신의 선호 방향과 실제 운동 방향 사이의 내적
        
        뉴런들이 선호 방향을 균등하게 분포할 경우 이 합산은 정확히 실제 운동 방향 벡터 v에 비례. 
        
        즉, **코사인 튜닝 + 균등 분포 = PVA가 unbiased estimator**.
        
    
    ### PVA의 가정과 한계
    
    | 가정 | 현실 |
    | --- | --- |
    | 코사인 튜닝이 정확함 | 실제로는 비대칭, 비선형 튜닝 존재 |
    | 선호 방향이 균등 분포 | 실제로는 특정 방향에 편중 |
    | 발화율 = 운동 의도만 반영 | 실제로는 위치, 힘, 인지 상태도 혼재 |
    | 뉴런 독립 가정 | 실제로는 강한 상관관계 존재 |
- Linear Regression / Kalman Filter (BCI 표준)
    
    **발화율 벡터 → 움직임 속도를 선형 변환으로 예측**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2028.png)
    
    Linear Regression으로 데이터에서 자동으로 가중치 학습
    
    ```python
    훈련 데이터:
    발화율 행렬 R = [r₁(t₁)  r₂(t₁)  r₃(t₁)  r₄(t₁)]   실제 속도
                    [r₁(t₂)  r₂(t₂)  r₃(t₂)  r₄(t₂)]   v_x(t₁)
                    [  ...      ...     ...     ...  ] → v_y(t₁)
                    [r₁(tₙ)  r₂(tₙ)  r₃(tₙ)  r₄(tₙ)]   ...
    
    최소자승법으로 W 추정:
    W = (RᵀR)⁻¹Rᵀ V
    ```
    
    **Kalman Filter (BCI 표준)**
    
    **"현재 상태를 예측하고, 관측값으로 보정하는 재귀적 추정”**
    
    예측 (운동 모델):  "지금 속도로 계속 움직이면 다음 위치는..."
    보정 (관측 모델):  "실제 뉴런 발화율을 보니 위치가..."
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2029.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2030.png)
    
    K가 크면: 관측값(발화율)을 더 신뢰
    K가 작으면: 예측값(운동 모델)을 더 신뢰
    
    예시:
    뉴런 노이즈 큼(R 큼) → K 작음 → 모델 예측 신뢰
    뉴런 노이즈 작음(R 작음) → K 큼 → 관측 신뢰
    
- **정규화 (Regularization), Optimization - Ridge**
    
    수학에서 최적화 : 특정 집합에 대한 목적 함수를 최소화, 혹은 최대화 시켜 파라미터를 찾는 것.
    
    머신러닝, 딥러닝은 결국 어떤 현상을 잘 설명하기 위한 모델 함수를 찾는 것.
    
    모델 찾을 때, 예측 결과와 실제 결과 간 오차 → 손실 함수
    
    학습 데이터에만 존재하는 노이즈들이 과하게 모델 반영 → 손실 함수가 필요 이상으로 작아짐 → 과적합 or Overfitting
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2031.png)
    
    Overfitting 해결 
    
    1. 학습 데이터 양 늘리기
    2. 배치 정규화
    3. 모델 복잡도 줄이기
    4. 드롭아웃 (Drop-out)
    5. 가중치 규제 : 손실 함수 값이 너무 작아지지 않도록 특정한 값을 추가
        
        → weight 값이 과도하게 커져서 일부 특징에 의존하는 현상 방지
        
        → 데이터의 일반적인 특징 (일반화, Generalization)을 잘 반영
        
    
    대표적인 가중치 규제 → L1 정규화, L2 정규화(Ridge)
    
    Norm - 벡터의 절대적인 크기 or 벡터간 거리
    
    Norm은 특정 속성을 만족, 측정 가능한 기능의 공간 Lp 공간 혹은 르베르 공간에서의 norm을 Lp norm.
    
    n(벡터의 차원 수), P(norm의 차수)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2032.png)
    
    2차원 벡터 공간에서 l1 분포는 마름모, l2는 원. P→infinite → 정사각형 형태
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2033.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2034.png)
    
    L1 norm (맨하탄 거리) - 두 벡터 간의 최단 거리를 찾는데 사용
    
    L1 loss → 실제 값과 예측 값 오차들의 절대값들에 대한 합
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2035.png)
    
    L2 norm (Euclidean distance, p=2) - 두 점 사이의 최단 거리 측정
    
    L2 loss → 실제 값과 예측 값 오차들의 제곱의 합
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2036.png)
    
    - L1, L2 비교
    
    L1은 다른 점으로 이동하는데에 다양한 방법. L2는 단 한 가지의 방법
    
    → L2 norm은 수식에서 오차의 제곱이기에 outlier에 대해 더 큰 영향
    
    Weight의 부호 뿐만 아니라 **그 크기만큼 페널티를 줄 수 있어 특정 weight가 너무 커지는 것을 방지하는 weight decay 가능**
    
    → L1 norm은 다양한 방법 중 특정 방법을 0으로 처리하는 것이 가능하며, 중요한 가중치만 남길 수 있음. L2 대비 outlier에 대해 robust.
    
    But 0에서 미분이 불가능하므로 Gradient-Based Learning 시 주의.
    
    → 편미분 시 weight의 부호만 남기에 weight의 크기에 따라 규제의 크기가 변하지 않으므로 **Regulation 효과가 L2 대비 떨어짐**
    
    - L1 Regulation (Lasso), L2 Regulation (Ridge)
    
    Regulation은 학습 기반 알고리즘에서 모델이 과적합되지 않도록 손실 함수에 특정한 규제 함수를 더하여 손실 함수가 너무 작아지지 않도록 weight에 페널티를 주는 기법임.
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2037.png)
    
    - Lasso : 기존 Cost Function에 가중치의 절대값의 합을 더함
        
        → 미분 시 weight의 크기에 상관 없이 부호에 따라 일정한 상수값을 뺴거나 더해주게 됨. → 특정 Weight들을 0으로 만들기에 Feature selection 가능
        
        → 특정 가중치를 삭제해 모델의 복잡도를 낮출 수 있음
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2038.png)
        
    - Ridge : 기존 Cost Function에 가중치 제곱의 합을 더하는 형태
        
        → Weight의 크기에 따라 weight 값이 큰 값을 더 빠르게 감소시킴.
        
        weight의 크기에 따라 패널티가 달라짐 → 가중치가 전반적으로 작아짐
        
        람다 값에 따라 패널티 조정 가능
        
        ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2039.png)
        
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2040.png)
    
    - λ가 뭘 결정하는가
    
    ```python
    Ridge 목적함수: min ||y - Xw||² + λ||w||²
                         ↑ 예측 오차    ↑ 가중치 크기 패널티
    
    λ 작음 → 패널티 약함 → 가중치 자유롭게 커짐 → 과적합 위험
    λ 큼   → 패널티 강함 → 가중치 전반적으로 작아짐 → 과소적합 위험
    ```
    
    → RidgeCV가 하는 일
    
    ```python
    from sklearn.linear_model import RidgeCV
    
    # 이 한 줄이 내부적으로 하는 일:
    ridge = RidgeCV(alphas=[0.001, 0.01, 0.1, 1, 10, 100])
    ```
    
    - `alphas` 리스트의 각 λ 값에 대해
    - Leave-One-Out Cross-Validation (LOOCV) 또는 k-fold CV 수행
    - 각 λ에서 validation 오차 계산
    - 오차가 가장 작은 λ 선택
    
    **실제로  λ 결정하는 방식**
    
    ```python
    # BCI 논문에서 보통 하는 방식
    alphas = np.logspace(-4, 4, 100)  # 10^-4 ~ 10^4 로그 균등
    
    ridge = RidgeCV(alphas=alphas, cv=5, scoring='r2')
    ridge.fit(X_train, y_train)
    print(f"최적 λ: {ridge.alpha_}")  # 예: 10.5
    ```
    
    **BCI 데이터에서 λ가 크게 나오는 이유:**
    
    - 161개 뉴런이 서로 강하게 상관 → 다중공선성 심각
    - 다중공선성이 심할수록 큰 λ가 필요
    - 3,220차원 time-lag feature에서는 더욱 큰 λ가 최적
    
    뇌 신경 신호는 인접한 뉴런들끼리 비슷한 타이밍에 발화하는 경향이 매우 강함. (강한 상관관계)
    일반 선형 회귀(OLS) 모델에 161개 뉴런 데이터를 그대로 넣으면, 중복된 정보를 가진 뉴런들 때문에 가중치 행렬 계산 시 역행렬이 불안정해지고 가중치가 비정상적임.
    → 릿지(Ridge, L2 정규화). 가중치의 제곱합에 패널티를 부여하여 특정 뉴런에 과도하게 의존하는 것을 막음.
    
     SNN은 복잡한 미분 방정식을 매 시간마다 업데이트해야 하지만, Ridge 디코딩은 칩에 미리 학습된 가중치 행렬(W)을 저장해 두고 단순한 곱셈-덧셈(MAC, Multiply-Accumulate) 연산 한 번만 수행하면 끝.
    
    즉, 깨어있는 시간(Duty Cycle) 자체도 짧고, 깨어났을 때 수행하는 연산도 극도로 단순하기 때문에 진정한 의미의 저전력 임플란트 설계가 완성
    
- **동적 가중치 (Burst)**
    
    뉴런은 Peak 속도가 필요한 시점에 스파이크 Bursting
    
    But, 이 관계가 비선형적. 속도 2배 되었다고 스파이크 카운트 2배 X
    
    속도의 정점에서는 스파이크 빈도가 지수함수적으로 폭발하는 비선형적 튜닝 곡선
    
    Ridge 회귀는 본질적으로 선형모델임. 입력(X, 스파이크 카운트), 출력(Y, 속도) 관계를 일차방정식 (Y = WX + b)로 해석
    
    선형 모델은 전체 데이터의 오차 제곱합을 최소화하는 방향으로 가중치 학습. 이때 데이터에서 base에 근접하는 구간이 90% 이상, peak는 5~10% 미만.
    
    → 선형 디코더는 데이터의 대부분을 차지하는 base 라인에서만 가중치 학습
    
    → 이때 Burst 데이터 만나면 실제 속도 피크를 쫓아가지 못하고 예측값을 아래로 부드럽게 뭉개버리는 과소추정 발생.
    
    - 해결법(Feature Expansion, Expressivity 극대화)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2041.png)
    
    → 다항 회귀와 같은 원리.
    
- Loss 함수
    
    손실 함수는 현재 모델이 얼마나 다르게 예측하는지 숫자로 계량화하는 함수
    
    - 인공지능의 학습 = Loss을 0에 가깝게 만들어주기 위해 가중치 조정
    - Loss 점수 기반으로 역전파(Backpropagation) 기울기가 생성되므로, 수식을 어떻게 설계하느냐(ex. 특정 버스트 구간에 가중치 더 주기)에 따라 모델이 데이터를 학습하는 성향과 전략이 완전히 결정
    
    ### Huber Loss (MSE와 MAE)
    
    - **오차가 작을 때 (정답 근처)** : 오차가 설정된 임계값(sigma)보다 작으면 **MSE(제곱 오차)** 형태로 작동한다. 최적점 근처에서 미분 값이 부드럽게 감소하므로 웅덩이 중심부로 안정적으로 수렴함.
    - **오차가 클 때 (이상치 구간)**

**평가지표**

- R² (결정계수): 1에 가까울수록 완벽한 예측
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2042.png)
    
    SS_tot: "평균으로만 예측했을 때의 오차"
    SS_res: "모델로 예측했을 때의 오차"
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2043.png)
    
    R² = 1 - (모델 오차 / 평균 오차)
    = 모델이 분산을 얼마나 설명하는가
    
    R² = 1.0        완벽한 예측
    R² > 0.9        매우 좋음 (논문 수준)
    R² > 0.7        좋음
    R² = 0.0        평균만큼만 예측 (모델 의미 없음)
    R² < 0.0        평균보다 나쁨 (심각)
    
    **시계열 교차 검증 (Time-Series Cross-Validation)**
    • **Data Leakage (정보 누설):** 시계열 데이터를 일반적인 K-Fold로 무작위 섞기(Shuffle) 해버리면, 미래의 정보가 과거를 예측하는 데 쓰이는 치명적인 오류가 발생.
    → 데이터를 시간 순서대로 쪼개고, 훈련 데이터가 항상 테스트 데이터보다 과거에 있도록 구성하는 기법(예: TimeSeriesSplit)
    
    - 우리 코드의 한계
    
    같은 trial 안에서 앞 bin이 뒷 bin을 "예언"하는 정보를 모델이 이미 학습한 상태 → **data leakage**
    
    ```python
    r이 과대평과 되었을 수 있음.
    실제 상황:
    - Trial 내 bin들은 smooth한 운동 궤적을 공유
    - bin t와 bin t+1의 신경 신호는 매우 비슷
    - 모델이 "t 시점의 신호 → t 시점 속도" 패턴을 학습할 때
      같은 trial의 다른 bin에서 이미 본 패턴을 활용
    
    결과:
    - 성능이 부풀려짐
    - 진짜 일반화 성능(새로운 trial)보다 높게 측정됨
    ```
    
- Correlation coefficient (r): 논문 Fig.4f의 핵심 지표
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2044.png)
    
- 결졍계수, correlation coefficient 차이
    
    → r = 선형 관계의 방향 + 강도 (-1 ~ +1)
    
    → R^2 = 분산 설명력 (음수 ~ 1)
    
    ```python
    실제:   [1, 2, 3, 4, 5]
    예측 A: [2, 4, 6, 8, 10]  ← 2배 스케일 차이
    
    r   = 1.0   (완벽한 선형 관계)
    R²  = 낮음  (스케일 다르므로 분산 설명 못함)
    
    → r은 스케일 무관, 방향/강도만 측정
    → R²는 실제 예측 정확도 측정
    ```
    
- Spike Error Rate (SER): 논문에서 쓰는 전송 오류 지표
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2045.png)
    
    SER = 10⁻⁴  →  r_SER/r_neural ≈ 1.0   (거의 손실 없음)
    SER = 10⁻³  →  r_SER/r_neural ≈ 0.89  (11% 성능 저하)
    SER = 10⁻²  →  r_SER/r_neural ≈ 0.70  (30% 성능 저하)
    

**모델**

- **SNN (Spiking Neural Network)** ← 논문 재현 시 필요
    
    발화율 코딩 (Rate Coding) vs 시간 코딩 (Temporal Coding)
    
    **Rate Coding (프로젝트 빈(Bin) 방식, PVA, Ridge)**
    
    → 일정 시간(50ms) 동안 뉴런이 **몇 번** 발화했는가?"가 정보의 핵심
    
    → 시간적 해상도는 떨어지지만 노이즈에 강함
    
    **Temporal Coding (SNN):**
    
    → 스파이크가 정확히 몇 밀리초(ms)에 발생했는가?" 자체가 정보.
    
    → 스파이크 간의 간격(Inter-Spike Interval) 패턴을 학습하기 때문에 시간 타이밍이 중요.
    
- Leaky Integrate-and-Fire (LIF) 뉴런 모델

---

## 4. 통신/하드웨어 (논문 이해용)

**RF 통신 기초**

- Backscattering: 능동 송신 없이 반사로 통신하는 원리

```python
일반 무선 통신 (스마트폰):
  배터리 → 증폭기 → 안테나 → 전파 송신
  
  능동적으로 전력을 써서 신호를 "만들어서" 보냄
  → 배터리 필요, 전력 소모 큼

Backscattering (교통카드, BCI 임플란트):
  외부 리더기가 강한 전파를 쏨
                    ↓
  임플란트 안테나에 전파가 도달
                    ↓
  안테나의 "반사율"을 조절해서 신호 전달
  → 자체 전력 송신 없음, 에너지 소모 극소
```

원리 : 임피던스 매칭 조절

→ 안테나에 연결된 부하(load)의 저항값을 바꾸면 반사되는 전파의 양 조절

```python
부하 저항 = 안테나 임피던스와 일치:
  → 전력이 안테나에 최대로 흡수됨
  → 반사 거의 없음 → 리더기에 약한 신호 도달 → "0"

부하 저항 = 안테나 임피던스와 불일치:
  → 전력이 반사됨
  → 반사 강함 → 리더기에 강한 신호 도달 → "1"
```

```python
리더기                    임플란트
  ~~~전파 송신~~~>        [안테나]
                              ↕ (부하 조절)
  <~~~반사파 수신~~~      [스위치: ON/OFF]

스위치 ON  (부하 연결): 흡수 → 반사 약함 → "0"
스위치 OFF (부하 해제): 반사 강함        → "1"
```

```python
뇌 임플란트의 현실:
  - 뇌 안에 배터리 교체 불가
  - 발열 제한: 체온 상승 0.5°C 이하
  - 크기 제한: 수 mm²

해결책: Backscattering
  - 자체 전파 송신 없음
  - 스위치 ON/OFF만으로 통신
  - 소비 전력: 수 μW 수준
  - 외부 코일이 에너지 공급 + 통신 동시에 담당
  
  단점:
  - 통신 거리 짧음 (수 cm ~ 수십 cm)
  - 리더기와 임플란트 사이에 장애물 있으면 약해짐
  - 외부 리더기가 항상 전파를 쏘고 있어야 함
```

- ASK-PWM 변조: 진폭으로 0/1 인코딩
- BPSK: 위상으로 0/1 인코딩
- Duty cycle: 전력 절감의 핵심 개념

**CDMA & Gold Code**

- Code Division Multiple Access: 같은 주파수를 여러 노드가 쓰는 방법
- Gold code: 준직교 의사난수 코드, 노드 식별자로 사용
- Matched filter: 수신단에서 특정 노드 신호만 복원

**ASBIT 프로토콜** (논문 핵심)

- Asynchronous Sparse Binary Identification Transmission
- 이벤트 없으면 전송 없음 → sparsity 활용
- EER (Event Error Rate): 전송 정확도 지표

**에너지 수확 (Energy Harvesting)**

- RF → 전력 변환 (정류기 회로)
- OVP (Over Voltage Protection)
- Near-field inductive coupling vs Far-field

---

## 5. 구현 도구

# 학습 모델

## Ridge

![image.png](Notion%20for%20Event-driven-bci-decoding/image%2046.png)

- **Kalman**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2047.png)
    
    칼만 필터는 시계열 데이터에서 상태 추정을 위한 알고리즘, 관찰 데이터(Observed data)의 노이즈와 시스템 모델의 불확실성이 있는 상황에서 시스템의 상태를 예측값과 노이즈가 포함된 관찰 데이터를 바탕으로 재귀적으로 예측, 보정
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2048.png)
    
    1. 예측 (prediction)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2049.png)
    
    1. 갱신 (Update)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2050.png)
    
    **실시간 시스템 제어, 사전 대응 가능.** 
    
    선형 시스템과 가우시안 노이즈를 가정하므로 비선형성 모델링 및 노이즈가 논가우시안인 경우 어려움 겪음.
    
- **MLP (Multi-Layer-Perceptron)**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2051.png)
    
    MLP란 **여러 개의 퍼셉트론 뉴런**을 **여러 층**으로 쌓은 다층신경망 구조
    
    입력과 출력 사이에 하나 이상의 은닉층.
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2052.png)
    
    - 다층 뉴런이 필요한 이유
        
        복잡한 패턴 분류를 위해서는 입출력 간의 복잡한 변환 구조가 필요함.
        
        단일뉴런(퍼셉트론)으로는 선형 분리 가능한 경계선만 생성 가능함.
        
        **두 개의 뉴런을 결합함으로써 XOR과 같은 비선형 분리가 가능한 결정선 생성가능.**
        
    
    **1. 활성화 함수**
    
    퍼셉트론에서는 step 함수 (계단 함수) 를 활성화 함수로 사용,
    
    MLP 에는 다양한 비선형 함수들을 활성화 함수로 사용
    
    인공 신경망을 통과해 온 값을 최종적으로 어떤 값으로 만들지.
    
    1) step function : 임계값을 미리 설정하고 (threshold value) 임계값 보다 크면 1, 아니면 0
    
    2) Sigmoid fuction : [0,1] 사이의 값
    
    3) Linear function : y =x
    
    4) tanh function : [-1, 1] 사이의 값
    
    5) **ReLu function** : 양수이면 그대로 , 음수이면 0
    
    6) Leaky ReLU
    
    7) ELU
    
    2. 손실 함수 : 전체 오차는 목표 출력값에서 실제 출력값을 빼서 제곱한 값을 모든 출력 노드에 대하여 합한 값이다 => 평균제곱법(MSE)
    
    3. 역전파 알고리즘 (EBP : Error BackPropagation) : 입력이 주어지면 순방향으로 계산하여 출력을 계산한 후에 실제 출력과 우리가 원하는 출력 간의 오차를 계산한다. 오차를 역방향으로 전파하면서 오차를 줄이는 방향으로 가중치를 변경한다.
    
    4. 다층 신경망의 활용: 다양한 지도 학습 문제에 적용 가능, MNIST 데이터셋에 적용, 스팸 여과기 만들기 !
    
- **LSTM (Long-Short Term Memory)**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2053.png)
    
    LSTM은 RNN(Recurrent Neural Network)의 장기 의존성 문제를 해결하고자 등장.
    
    - 장기 의존성 문제 : 시퀀스의 길이가 길어질수록 과거의 정보가 잊혀져 마지막까지 전달되지 못하는 문제.
        - RNN은 과거의 정보를 hidden state에 저장하며 시퀀스 데이터를 처리하지만, 시퀀스가 길어지면 이전에 저장된 정보가 점차 잊혀져 긴 문맥 이해하는데 한계
    
    Gate구조와 Cell state 구조 도입 → **단기기억과 장기기억 나눠서 처리 가능**
    
    1. Cell state(Ct) 장기 기억 담당. 시퀀스의 정보를 장기적으로 누적하여 전달하는 역할. Forget gate에서 저장된 장기 정보의 일부는 지워지고, input gate에서 현재 정보의 일부가 새롭게 누적되어야 함.
    2. Hidden state 단기기억 담당 : 시퀀스의 단기적인 상태 요약. 현재 시점의 output으로 사용되면서 다음 시점의 연산에 필요한 단기적 정보로 제공
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2054.png)
    
    내부에는 두가지 활성화 함수인 tanh(-1 ~ 1), sigmoid(0 ~ 1) 사용.
    
    Tanh : 저장/출력할 정보의 값을 구하기 위해 사용
    
    Sigmoid : 기억/저장/출력할 정보의 비율을 구하기 위해 사용
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2055.png)
    
    **Forget Gate**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2056.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2057.png)
    
    ft는 시그모이드가 적용된 값으로 이전 cell state를 기억할 비율
    
    ft 계산 이후 Ct-1과 element-wise product 수행
    
    → 이전 cell state의 일부 사라짐
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2058.png)
    
    **Input Gate**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2059.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2060.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2061.png)
    
    **Output Gate**
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2062.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2063.png)
    
    ![image.png](Notion%20for%20Event-driven-bci-decoding/image%2064.png)
    
    활용 : 
    
    One-to-Many : 하나의 입력을 넣고 출력 시퀀스를 얻는 경우 (Image Captioning)
    
    Many-to-One : 시퀀스 입력 넣고 하나의 출력 (Sentiment classification)
    
    Many-to-Many : 시퀀스 입력 넣고 시퀀스 (Machine translation)
    
    Learning Rate → 모델이 오차를 줄이기 위해 가중치를 한 번 업데이트를 할 때 이동할 보폭. 너무 크면 최적 위치 지나쳐 발산, 작으면 학습 속도가 지나치게 느려지거나 로컬 미니마에 갇힘.
    
    **Adam Optimizer (Adaptive Moment Estimation)** : 현재 딥러닝에서 가장 널리 쓰이는 표준 최적화 알고리즘. 경사하강법(SGD)의 단점을 보완하기 위해서 방향(관성)과 보폭(맞춤형 변형)을 모두 고려함
    
    - Momentum(관성) : 기울기가 0에 가까운 평지를 만나도 이전의 관성을 이용해 웅덩이 탈출하도록 돕는다.
    - RMSProp(적응형 보폭) : 자주 변하는 가중치는 소폭으로, 변화가 적은 가중치는 큰폭으로 업데이트
    

---

```
1순위 (지금 당장)
├── MAD threshold 원리 O
├── Population Vector Algorithm 수식 O
├── R² vs Correlation 차이 O
└── Duty cycle 개념

2순위 (논문 재현 시)
├── Gold code 생성 원리
├── Matched filter 동작
├── SER vs 디코딩 성능 관계
└── CRCNS 데이터 로딩

3순위 (대학원 진학 후)
├── HH 모델 미분방정식
├── SNN / LIF 뉴런
├── Kalman Filter BCI 디코더
└── ASIC 회로 설계
```

---