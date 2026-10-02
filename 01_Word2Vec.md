# Word2Vec 논문 리뷰

## Word Embedding
- 기존 NLP의 기본 단위는 **one-hot / 단어 ID** — 단어 간 유사도가 전혀 없고(모든 쌍이 직교), 차원이 어휘 크기만큼 필요함.
- 대안: 단어를 **저차원 밀집 벡터(dense vector)** 로 표현. 분포 가설(distributional hypothesis) — "비슷한 문맥에 등장하는 단어는 비슷한 의미" — 에 기반.
- 이 논문의 핵심 문제의식은 "**더 좋은 모델**"이 아니라 "**같은 품질을 훨씬 싸게**". 기존 NNLM/RNNLM은 은닉층 때문에 연산량 O(N×D×H)가 지배적이라 대규모 코퍼스에 못 씀.

## Continuous Word Vectors
- 학습된 벡터 공간에는 **선형적인 규칙성(linear regularities)** 이 존재한다는 것이 핵심 발견.
- **벡터 산술**: `vec("King") − vec("Man") + vec("Woman") ≈ vec("Queen")`, `Paris − France + Italy ≈ Rome`.
- 한 단어가 **여러 종류의 유사도**를 동시에 가짐(예: big–bigger 관계와 big–large 관계가 서로 다른 축).

## Skip-gram and CBOW
두 구조 모두 **비선형 은닉층을 제거**하고, 출력층은 **hierarchical softmax(Huffman tree)** 로 계산량을 log₂(V)로 축소.

| | **CBOW (Continuous Bag-of-Words)** | **Skip-gram** |
|---|---|---|
| 방향 | **주변 단어들 → 중심 단어** 예측 | **중심 단어 → 주변 단어들** 예측 |
| 입력 처리 | 문맥 벡터들을 **평균/합**(순서 무시 = bag-of-words) | 중심 단어 하나 |
| 연산량 | Q = N×D + D×log₂V (저렴) | Q = C×(D + D×log₂V) (비쌈) |
| 속도 | **빠름** | 느림 |
| 강점 | **문법(syntactic)** 과제 우세, 빈출 단어에 유리 | **의미(semantic)** 과제 크게 우세, **희귀 단어**에 강함 |
| 윈도우 | 앞뒤 문맥 4단어 등 | 거리가 먼 단어는 낮은 확률로 샘플링(가까운 단어에 가중) |

- 정확도 비교(300차원, 1.6B Training Words): **CBOW** 의미 16.1 / 문법 52.6 / 전체 36.1%, **Skip-gram** 의미 52.2 / 문법 55.1 / 전체 53.8%.
- 학습 효율: DistBelief로 병렬화해 **1,000차원 벡터를 6B 단어 코퍼스에서** 학습. 기존 NNLM 대비 **수천 배 빠름며 성능은 더 우수**.
