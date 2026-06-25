# Bridge: Full-Data → Low-Data → Augmentation

> 연구의 핵심 문제 전이 흐름.
> 이 브릿지를 따라가면 전체 논문 스토리가 보임.

## 흐름 요약

1. `[[01 - Baseline Decoding]]` (Full data 496 trial)
   → "어떤 디코더가 기본으로 좋은가" 정리.
2. `[[02 - SER Robustness]]` + `[[03 - Attention Analysis]]`
   → 통신/하드웨어 노이즈에서 디코더가 왜 robust한가 설명.
3. `[[04 - Low-Data Augmentation Quality Gate]]`
   → 100 trial만 쓸 때, 생성 spike의 품질 기준 설정.
4. `[[07 - Augmented Decoding]]`
   → 생성 spike 비율에 따른 decoder 성능 곡선.
5. `[[08 - VAE Architecture]]` + `[[06 - Physics Regularization]]`
   → Conditional VAE + physics regularization으로 다음 논문 주제.

## 연결 축 2개

- **SER → Augmentation**:
  - SER가 높을수록 저데이터 damage가 큼.
  - "그래서 augmentation이 필요한데, 어느 비율까지가 효과적인가?"로 연결.
- **VAE Quality → SER transfer**:
  - 생성 spike에 SER noise도 같이 주입하면,
  - SER=1e-2 조건에서 decoder가 더 robust해지는가?
  - Data augmentation과 noise robustness의 trade-off 해소 여부 검증.
