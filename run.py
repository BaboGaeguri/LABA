import pandas as pd

from AIportfolio.optimization import portfolio_optimization

# 연구 기간
forecast_period = [
    "24-05-31",
    "24-06-30",
    "24-07-31",
    "24-08-31",
    "24-09-30",
    "24-10-31",
    "24-11-30",
    "24-12-31"
]

# tau: 시장 불확실성(pi 계산용)
tau = 0.025
# gamma: 위험회피계수(MVO 최적화용)
gamma = 0.1

results = []

# 각 예측기간에 따른 포트폴리오 최적화 수행
for i, period in enumerate(forecast_period):

    print(f"--- 시나리오: {period} ---")
    
    opt = portfolio_optimization(tau, gamma)
    
    scenario_result = {
        "period": period,
        "w_delta_norm": opt[0],
        "w_tan": opt[1],
        "SECTOR": opt[2]
    }
    results.append(scenario_result)

# 결과 출력
for res in results:
    print(f"기간: {res['period']}")
    print(f"Delta-Normal 포트폴리오 비중: {pd.Series(res['w_delta_norm'].flatten(), index=res['SECTOR']).to_string(float_format='{:,.4f}'.format)}")
    print(f"Tangency 포트폴리오 비중: {pd.Series(res['w_tan'].flatten(), index=res['SECTOR']).to_string(float_format='{:,.4f}'.format)}")
    print("-------------------------------")