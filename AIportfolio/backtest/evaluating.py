import numpy as np
import pandas as pd
from scipy import stats

class PortfolioPerformance:    
    def __init__(self, risk_free_rate=0.0):

        self.risk_free_rate = risk_free_rate
        self.monthly_returns = []
        self.portfolio_values = []
        
    def calculate_monthly_return(self, weights, returns):

        weights = np.array(weights)
        returns = np.array(returns)
        return np.sum(weights * returns)
    
    def backtest(self, weights_list, returns_df, initial_capital=10000000):
        
        returns_df = returns_df.pivot_table(
            index='date', columns='SECTOR', values='RET_SEC'
        )

        print(returns_df)

        self.monthly_returns = []
        self.portfolio_values = [initial_capital]
        
        results = []
        
        for i, weights in enumerate(weights_list):
            # 변환된 데이터프레임에서 수익률 추출
            monthly_return_data = returns_df.iloc[i]
            
            # 포트폴리오 수익률 계산 (기존 로직과 동일)
            portfolio_return = self.calculate_monthly_return(weights, monthly_return_data)
            
            self.monthly_returns.append(portfolio_return)
            
            new_value = self.portfolio_values[-1] * (1 + portfolio_return)
            self.portfolio_values.append(new_value)
            
            results.append({
                'period': monthly_return_data.name, # 인덱스 (날짜) 사용
                'portfolio_return': portfolio_return,
                'portfolio_value': new_value,
                'cumulative_return': (new_value / initial_capital) - 1
            })
        
        return pd.DataFrame(results)
    
    def calculate_sharpe_ratio(self, returns=None):

        if returns is None:
            returns = np.array(self.monthly_returns)
        else:
            returns = np.array(returns)
        
        # 월간 무위험 수익률
        monthly_rf = (1 + self.risk_free_rate) ** (1/12) - 1
        
        excess_returns = returns - monthly_rf
        
        if len(excess_returns) == 0 or np.std(excess_returns) == 0:
            return 0.0
        
        # 샤프 비율 (연율화: sqrt(12))
        sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(12)
        return sharpe
    
    def calculate_cagr(self, n_periods=None):

        if n_periods is None:
            n_periods = len(self.monthly_returns)
        
        if n_periods == 0:
            return 0.0
        
        initial_value = self.portfolio_values[0]
        final_value = self.portfolio_values[n_periods]
        
        # 월 단위를 연 단위로 변환
        years = n_periods / 12
        cagr = (final_value / initial_value) ** (1 / years) - 1
        return cagr
    
    def calculate_mdd(self, returns=None):

        if returns is None:
            values = np.array(self.portfolio_values)
        else:
            # 수익률로부터 누적 가치 계산
            values = np.cumprod(1 + np.array(returns))
            values = np.insert(values, 0, 1.0)
        
        # 각 시점까지의 최대값 계산
        cummax = np.maximum.accumulate(values)
        
        # Drawdown 계산
        drawdown = (values - cummax) / cummax
        
        # MDD는 가장 큰 낙폭
        mdd = np.min(drawdown)
        return mdd
    
    def calculate_var_cvar(self, returns=None, confidence_level=0.95):

        if returns is None:
            returns = np.array(self.monthly_returns)
        else:
            returns = np.array(returns)
        
        # VaR: 하위 (1-confidence_level) 백분위수
        var = np.percentile(returns, (1 - confidence_level) * 100)
        
        # CVaR: VaR 이하 수익률의 평균
        cvar = returns[returns <= var].mean()
        
        return var, cvar
    
    def calculate_all_metrics(self):

        sharpe = self.calculate_sharpe_ratio()
        cagr = self.calculate_cagr()
        mdd = self.calculate_mdd()
        var, cvar = self.calculate_var_cvar()
        
        return {
            'Sharpe Ratio': sharpe,
            'CAGR': cagr,
            'MDD': mdd,
            'VaR (95%)': var,
            'CVaR (95%)': cvar,
            'Total Return': self.portfolio_values[-1] / self.portfolio_values[0] - 1,
            'Volatility (Annual)': np.std(self.monthly_returns) * np.sqrt(12)
        }
    
    def compare_with_benchmark(self, benchmark_returns):

        # 벤치마크 성과 계산
        benchmark_perf = PortfolioPerformance(self.risk_free_rate)
        benchmark_perf.monthly_returns = list(benchmark_returns)
        benchmark_perf.portfolio_values = [self.portfolio_values[0]]
        
        for ret in benchmark_returns:
            new_val = benchmark_perf.portfolio_values[-1] * (1 + ret)
            benchmark_perf.portfolio_values.append(new_val)
        
        # 각각의 지표 계산
        portfolio_metrics = self.calculate_all_metrics()
        benchmark_metrics = benchmark_perf.calculate_all_metrics()
        
        # 비교 DataFrame 생성
        comparison = pd.DataFrame({
            'Portfolio': portfolio_metrics,
            'Benchmark': benchmark_metrics,
            'Difference': {k: portfolio_metrics[k] - benchmark_metrics[k] 
                          for k in portfolio_metrics.keys()}
        })
        
        return comparison