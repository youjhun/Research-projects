# Action Potential & Hodgkin-Huxley Model

> spike의 생물물리적 기원. 하위 노드: [[01 - Spike Train & Neural Coding]]

## 핵심

- 뉴런의 신호 전달 단위 = 활동 전위 (Action Potential, AP).
- 길이: ~1 ms.
- 진폭: ~100 mV.
- threshold: 약 -55 mV.

## HH 모델 구조

- `C_m * dV/dt = I_Na + I_K + I_L + I_pump`
- 각 currents:
  - `I_Na = g_Na * m^3 * h * (V - E_Na)` (탈분极化)
  - `I_K  = g_K  * n^4 * (V - E_K)` (재분극)
  - `I_L  = g_L * (V - E_L)` (누출)
- 게이트 변수 m, h, n는 voltage-dependent.

## Reversal potentials

- `E_Na ≈ +55 mV`
- `E_K  ≈ -90 mV`
- `E_Cl ≈ -65 mV`
- Nernst equation: `E = (RT/zF) ln([out]/[in])`

## 한계

- 공간적 확장 없음 (지금은 point neuron).
- 실험적 뉴런 diversity 반영 어려움.
- 연결: `01 - Spike Train & Neural Coding`
