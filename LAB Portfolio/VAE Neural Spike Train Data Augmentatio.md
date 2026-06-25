# VAE 기반 Neural Spike Train 생성 및 Data Augmentation 효과 검증

## 실험 파이프라인

---

### Stage 0: 문제 정의

pmd-1은 496 trial. 실제 환자 세팅에서는 이것보다 훨씬 적은 50~100 trial로 decoder를 학습

**"실제 데이터가 100 trial밖에 없을 때, VAE로 생성한 가짜 데이터를 섞으면 MLP decoder 성능이 올라가는가?"**

→ data augmentation이 성공하면 임상 실용화 비용(교정 시간, 환자 피로) Reduce

---

### Stage 1: 데이터 준비 — Low-data regime 시뮬레이션

전체 496 trial 중에서 의도적으로 일부만 사용.

실험 조건을 세 가지로 나눠.

첫 번째 **Full data** 조건. 전체 496 trial 사용. 성능 상한선

두 번째 **Low-data** 조건. 100 trial만 사용. augmentation이 필요한 상황

세 번째 **Low-data + Augmented** 조건. 100 trial로 VAE를 학습하고, 생성 데이터를 추가해서 decoder를 학습.

이 세 조건의 MLP decoder 성능을 비교.

---

### Stage 2: VAE 설계 — 무엇을 생성할 것인가

VAE가 생성해야 하는 것은 **(spike_train, velocity) 쌍**. 

**입력 구조.**

하나의 데이터 샘플 →  (20 bins × 161 neurons)의 spike window, 그에 대응하는 (Vx, Vy) velocity. VAE : 위 두 가지를 동시에 latent space로 압축, 재복원.

VAE 구조 - Three pt.

**Encoder:**  spike window를 flatten해서 FC 레이어를 통해 latent vector z의 mean과 log-variance를 출력. z의 차원은 64 정도면 충분할 것임.

**Decoder:** z를 받아서 spike window와 velocity를 동시에 복원. spike는 Poisson 분포 기반이라 출력에 softplus를 쓰고, velocity는 Gaussian이라 linear output.

**Loss:**  세 항의 합. spike 복원 오차(MSE), velocity 복원 오차(MSE), KL divergence. velocity 복원 오차에는 가중치를 더 줘서 kinematic consistency를 강제.

---

### Stage 3: VAE 학습 및 생성 데이터 품질 검증

VAE를 학습하기 전에 먼저 **생성 데이터가 실제 데이터처럼 보이는지** 검증. 

검증 지표는 세 가지야.

**통계적 유사성**은 생성된 spike train의 sparsity와 평균 발화율이 실제 데이터(희소율 93.9%, 평균 6.4 Hz)와 얼마나 가까운가?

**Kinematic consistency**는 생성된 (spike, velocity) 쌍에서 velocity가 실제로 spike와 의미있게 연결되어 있는가? 생성 데이터만으로 Ridge decoder를 학습했을 때 r이 0.5 이상 나오면 quality가 충분.

**Latent space visualization**은 실제 데이터와 생성 데이터의 z를 UMAP으로 시각화. 두 분포가 겹치면 VAE가 실제 데이터 분포를 잘 학습한 것. 만약 완전히 분리돼 있으면 VAE가 mode collapse.

---

### Stage 4: Augmentation 실험

Low-data 조건(100 trial)에서 VAE로 생성한 데이터를 추가해서 MLP를 학습.

생성 데이터의 비율을 바꿔가면서 실험. 

- 실제 100 trial에 생성 100 trial을 추가(1:1)
- 실제 100 trial에 생성 300 trial 추가(1:3)
- 실제 100 trial에 생성 900 trial 추가(1:9)

Why change the ratio?

생성 데이터가 너무 많으면 오히려 실제 분포에서 벗어나서 성능이 떨어지는 **augmentation degradation** 현상. 이 현상이 나타나는 지점을 찾는 것 자체가 insight 가져가는 부분.

결과적으로 보고 싶은 그래프는 x축이 "생성 데이터 비율", y축이 "MLP r_neural"인 곡선. 최적 비율이 어딘가에서 peak를 형성할 것임.

---

### Stage 5: 결과 해석

**가능성 1: Augmentation이 효과가 있다**
Low-data + Augmented가 Low-data만 쓴 것보다 r이 통계적으로 유의미하게 높으면, "VAE 기반 augmentation이 data-scarce BCI 세팅에서 decoder 성능을 개선한다"는 positive result. 

**가능성 2: 효과가 제한적이다**
marginal improvement만 나오면, "생성 모델의 kinematic consistency가 충분하지 않아 augmentation 효과가 제한된다"는 분석. negative result가 아니라 "어떤 조건에서 작동하는지"에 대한 valuable finding.

**가능성 3: 오히려 성능이 떨어진다**
생성 데이터의 분포 왜곡이 decoder를 mislead하는 거야. "단순한 VAE augmentation은 BCI에서 충분하지 않고, conditional generation이 필요하다"는 결론으로 연결.

세 가능성 모두 narrative가 있어. 그래서 이 실험이 실패 리스크가 낮아.

---

### Stage 6: 확장

**Conditional VAE**는 velocity를 조건으로 줘서 "이런 움직임에 대응하는 spike train을 생성해줘"라고 명시적으로 요청하는 거야. 기본 VAE보다 kinematic consistency가 상승.

**SER-aware augmentation**은 VAE로 생성한 데이터에 SER을 적용해서 noisy한 조건에서도 augmentation이 효과가 있는지 확인. Project 2의 SER framework와 직접 연결되는 확장.