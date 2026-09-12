# Event-Driven Neural Decoding — SER robustness on CRCNS pmd-1

무선 BCI에서 **스파이크 전송 오류(SER, Spike Error Rate)가 늘어날 때 운동 디코딩 성능이 얼마나
무너지는가**를 공개 영장류 데이터로 검증하려는 연구 기록이다. 과거 분석과 보고서를 보존하되,
2026-09-12부터는 누수 없는 기준선 재현을 먼저 확정한 뒤 강건성 설명을 다시 시험한다.

> **상태 (2026-09-12 코드 감사)**: 아래 수치는 과거 파이프라인이 산출한 **legacy claim**이며,
> 깨끗한 환경에서 독립 재현된 결과가 아니다. 감사 결과 기존 `trial-aware` 구현에는 train/test
> trial 혼입과 trial 경계를 넘는 lag window 문제가 있었고, burst 오류 구현도 iid 조건과 같은 오류량을
> 비교하지 않았다. 따라서 현재 수치를 검증된 연구 결과로 인용하지 않는다. 새
> [`reproduction/r0_ridge.py`](reproduction/r0_ridge.py)가 corrected baseline의 정본이다.

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

## 3. 과거 보고 결과 — 재검증 전

### 3.1 기저 성능 (legacy report; clean trial-level CV 미확인)

| Decoder | r | VAF | Scale Bias(x) |
|---|---|---|---|
| Ridge | 0.8701 | 0.740 | 0.856 |
| **MLP** | **0.9209** | 0.842 | 0.880 |
| LSTM | 0.8945 | 0.789 | 0.842 |
| Transformer | 0.9097 | 0.819 | 0.813 |
| *원논문 SNN* | *0.9324* | — | — |

### 3.2 SER 강건성 (legacy report; 현재 증거로 사용 금지)

| SER | rate-coded (이 작업) | SNN (원논문) |
|---|---|---|
| 1e-4 | 1.0000 | ~1.000 |
| 1e-3 | 0.9999 | **0.888** |
| 1e-2 | 0.9988~0.9991 | **~0.700** |
| 5e-2 | 0.9955 | — |
| 1e-1 | 0.9880 | — |
| 2e-1 | 0.9764 | — |

(retention ratio = r_SER / r_clean)

과거 분석은 **rate-coded 디코더 4종이 SER=1e-2에서 retention ≥0.996**이라고 보고했다. 그러나
clean baseline과 오류 모델이 다시 검증되기 전에는 SNN 대비 우위나 breakdown point를 주장하지 않는다.

### 3.3 제안했던 설명 — population averaging (미검증 가설)

가설: 뉴런이 많으면 개별 스파이크 오류가 population 평균에서 희석된다.

- N=161, bin당 활성 뉴런 ≈ 9.8개 → SER=0.01에서 bin당 손상 채널 ≈ **0.1개** (희석 ≈ 1/10)
- **뉴런 subsampling 실험(N=40 vs 161)** 으로 직접 검증 — 뉴런 수를 늘릴수록 retention 곡선이 개선

이 결과 역시 corrected R0 이후 동일 오류량을 보장하는 R1로 다시 실행해야 한다. 현 단계에서는
**표현 방식과 population 크기가 강건성에 기여할 수 있다**는 후보 가설로만 둔다.

### 3.4 Transformer attention

trial-level CV + **causal mask**(실시간 BCI는 미래를 못 본다) 조건에서 layer별 attention peak lag
L1 = 0 ms, L2 = −20 ms, L3 = −10 ms — motor cortex의 movement onset 전 준비 활동과 정합하는
계층적 temporal processing 패턴.

## 4. 코드 감사에서 확인한 방법론 문제

- 기존 `make_trial_folds`는 train trial ID 자체를 선택하지 않고 연속 bin 범위를 만들기 때문에 일부
  held-out trial이 train에 포함된다.
- 전체 trial을 먼저 이어 붙인 뒤 lag window를 만들기 때문에 서로 다른 reach trial 사이를 가로지르는
  가짜 시간 문맥이 생긴다. lag 이후 bin index와 원래 누적 index도 어긋난다.
- 기존 burst 함수는 trial 수를 20으로 고정하고, 저 SER에서도 최소 한 구간을 섞으며, iid와 동일한
  miss/false-alarm 수를 보장하지 않는다. 따라서 iid-versus-burst 비교로 해석할 수 없다.
- 일부 비선형 경로는 전체 데이터 평균·표준편차를 fold 전에 계산한다. 해당 결과는 누수가 없는
  재현 전까지 사용하지 않는다.

새 R0는 trial별 window 생성, 명시적 trial-ID 분리, trial별 예측 smoothing, 무 rescaling을 강제한다.
Transformer·MLP·LSTM·Kalman·SER는 R0가 닫힐 때까지 실행 범위에서 제외한다.

## 5. 재현

> ⚠️ **실데이터 full run은 아직 실행되지 않았다.** 코드와 합성 데이터 검증은 저장소에서 가능하지만,
> `MM_S1_processed.mat`는 별도로 준비해야 한다. R0의 성공 조건은 `0.8701`을 다시 만드는 것이 아니라
> 누수 없는 절차가 끝까지 실행되고 그 차이를 정직하게 기록하는 것이다.

- **실행 환경**: Google Colab 또는 로컬 Python. R0 Ridge는 CPU만 사용한다.
- **데이터**: CRCNS pmd-1의 `MM_S1_processed.mat`. CRCNS는 계정 신청이 필요하며
  이 저장소에 데이터는 포함되지 않는다. 스크립트는 Google Drive 경로
  `/content/drive/MyDrive/data_and_scripts/source_data/processed/MM_S1_processed.mat`를 가정한다.
- **R0 의존성**: [`reproduction/requirements.txt`](reproduction/requirements.txt)에 최소 패키지를 명시했다.
- **태블릿 진입점**: [`notebooks/R0_ridge_colab.ipynb`](notebooks/R0_ridge_colab.ipynb)을 위에서 아래로
  실행한다. smoke/full 결과는 휘발성 `/content`가 아니라 Google Drive에 저장한다.
- **레거시 코드 원본**: `github.com/youjhun05/A-Software-Validation-Using-Macaque-Motor-Cortex-Data-pmd-1-`.
  연구 근거는 이 저장소의 corrected R0 결과만 사용한다.

**R0를 완결하려면 남은 것**

1. 태블릿에서 데이터 접근 셀을 실행해 `R0_GATE=DATA_FOUND` 확인
2. 25-trial smoke run으로 파일 구조와 실행 경로 확인
3. 전체 5-fold 실행 후 `r0_summary.json`과 `r0_folds.csv`를 Drive에 보존
4. corrected 결과와 legacy `r=0.8701`의 차이를 PI용 보고서에 원인 미정 상태로 기록

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
