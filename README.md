# Event-Driven Neural Decoding — SER robustness on CRCNS pmd-1

무선 BCI에서 **스파이크 전송 오류(SER, Spike Error Rate)가 늘어날 때 운동 디코딩 성능이 얼마나
무너지는가**를 공개 영장류 데이터로 독립 재현하고, 원 논문에 없던 **붕괴하지 않는 이유**를 실험으로
설명한 기록이다.

> **상태 (2026-08-04)**: 결과까지 도달했고 보고서·코드가 있으나, 외부인이 그대로 재현할 수 있는
> 상태는 아니다. 아래 §5 재현 · §6 한계에 무엇이 검증됐고 무엇이 안 됐는지 그대로 적었다.

---

## 1. 질문

무선 신경 임플란트는 채널 대역폭·전력 제약 때문에 스파이크 손실과 오검출이 불가피하다.
그래서 설계자는 **"오류를 얼마나 허용해도 행동 정보가 보존되는가"**를 알아야 한다.

원 논문(Nature Electronics, 2024)은 SNN 디코더로 이 트레이드오프를 제시했으나 **코드와 방법이
공개되지 않았다.** 그래서 다음을 했다.

| | 원 논문 | 이 작업 |
|---|---|---|
| 데이터 | Fagg 2009 (M1+S1, center-out) | **CRCNS pmd-1** (M1+PMd, sequential reaching) |
| 디코더 | SNN | **Ridge / MLP / LSTM / Transformer / Kalman** |
| 언어·공개 | MATLAB, 비공개 | Python, 공개 |
| 산출 | SER↔성능 곡선 | 같은 곡선 + **왜 그런지에 대한 메커니즘 실험** |

## 2. 데이터

CRCNS **pmd-1** (Perich et al., 2018). 마카크 1개체, M1 67ch + PMd 94ch = **161 뉴런**,
**496 reach trial**, 10 ms bin(100 Hz). 스파이크 행렬 59,742 × 161, 총 587,914 스파이크,
희소율 **93.89%**, 평균 발화율 6.41 Hz.

## 3. 핵심 결과

### 3.1 기저 성능 (SER=0, trial-level CV)

| Decoder | r | VAF | Scale Bias(x) |
|---|---|---|---|
| Ridge | 0.8701 | 0.740 | 0.856 |
| **MLP** | **0.9209** | 0.842 | 0.880 |
| LSTM | 0.8945 | 0.789 | 0.842 |
| Transformer | 0.9097 | 0.819 | 0.813 |
| *원논문 SNN* | *0.9324* | — | — |

### 3.2 SER 강건성 — 재현의 핵심

| SER | rate-coded (이 작업) | SNN (원논문) |
|---|---|---|
| 1e-4 | 1.0000 | ~1.000 |
| 1e-3 | 0.9999 | **0.888** |
| 1e-2 | 0.9988~0.9991 | **~0.700** |
| 5e-2 | 0.9955 | — |
| 1e-1 | 0.9880 | — |
| 2e-1 | 0.9764 | — |

(retention ratio = r_SER / r_clean)

**rate-coded 디코더 4종은 전부 SER=1e-2에서 retention ≥0.996인 반면, spike-timing 기반 SNN은
같은 조건에서 0.700으로 무너진다.** 실제 breakdown point는 **SER 0.1~0.2** 부근이며, 이는 SNN이
이미 붕괴한 지점보다 한 자릿수 뒤다.

### 3.3 왜 안 무너지는가 — population averaging (원 논문에 없는 기여)

가설: 뉴런이 많으면 개별 스파이크 오류가 population 평균에서 희석된다.

- N=161, bin당 활성 뉴런 ≈ 9.8개 → SER=0.01에서 bin당 손상 채널 ≈ **0.1개** (희석 ≈ 1/10)
- **뉴런 subsampling 실험(N=40 vs 161)** 으로 직접 검증 — 뉴런 수를 늘릴수록 retention 곡선이 개선

즉 강건성의 출처는 디코더 아키텍처가 아니라 **표현 방식(rate vs spike-timing)과 population 크기**다.
설계 함의: 저전력 무선 BCI에서 채널 수를 확보하면 오류 내성 마진을 살 수 있다.

### 3.4 Transformer attention

trial-level CV + **causal mask**(실시간 BCI는 미래를 못 본다) 조건에서 layer별 attention peak lag
L1 = 0 ms, L2 = −20 ms, L3 = −10 ms — motor cortex의 movement onset 전 준비 활동과 정합하는
계층적 temporal processing 패턴.

## 4. 방법에서 스스로 고친 것

- **trial-level CV로 재설계.** bin 단위 KFold는 trial 경계 내부를 잘라, 운동 궤적의 trial 내 상관이
  train/test에 걸쳐 새어 들어간다(leakage). trial 단위로 분할해 제거.
- **affine rescaling을 train split에서만 fit** 해 test에 apply — 시각화 단계의 leakage 차단.
- **causal mask** — 미래 방향 attention을 상삼각 마스킹.
- 학습용(`need_weights=False`)과 attention 추출용 클래스를 분리해 매 step의 weight 저장 낭비 제거.

## 5. 재현

> ⚠️ **아직 한 번도 "깨끗한 환경에서 처음부터" 재현해 본 적이 없다.** 아래는 코드에서 읽어낸
> 실행 조건이며, 이 저장소만으로 재현이 완결되지 않는다.

- **실행 환경**: Google Colab (스크립트가 `google.colab.drive`를 직접 import). CUDA 사용.
- **데이터**: CRCNS pmd-1의 `MM_S1_processed.mat`. CRCNS는 계정 신청이 필요하며
  이 저장소에 데이터는 포함되지 않는다. 스크립트는 Google Drive 경로
  `/content/drive/MyDrive/data_and_scripts/source_data/processed/MM_S1_processed.mat`를 가정한다.
- **의존성**: `scipy`, `numpy`, `scikit-learn`, `matplotlib`, `torch`.
  스크립트가 `requirements.txt`를 설치하는데, **그 파일은 이 저장소가 아니라 별도 저장소에 있다**(아래).
- **코드 원본 저장소**: `github.com/youjhun05/A-Software-Validation-Using-Macaque-Motor-Cortex-Data-pmd-1-`
  — 스크립트가 런타임에 clone한다. ⚠️ **계정이 다르다**(`youjhun05` ≠ `youjhun`).

**재현을 완결하려면 남은 것**

1. Colab 의존(`drive.mount`, `!pip`, `!git clone`)을 분리해 로컬에서도 도는 진입점 만들기
2. `requirements.txt`를 이 저장소로 가져와 버전 고정
3. 데이터 획득 절차 문서화 (CRCNS 계정 → 파일 → 배치 경로)
4. 결과 표와 그림을 **한 번의 명령으로 재생성**해 위 §3 숫자와 대조

## 6. 한계 (정직하게)

- **인과가 아니다.** SER↔성능은 시뮬레이션된 오류 주입 결과이며, 실제 ASBIT 프로토콜의 채널 모델을
  적용한 검증은 하지 않았다.
- **단일 피험자·단일 세션**(MM_S1). 일반화 주장 불가.
- **SNN을 직접 돌리지 않았다.** 비교 대상 SNN 수치는 원 논문 보고값을 인용한 것이고 데이터셋도 다르다.
  따라서 이 작업이 보인 것은 **"같은 SER 범위에서 rate-coded는 무너지지 않았다"**이지,
  head-to-head 우열이 아니다.
- **Transformer가 baseline에서 MLP보다 낮다.** T=20의 짧은 시퀀스에서 attention이 과설계일 수 있다.
- 보고서 PDF 본문에 한계·다음 실험 절이 있는지는 **미확인**(2026-08-04 기준 PDF 미열람).

## 7. 열린 질문 / 다음 실험

Obsidian vault의 `Experiments/`에 기록된 미해결 항목:

- **왜 Transformer가 SER ≥1e-2에서 MLP·LSTM과 비슷해지는가?**
  가설 ① population averaging이 아키텍처 차이를 덮는다 ② 짧은 시퀀스에서 attention이 의미를 잃는다.
  → SER 0 / 1e-3 / 5e-2 / 1e-1에서 attention heatmap을 겹쳐 diffuse 여부를 본다.
- **Burst SER**(연속 손실)이 random SER과 같은 곡선을 그리는가 — 실제 무선 채널은 랜덤이 아니다.
- **저데이터 영역**: 100 trial만 쓸 때 SER 손상이 커지는가, 그리고 VAE 증강이 그 손상을 메우는가
  (`Experiments/04 - Quality Gate`, `07 - Augmented Decoding`).

## 8. 파일 지도

```
LAB Portfolio/
├── Event-driven-bci-decoding (For NEP LAB)/
│   ├── bci_event_driven_v1.py                    # 4-디코더 통합 파이프라인 (727줄)
│   ├── Event-Driven_Neural_Decoding_in_BCI....pdf # 종합 보고서
│   ├── BCI_EventDriven_NeuralDecoding_v2.pdf
│   └── CRCNS pmd-1 기반 프로젝트/
│       ├── crcns_pmd_1.py                        # SER 재현 본체 (1,824줄)
│       └── bci_ser_report.pdf                    # SER 보고서
├── Attention-based Neural Decoder Transformer vs LSTM/
│   ├── attention_..._on_pmd_1.py                 # 4-디코더 + attention 분석 (1,911줄)
│   └── Attention_based_Neural_Decoder....pdf
└── KAIST NEP Lab 6 papers report/
    ├── Distributed_Wireless_Microimplant_BMI....pdf  # Neurograin 6편 종합 리뷰
    └── (원논문 PDF 2편)

Obsidian Vault/          # 개념 계층 + 실험 노트 (md 57편)
├── Concepts/            # spike train → decoding → SER → population averaging → VAE
└── Experiments/         # 00~07, 각 실험의 design·결과·해석·미해결 질문

Research.zip             # 위 트리의 Notion export 원본 (중복 — 정리 대상)
```

## 9. 원 논문 / 참고

- Nature Electronics 2024 — *An asynchronous wireless network for capturing event-driven data
  from large populations of autonomous sensors* (ASBIT 프로토콜 + SNN 디코딩).
  이 작업이 재현한 SER↔성능 트레이드오프의 출처.
  <https://www.nature.com/articles/s41928-024-01134-y>
- Nature Electronics 2021 — *Neural recording and stimulation using wireless networks of
  microimplants* (Neurograin 개념의 출발점).
- CRCNS pmd-1 — Perich et al., 2018.
