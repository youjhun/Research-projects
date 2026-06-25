# Attention-based Neural Decoder: Transformer vs. LSTM on pmd-1

[Attention_based_Neural_Decoder__Transformer_vs__LSTM_on_pmd_1.pdf](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/Attention_based_Neural_Decoder__Transformer_vs__LSTM_on_pmd_1.pdf)

[Google Colab](https://colab.research.google.com/drive/1iO2hursZqIZC4BjthlO6qEKjIb-om4Wb?hl=ko)

```python

============================================================
PHASE 2: Trial-level CV Baseline (SER=0)
============================================================

── Fold 1/5 ──
  Ridge         rx=0.8629  ry=0.8680  SB_raw=0.819/0.801  SB_res=1.000/1.000
  MLP           rx=0.9194  ry=0.9216  SB_raw=0.870/0.872  SB_res=1.000/1.000
  LSTM          rx=0.8920  ry=0.8986  SB_raw=0.833/0.894  SB_res=1.000/1.000
  Transformer   rx=0.9053  ry=0.9092  SB_raw=0.791/0.826  SB_res=1.000/1.000

── Fold 2/5 ──
  Ridge         rx=0.8646  ry=0.8623  SB_raw=0.837/0.865  SB_res=1.000/1.000
  MLP           rx=0.9189  ry=0.9099  SB_raw=0.857/0.873  SB_res=1.000/1.000
  LSTM          rx=0.8909  ry=0.8966  SB_raw=0.801/0.852  SB_res=1.000/1.000
  Transformer   rx=0.9067  ry=0.9022  SB_raw=0.792/0.808  SB_res=1.000/1.000

── Fold 3/5 ──
  Ridge         rx=0.8750  ry=0.8740  SB_raw=0.853/0.844  SB_res=1.000/1.000
  MLP           rx=0.9225  ry=0.9185  SB_raw=0.899/0.881  SB_res=1.000/1.000
  LSTM          rx=0.8935  ry=0.9000  SB_raw=0.879/0.858  SB_res=1.000/1.000
  Transformer   rx=0.9131  ry=0.9106  SB_raw=0.839/0.820  SB_res=1.000/1.000

── Fold 4/5 ──
  Ridge         rx=0.8887  ry=0.8748  SB_raw=0.850/0.922  SB_res=1.000/1.000
  MLP           rx=0.9324  ry=0.9243  SB_raw=0.869/0.885  SB_res=1.000/1.000
  LSTM          rx=0.9086  ry=0.8891  SB_raw=0.817/0.876  SB_res=1.000/1.000
  Transformer   rx=0.9230  ry=0.9157  SB_raw=0.797/0.853  SB_res=1.000/1.000

── Fold 5/5 ──
  Ridge         rx=0.8683  ry=0.8618  SB_raw=0.921/0.885  SB_res=1.000/1.000
  MLP           rx=0.9263  ry=0.9154  SB_raw=0.905/0.917  SB_res=1.000/1.000
  LSTM          rx=0.8943  ry=0.8815  SB_raw=0.880/0.898  SB_res=1.000/1.000
  Transformer   rx=0.9115  ry=0.8999  SB_raw=0.846/0.840  SB_res=1.000/1.000

=== Phase 2 요약 ===
Decoder       r_neural    vs SNN     VAF   SB_raw(x)   SB_res(x)
  Ridge           0.8701   -0.0623   0.740       0.856       1.000
  MLP             0.9209   -0.0115   0.842       0.880       1.000
  LSTM            0.8945   -0.0379   0.789       0.842       1.000
  Transformer     0.9097   -0.0227   0.819       0.813       1.000
  Paper SNN       0.9324

============================================================
PHASE 3: SER Robustness Sweep
============================================================

[Noise Averaging Analysis]
  N neurons:            161
  Active per bin (avg): 9.8
  → SER=0.01 → ~0.10 corrupted channels/bin
  → noise dilution ≈ 1/10

Phase 2 모델 재훈련 (fold별 저장)...
  Fold 1  Ridge        trained.
  Fold 1  MLP          trained.
  Fold 1  LSTM         trained.
  Fold 1  Transformer  trained.
  Fold 2  Ridge        trained.
  Fold 2  MLP          trained.
  Fold 2  LSTM         trained.
  Fold 2  Transformer  trained.
  Fold 3  Ridge        trained.
  Fold 3  MLP          trained.
  Fold 3  LSTM         trained.
  Fold 3  Transformer  trained.
  Fold 4  Ridge        trained.
  Fold 4  MLP          trained.
  Fold 4  LSTM         trained.
  Fold 4  Transformer  trained.
  Fold 5  Ridge        trained.
  Fold 5  MLP          trained.
  Fold 5  LSTM         trained.
  Fold 5  Transformer  trained.

── SER=1e-04 ──
  Ridge         rep=1  r=0.8701
  MLP           rep=1  r=0.9209
  LSTM          rep=1  r=0.8937
  Transformer   rep=1  r=0.9069
  Ridge         rep=2  r=0.8701
  MLP           rep=2  r=0.9209
  LSTM          rep=2  r=0.8937
  Transformer   rep=2  r=0.9069
  Ridge         rep=3  r=0.8700
  MLP           rep=3  r=0.9209
  LSTM          rep=3  r=0.8936
  Transformer   rep=3  r=0.9069

── SER=3e-04 ──
  Ridge         rep=1  r=0.8700
  MLP           rep=1  r=0.9209
  LSTM          rep=1  r=0.8935
  Transformer   rep=1  r=0.9069
  Ridge         rep=2  r=0.8700
  MLP           rep=2  r=0.9210
  LSTM          rep=2  r=0.8936
  Transformer   rep=2  r=0.9069
  Ridge         rep=3  r=0.8701
  MLP           rep=3  r=0.9209
  LSTM          rep=3  r=0.8936
  Transformer   rep=3  r=0.9069

── SER=1e-03 ──
  Ridge         rep=1  r=0.8699
  MLP           rep=1  r=0.9207
  LSTM          rep=1  r=0.8933
  Transformer   rep=1  r=0.9068
  Ridge         rep=2  r=0.8699
  MLP           rep=2  r=0.9208
  LSTM          rep=2  r=0.8936
  Transformer   rep=2  r=0.9068
  Ridge         rep=3  r=0.8698
  MLP           rep=3  r=0.9208
  LSTM          rep=3  r=0.8936
  Transformer   rep=3  r=0.9069

── SER=3e-03 ──
  Ridge         rep=1  r=0.8698
  MLP           rep=1  r=0.9207
  LSTM          rep=1  r=0.8934
  Transformer   rep=1  r=0.9068
  Ridge         rep=2  r=0.8697
  MLP           rep=2  r=0.9208
  LSTM          rep=2  r=0.8933
  Transformer   rep=2  r=0.9069
  Ridge         rep=3  r=0.8697
  MLP           rep=3  r=0.9207
  LSTM          rep=3  r=0.8934
  Transformer   rep=3  r=0.9067

── SER=1e-02 ──
  Ridge         rep=1  r=0.8688
  MLP           rep=1  r=0.9201
  LSTM          rep=1  r=0.8920
  Transformer   rep=1  r=0.9063
  Ridge         rep=2  r=0.8690
  MLP           rep=2  r=0.9199
  LSTM          rep=2  r=0.8925
  Transformer   rep=2  r=0.9061
  Ridge         rep=3  r=0.8690
  MLP           rep=3  r=0.9203
  LSTM          rep=3  r=0.8935
  Transformer   rep=3  r=0.9064

=== SER 성능 유지율 ===
       SER         Ridge           MLP          LSTM   Transformer  Paper
     0e+00        1.0000        1.0000        1.0000        1.0000      —
     1e-04        1.0000        1.0000        0.9991        0.9969  1.000
     3e-04        1.0000        1.0000        0.9990        0.9969      —
     1e-03        0.9998        0.9998        0.9989        0.9968  0.888
     3e-03        0.9996        0.9998        0.9987        0.9968      —
     1e-02        0.9987        0.9991        0.9979        0.9962  0.700

============================================================
PHASE 4: Transformer Attention Extraction (Fixed)
============================================================
  추출된 레이어 수: 3
  Attention at now (last index): L1=0.0670 | L2=0.0612 | L3=0.0702
  Attention peak lag: L1=0ms | L2=-20ms | L3=-10ms

============================================================
PHASE 5: 시각화
============================================================
Saved: fig1_baseline.png
Saved: fig2_ser_robustness.png
Saved: fig3_velocity_tracking.png
Saved: fig4_attention_heatmap.png
Saved: fig5_attention_profile_fixed.png  ← 버그 수정

==============================================================
최종 요약 (Trial-level CV 기준)
==============================================================

Decoder       r_neural    vs SNN     VAF    SER=1e-2 ρ
────────────────────────────────────────────────────────
  Ridge           0.8701   -0.0623   0.740        0.9987
  MLP             0.9209   -0.0115   0.842        0.9991
  LSTM            0.8945   -0.0379   0.789        0.9979
  Transformer     0.9097   -0.0227   0.819        0.9962
  Paper (SNN)     0.9324         —       —        ~0.700

핵심 발견:
  ① 모든 rate-coded 디코더가 SER=1e-2에서 ρ≥0.98 유지
  ② SNN(spike-timing)은 동일 SER에서 0.700으로 하락
  ③ 이유: Population averaging (N=161 neurons, 
      active/bin≈10) → 개별 spike error 희석
  ④ Transformer attention peak: 
      최근 과거 bin에 집중 (biologically plausible)

산출물:
  fig1_baseline.png
  fig2_ser_robustness.png
  fig3_velocity_tracking.png
  fig4_attention_heatmap.png
  fig5_attention_profile_fixed.png  ← attention 버그 수정
```

```python
============================================================
PHASE 1: 데이터 로딩 & 전처리
============================================================
총 reaches 수: 496
X shape:  (59742, 161)
Vx shape: (59742,)
희소율: 93.89% | 평균 발화율: 6.41 Hz

============================================================
PHASE 2: 기저 디코딩 성능 측정
============================================================
r_neural_x (mean, affine-rescaled): 0.8711
r_neural_y (mean, affine-rescaled): 0.8669
r_neural   (avg):                   0.8690
논문 기준 (SNN):                    0.9324

============================================================
PHASE 2.5: Neuron Subsampling Analysis (Population Averaging)
============================================================
  N= 40  rep=1  ratio=0.9984
  N= 40  rep=2  ratio=0.9974
  N=161  rep=1  ratio=0.9991
  N=161  rep=2  ratio=0.9984

=== Subsampling 결과 ===
   N neurons   ρ (ratio)       std
          40      0.9979    0.0005
         161      0.9987    0.0003

============================================================
PHASE 3: Extended SER Robustness Sweep
============================================================
  SER=0e+00  rep=1/1  r=0.8690
  SER=1e-04  rep=1/1  r=0.8691
  SER=1e-03  rep=1/1  r=0.8690
  SER=1e-02  rep=1/1  r=0.8682
  SER=5e-02  rep=1/1  r=0.8651
  SER=1e-01  rep=1/1  r=0.8586
  SER=2e-01  rep=1/1  r=0.8485

r_neural (SER=0, affine-rescaled): 0.8690

       SER         ρ       std
     0e+00    1.0000    0.0000
     1e-04    1.0000    0.0000
     1e-03    0.9999    0.0000
     1e-02    0.9991    0.0000
     5e-02    0.9955    0.0000
     1e-01    0.9880    0.0000
     2e-01    0.9764    0.0000

============================================================
PHASE 4: Noise Dilution Factor Analysis
============================================================
Total neurons N:          161
Mean active per bin:      9.8
Feature vector dim:       3220

SER=1e-04:
  Expected corrupted features/sample: 0.0 / 3220
  Noise fraction:                     0.001%
  Dilution factor (N/active):         16.4×

SER=1e-03:
  Expected corrupted features/sample: 0.2 / 3220
  Noise fraction:                     0.006%
  Dilution factor (N/active):         16.4×

SER=1e-02:
  Expected corrupted features/sample: 2.0 / 3220
  Noise fraction:                     0.061%
  Dilution factor (N/active):         16.4×

SER=1e-01:
  Expected corrupted features/sample: 19.7 / 3220
  Noise fraction:                     0.611%
  Dilution factor (N/active):         16.4×

============================================================
PHASE 5: 시각화
============================================================
Saved: fig1_baseline_improved.png
Saved: fig2_ser_extended.png
Saved: fig3_velocity_rescaled.png
Saved: fig4_dilution_table.png
```

## 개념 플로우

---

### 1. Trial-level CV

pmd-1 데이터는 496개 trial이 이어붙여진 구조. KFold를 bin 단위로 자르면 trial 도중에 경계 발생

EX) trial 37번의 앞부분이 train, 뒷부분이 test. 운동 궤적은 trial 내에서 연속적으로 correlate. train에서 본 것과 비슷한 패턴이 test에 반영되는 data leakage 발생 결과적으로 r이 실제보다 낙관적.

**HOW**

trial 단위로 fold 다시 나누기. trial 1~396번이 train이라면, trial 397~496번이 test. trial 경계 안에서는 bin들이 같은 fold에 묶여 있므로 NO leakage. 

---

### 2. Attention Visualization

**self-attention**

Transformer가 20개 시간 bin을 처리할 때, 각 bin은 "나는 다른 bin들과 얼마나 관계가 있냐"를 내적으로 계산. → attention weight

IF 값이 크면 저 시점의 spike 패턴이 예측에 중요.

**Causal mask**

실시간 BCI에서는 미래 데이터를 볼 수 없음. t=now 시점에서 예측할 때 t=now+1의 spike를 참조X causal mask는 상삼각 행렬로 미래 방향 attention을 0으로 막음. 

**시각화**

attention map은 (query 시점) × (key 시점)의 2D 행렬. 

마지막 행, 즉 "t=now가 어떤 과거 bin에 집중하는가"를 보면 motor cortex의 temporal integration 특성이 드러나게 설계하였음. 실제로 운동신경은 movement onset 100~200ms 전부터 준비 활동이 나타난다고 알려져 있으므로 Layer 1이 먼 과거에 집중하고 Layer 3이 최근에 집중한다면, 문헌과 일치하는 계층적 temporal processing의 증거가 될 것임.

---

### 3. CausalTransformerWithAttn 분리 설계

**두 클래스로 나누기**

PyTorch의 TransformerEncoderLayer는 기본적으로 학습 중 attention weight를 저장 X

attention weight를 뽑으려면 MultiheadAttention을 직접 호출하면서 need_weights=True를 줘야 함. → 매 학습 step마다 하면 메모리와 연산이 낭비

CausalTransformerDecoder는 학습 전용. need_weights=False로 빠르게 연산CausalTransformerWithAttn은 시각화 전용. 

forward_with_attn() 메서드만 따로 있고, 학습이 끝난 다음 inference 단계에서만 호출. 

**실제 흐름**

학습은 CausalTransformerDecoder로 80 epoch 돌린다 → 학습 완료 → 같은 가중치를 CausalTransformerWithAttn에 올린다 → 테스트 샘플 100개만 forward_with_attn()으로 통과 → attention map 추출 → 시각화. 

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%201.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%202.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%203.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%204.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%205.png)

# Ridge

### 개선 1: Extended SER Sweep (가장 중요)

python

`SER_VALUES = [0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 5e-2, 1e-1, 2e-1]`

지금 커브가 완전히 flat하게 보이는 건 SER=1e-2가 너무 작아서야. Rate-coded decoder들도 SER=0.1~0.2 근처에서는 분명히 무너져. Breakdown point가 어디냐는 게 사실 이 연구의 진짜 contribution이 될 수 있어. "SNN은 1e-2에서 무너지고, rate-coded는 어디서 무너지나?" 를 보여줘야 비교가 의미 있는 그림이 돼.

---

### 개선 2: Affine Rescaling을 Velocity Tracking에도 적용

지금 코드의 문제는 Phase 2에서 `SB_res=1.000`으로 affine rescaling이 작동하는 걸 측정은 했는데, 실제 velocity tracking figure(Image 3)에는 그 rescaling이 안 들어가 있어. 그래서 predicted가 22→12 cm/s로 amplitude가 죽어 보이는 거야.

개선된 코드에서는 각 fold 학습 시 train split으로 affine 파라미터 `(a, b)`를 fit하고, test 예측에 적용해:

python

`ax, bx = fit_affine_rescaler(vxp_train, vxtr)  # train에서 fit
vxp    = apply_affine(vxp_raw, ax, bx)          # test에 적용`

이게 올바른 방식이야. Train에서 bias 보정을 학습하고 test에 apply하는 거지, test에서 bias를 직접 측정해서 보정하면 data leakage가 생겨.

---

### 개선 3: Neuron Subsampling Analysis (새로 추가)

이게 가장 중요한 신규 contribution이야. "왜 flat한가?"에 대한 mechanistic answer를 그림으로 보여주는 거야.

뉴런 수를 N=20, 40, 80, 161로 서브샘플링하면서 SER=1e-2에서 retention ratio를 측정하면, N이 클수록 robust해지는 곡선이 나와. 이게 population averaging 효과를 direct하게 증명하는 거야.

수학적으로도 코드에 넣었어:

`N=161, active≈10 → dilution factor ≈ 16×
SER=1e-2에서 corrupted features = 200 (non-zero features 중)
Noise fraction = 200/3220 = 6.2% → Pearson r 변화 ≈ 0.2% 수준`

```
  1. Extended SER sweep [0, 1e-4, 1e-3, 1e-2, 5e-2, 1e-1, 2e-1]
     → rate-coded decoder breakdown point 탐색
  2. Affine rescaling → velocity tracking amplitude 보정
  3. Neuron subsampling [40, 161] × 2 reps
     → population averaging 메커니즘 시각화
```

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/fae31483-8c3d-4cfa-b74b-a7fe4fc0ceae.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%206.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%207.png)

![image.png](Attention-based%20Neural%20Decoder%20Transformer%20vs%20LSTM/image%208.png)