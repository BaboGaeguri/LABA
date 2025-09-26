from BL_opt.BL_opt import BL_optimization
from MVO_opt import MVO_Optimizer

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
gamma = 0.1

BL = BL_optimization(tau)
mvo = MVO_Optimizer(BL[0], BL[1], BL[2])
w_delta_norm = mvo.optimize_utility_1(gamma)
w_tan = mvo.optimize_tangency_1()