from BL_opt.BL_opt import BL_optimization
from MVO_opt_불완전 import MVOOptimizer

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

# tau: 시장 불확실성 스칼라 (1*1)
tau = 0.025

BL_returns = BL_optimization(tau)
print("BL Returns:\n", BL_returns)