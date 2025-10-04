from ..BL_opt import BL_optimization

'''
IT vs Financials → 금리 인하 기대 제한·커브 역전 유지: Financials 근소 우위.
⇒ “Financials가 IT 보다 3% 우위일 것이다.”
Discretionary vs Staples → 확장 약·금리 고점 인식: Staples 우위.
⇒ “Discretionary가 Staples 보다 2% 우위일 것이다.”
Healthcare vs Industrials → 경기 모멘텀 약: Healthcare 우위.
⇒ “Healthcare가 Industrials 보다 1% 우위일 것이다.”
Energy vs Industrials → 유가 상단권: 중립~약한 Energy 우위.
⇒ “Energy가 Industrials 보다 0.5% 우위일 것이다.”
Utilities vs Financials → 스트레스 낮음+금리부담: Financials 우위.
⇒ “Utilities가 Financials 보다 2% 우위일 것이다.”
'''

# P: 자산 식별 견해 행렬 (K*N)
# omega: 견해 불확실성 공분산 행렬 (K*K)
# Q: 투자자 견해 초과수익률 벡텨 (K*1)

a = BL_optimization(tau=0.05, start_date='2021-05-31', end_date='2024-04-30')
print(a)
