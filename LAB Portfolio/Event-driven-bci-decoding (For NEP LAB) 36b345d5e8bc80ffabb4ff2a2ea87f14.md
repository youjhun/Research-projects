# Event-driven-bci-decoding (For NEP LAB)

[LAYER 1] Raw Input & Preprocessing (입력 및 생물학적 보정)

```jsx
[ 원숭이 Sequential Reaching MAT 데이터 ]
  │
  ├── 1) Neural Matrix 추출 ──> M1 + PMd 피처 결합 (X_cpu)
  └── 2) Kinematics 추출   ──> 손동작 Vx, Vy 속도 (Vx_cpu, Vy_cpu)
  
RAW 데이터 : .mat에서 추출한 Reach 별 데이터 리스트. 
각 Reach의 시간을 T, 채널 수를 D라 하면, 각 Reach 요소는 (T, D)

 X_cpu : 모든 Reach 데이터가 시간축(수직)으로 쭉 이어 붙여짐. 
 총 타임 스텝 합을 N이라 할 때, (N, D)
```

- X_cpu : Tensor 이동 전, CPU 상에 존재하는 일반 Array 배열
    - np.vstack : (t1,d), (t2,d) → (t1+t2, d) - 열 크기만 고정
    - np.concatenate : 특정 축을 기준으로 길게 결합
        
        [(t1), (t2)] → (t1+t2)
        
    - (D) 벡터 3개를 concatenate → (3*D), np.stack → (3,D)

[LAYER 2] Feature Engineering & Model-Specific Inputs (디코더별 피처 커스텀)

```jsx
[ X_cpu (Raw Spikes) ]
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
   [ 1D Time-Bin ]       [ Sliding Window Lags ]   [ Peak-Aware Feature Extraction ]
  (현재 시점 스파이크)       (과거 200ms 시간 축 축적)   (집단 발화 및 가속도 온셋 분석)
         │                       │                       │
         │ (O(1) Stride Tricks)  │ (O(1) Stride Tricks)  ├── burst_score / burst_mean
         ▼                       ▼                       ├── max_spike / active_ratio
   [ Kalman Input ]        [ Lagged Feature ]            └── onset_ratio (최신/과거 비율)
         │                       │                               │
         ▼                       ▼                               ▼
  💡 Dynamic Weighting    💡 Dynamic Weighting             [ Peak Feats Matrix ]
  (Spike > 0, Power 1.3)  (Spike > 0, Power 1.3)                 │
         │                       │                               │
         ▼                       ▼                               ▼
 ┌───────────────┐       ┌────────────────────────┐              │
 │ Kalman Input  │       │ Ridge / LSTM / MLP Main│              │
 └───────┬───────┘       └───────────┬────────────┘              │
         │                           │                           │
         │                           ├───────────────────────────┼──────────────┐
         ▼                           ▼                           ▼              ▼
   (Kalman 전용)                (Ridge 전용)                (MLP 전용)     (LSTM 전용)
   [ 1D Array ]                 [ 2D Flattened ]           [ PCA 128D ]    [ 3D Sequence ]
```

- X_lag(Ridge, MLP용 - Flattened Lag Features) (N - num_lags, num_lags * D)
    - 선형 모델이나 단순 신경망은 입력 데이터 간의 순서나 시계열적 3차원 구조를 스스로 인지하지 못함. 따라서 num_lag 동안의 스파이크 정보를 가로로 길게 펼쳐서 주입
    - 200ms 동안 일어난 전체 채널의 발화 패턴을 고차원 공간(num_lags X D) 속 point로 매핑. → 모델은 공간 상의 점들 사이를 가르는 경계선을 그어 속도 예측.
- X_seq (LSTM용 - Sequential Features) (N - num_lags, num_lags, D)
    - LSTM은 시계열의 흐름과 맥락을 단계별로 기억하는 순환 신경망.
    - 샘플 개수, 과거 시간 스텝 수, 뉴런 채널 수라는 3차원 구조 유지가 되어야 LSTM 셀이 매 스텝 순차적으로 기억 세포 업데이트 가능
    - 데이터를 점이 아닌 시계열 궤적(선)으로 다루는 것.
- X_obs (Kalman Filter용 - Pure Observation) (N-num_lags, D)
    - 칼만 필터는 확률론적 상태 공간 모델 → 현재 상태(손의 속도)는 직전 상태와 현재 시점의 관측값에 의해서만 결정된다 가정.
        
        → 과거의 이력을 수식 내에서 자체적으로 누적. 굳이 과거 묶을 필요 X
        
    - 현재 타겟 시점과 동기화된 뇌의 Snapshot 공간을 그대로 사용.

[LAYER 3] Multi-Decoder Processing & Optimization (디코딩 및 모델 학습)

```jsx
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ 🔄 5-Fold Time-series Cross Validation (시간 연속성 유지 분할, No Shuffle)             │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ ▼ [Decoder 1] Kalman  │ ▼ [Decoder 2] Ridge  │ ▼ [Decoder 3] MLP   │ ▼ [Decoder 4] LSTM│
│                       │                      │                     │                   │
│ • Steady-State        │ • GPU Ridge Regression│ • Dual-Stream Net   │ • 2-Layer LSTM     │
│   Riccati 방정식 반복  │ • L2 정규화 최적화   │   (PCA + Peak 결합) │ • Temporal Flow   │
│ • 선형 상태공간 모델   │ • 차원 변환 연산     │ • PeakAwareLoss     │ • Hidden Dim 128  │
│   (A, H, Q, R 추정)   │                      │   (Huber + 가속도가중)│ • MSE Loss 최적화 │
│                       │                      │ • Mixed Precision   │                   │
│                       │                      │   (FP16 AMP 가속)    │                   │
└───────────┬───────────┴───────────┬──────────┴───────────┬─────────┴─────────┬─────────┘
            │                       │                      │                   │
            ▼                       ▼                      ▼                   ▼
      [ Kalman Pred ]          [ Ridge Pred ]         [ MLP Pred ]        [ LSTM Pred ]
```

[LAYER 4] Post-Processing & Evaluation (후처리 및 벤치마킹 시각화)

```jsx
[ Kalman / Ridge / MLP / LSTM Raw Predictions ]
                          │
                          ▼
             💡 Gaussian Smoothing Filter (GAUSS_SIGMA = 3)
             (노이즈 제거 및 부드러운 손동작 궤적 복원)
                          │
                          ├─────────────────────────────────────┐
                          ▼                                     ▼
             [ Metric Evaluation ]                     [ Visualization (PHASE 4) ]
  • Pearson r (정밀도 지표)                              • Fig 1: Baseline Performance
  • VAF (분산 설명도)                                     - Decoder 간 r, VAF, Scale 비교
  • RMSE (절대 오차 범위)                                 - 논문 SNN 기저선(0.9324)과 벤치마킹
  • Scale Bias (실제 대비 예측 진폭 비율)                • Fig 3: Time-Series Tracking
                                                          - 실제 쥐/원숭이 궤적과 모델별 복원
                                                            스트리밍 데이터 실시간 오버레이
```

[BCI_EventDriven_NeuralDecoding_v2.pdf](Event-driven-bci-decoding%20(For%20NEP%20LAB)/BCI_EventDriven_NeuralDecoding_v2.pdf)

[Event-Driven Neural Decoding in Brain-Computer Interfaces_    Design, Validation, and Robustness Analysis.pdf](Event-driven-bci-decoding%20(For%20NEP%20LAB)/Event-Driven_Neural_Decoding_in_Brain-Computer_Interfaces_____Design_Validation_and_Robustness_Analysis.pdf)

[BCI_종합연구보고서.docx](Event-driven-bci-decoding%20(For%20NEP%20LAB)/BCI_%EC%A2%85%ED%95%A9%EC%97%B0%EA%B5%AC%EB%B3%B4%EA%B3%A0%EC%84%9C.docx)

[Notion for Event-driven-bci-decoding](Event-driven-bci-decoding%20(For%20NEP%20LAB)/Notion%20for%20Event-driven-bci-decoding%2036b345d5e8bc80c59980e20a454ceb40.md)

[CRCNS pmd-1 기반 프로젝트](Event-driven-bci-decoding%20(For%20NEP%20LAB)/CRCNS%20pmd-1%20%EA%B8%B0%EB%B0%98%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%2036d345d5e8bc803aa42dd75f6182a773.md)

[CODE](Event-driven-bci-decoding%20(For%20NEP%20LAB)/CODE%20375345d5e8bc803193e8ffa282e0e1ac.md)