# MVO opt

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Optional, Tuple, Dict
import warnings

class MVOOptimizer:
    def __init__(self, returns: np.ndarray, covariance_matrix: Optional[np.ndarray] = None):
        self.returns = returns
        self.n_assets = returns.shape[0]

        # 공분산 행렬 설정
        if covariance_matrix is None:
            self.cov_matrix = self._generate_covariance_matrix()

    def _generate_covariance_matrix(self) -> np.ndarray:
        cov_matrix = self.returns.cov()
        return cov_matrix.values

    # 최대 샤프비율    
    def maximize_sharpe_ratio(self, risk_free_rate: float = 0.02) -> Dict:

        def objective(weights):
            portfolio_return = np.dot(weights, self.returns)
            portfolio_variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
            return -sharpe_ratio  # 최대화를 위해 음수로 변환
        
        # 제약조건
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        
        # 경계조건 (롱온리)
        bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        # 초기값
        x0 = np.array([1/self.n_assets] * self.n_assets)
        
        # 최적화 수행
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        return {
            'success': True,
            'weights': weights,
            'return': ret,
            'volatility': vol,
            'sharpe_ratio': sharpe,
            'risk_free_rate': risk_free_rate
        }