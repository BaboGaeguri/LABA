from .portfolio_opt.BL_opt import BL_optimization
from .portfolio_opt.MVO_opt import MVO_Optimizer

def portfolio_optimization(tau, gamma):
    tau = tau
    gamma = gamma
    BL = BL_optimization(tau)
    mvo = MVO_Optimizer(BL[0], BL[1], BL[2])
    w_delta_norm = mvo.optimize_utility_1(gamma)
    w_tan = mvo.optimize_tangency_1()
    return [w_delta_norm, w_tan, BL[2]]