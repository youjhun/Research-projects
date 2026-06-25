# Extracellular Recording & Spike Sorting

> 전극 신호에서 spike를 분리하는 과정. 하위 노드: [[01 - Spike Train & Neural Coding]]

## 신호 계층

- **LFP** (1~300 Hz): 집단 synaptic activity.
- **MUA** (300~3000 Hz): 근처 뉴런들의 spike 합.
- **SUA** (single-unit): spike sorting으로 분리된 단일 뉴런.
  - 정밀도 높지만 stability 낮음.

## Spike 검출

- MAD threshold: `σ_n = median|x| / 0.6745`.
  - std 대비 robust.
  - threshold = ±4σ.
- Dead time / refractory period:
  - ARP (절대 불응기): 완전 차단.
  - RRP (상대 불응기): stronger spike만 통과.

## Spike Sorting 방법

1. **Template matching**: 미리 구한 waveform template과 correlation.
2. **PCA + Clustering**: waveform을 PCA로 축소 → k-means / GMM.
3. **Watershed**: spike amplitude와 PC space를 density 기반으로 분할.
- ISI histogram 검증: Refractory period 위반 비율 < 1%.

## pmd-1 위치

- 이미 spike sorted 상태로 제공.
  - `Data.neural_data_M1`, `Data.neural_data_PMd`.
  - spike count matrix.
- 연결: `01 - Spike Train & Neural Coding`
