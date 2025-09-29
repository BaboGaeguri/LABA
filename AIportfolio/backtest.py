import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

class PortfolioPerformance:
    """포트폴리오 성과 분석 클래스"""
    
    def __init__(self, risk_free_rate=0.0):
        """
        Parameters:
        -----------
        risk_free_rate : float
            무위험 수익률 (연율 기준, 예: 0.03 = 3%)
        """
        self.risk_free_rate = risk_free_rate
        self.monthly_returns = []
        self.portfolio_values = []
        
    def calculate_monthly_return(self, weights, returns):
        """
        한 달간의 포트폴리오 수익률 계산
        
        Parameters:
        -----------
        weights : array-like
            자산별 비중 (합계 1.0)
        returns : array-like
            자산별 수익률
            
        Returns:
        --------
        float : 포트폴리오 수익률
        """
        weights = np.array(weights)
        returns = np.array(returns)
        return np.sum(weights * returns)
    
    def backtest(self, weights_list, returns_df, initial_capital=10000000):
        """
        전체 기간 백테스팅 수행
        
        Parameters:
        -----------
        weights_list : list of array-like
            각 리밸런싱 시점의 포트폴리오 비중
        returns_df : DataFrame
            자산별 수익률 데이터 (행: 날짜, 열: 자산)
        initial_capital : float
            초기 투자금액
            
        Returns:
        --------
        DataFrame : 월별 성과 데이터
        """
        self.monthly_returns = []
        self.portfolio_values = [initial_capital]
        
        results = []
        
        for i, weights in enumerate(weights_list):
            # 해당 월의 수익률 데이터 추출
            monthly_return_data = returns_df.iloc[i]
            
            # 포트폴리오 수익률 계산
            portfolio_return = self.calculate_monthly_return(weights, monthly_return_data)
            self.monthly_returns.append(portfolio_return)
            
            # 포트폴리오 가치 업데이트
            new_value = self.portfolio_values[-1] * (1 + portfolio_return)
            self.portfolio_values.append(new_value)
            
            results.append({
                'period': i + 1,
                'portfolio_return': portfolio_return,
                'portfolio_value': new_value,
                'cumulative_return': (new_value / initial_capital) - 1
            })
        
        return pd.DataFrame(results)
    
    def calculate_sharpe_ratio(self, returns=None):
        """
        샤프 비율 계산
        
        Parameters:
        -----------
        returns : array-like, optional
            수익률 시계열 (None이면 저장된 monthly_returns 사용)
            
        Returns:
        --------
        float : 샤프 비율 (연율화)
        """
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
        """
        연평균 복리 수익률(CAGR) 계산
        
        Parameters:
        -----------
        n_periods : int, optional
            기간 수 (월 단위, None이면 전체 기간)
            
        Returns:
        --------
        float : CAGR
        """
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
        """
        최대 낙폭(MDD) 계산
        
        Parameters:
        -----------
        returns : array-like, optional
            수익률 시계열 (None이면 저장된 portfolio_values 사용)
            
        Returns:
        --------
        float : MDD (음수 값)
        """
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
        """
        VaR(Value at Risk)와 CVaR(Conditional VaR) 계산
        
        Parameters:
        -----------
        returns : array-like, optional
            수익률 시계열 (None이면 저장된 monthly_returns 사용)
        confidence_level : float
            신뢰수준 (기본값: 0.95 = 95%)
            
        Returns:
        --------
        tuple : (VaR, CVaR)
        """
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
        """
        모든 성과 지표를 한 번에 계산
        
        Returns:
        --------
        dict : 성과 지표 딕셔너리
        """
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
        """
        벤치마크와 성과 비교
        
        Parameters:
        -----------
        benchmark_returns : array-like
            벤치마크 수익률 시계열
            
        Returns:
        --------
        DataFrame : 비교 결과
        """
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
    
    def plot_performance(self, benchmark_returns=None, figsize=(15, 10)):
        """
        성과 시각화
        
        Parameters:
        -----------
        benchmark_returns : array-like, optional
            벤치마크 수익률 (비교용)
        figsize : tuple
            그래프 크기
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Portfolio Performance Analysis', fontsize=16, fontweight='bold')
        
        # 1. 누적 수익률 그래프
        ax1 = axes[0, 0]
        periods = range(len(self.portfolio_values))
        portfolio_cum_returns = [(v / self.portfolio_values[0] - 1) * 100 
                                 for v in self.portfolio_values]
        
        ax1.plot(periods, portfolio_cum_returns, label='Portfolio', linewidth=2)
        
        if benchmark_returns is not None:
            benchmark_values = [self.portfolio_values[0]]
            for ret in benchmark_returns:
                benchmark_values.append(benchmark_values[-1] * (1 + ret))
            benchmark_cum_returns = [(v / benchmark_values[0] - 1) * 100 
                                     for v in benchmark_values]
            ax1.plot(periods, benchmark_cum_returns, label='Benchmark', 
                    linewidth=2, linestyle='--')
        
        ax1.set_title('Cumulative Returns')
        ax1.set_xlabel('Period')
        ax1.set_ylabel('Return (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 월별 수익률 바 차트
        ax2 = axes[0, 1]
        periods = range(1, len(self.monthly_returns) + 1)
        colors = ['green' if r > 0 else 'red' for r in self.monthly_returns]
        ax2.bar(periods, [r * 100 for r in self.monthly_returns], color=colors, alpha=0.6)
        ax2.set_title('Monthly Returns')
        ax2.set_xlabel('Period')
        ax2.set_ylabel('Return (%)')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(True, alpha=0.3)
        
        # 3. Drawdown 차트
        ax3 = axes[1, 0]
        values = np.array(self.portfolio_values)
        cummax = np.maximum.accumulate(values)
        drawdown = (values - cummax) / cummax * 100
        
        ax3.fill_between(range(len(drawdown)), drawdown, 0, color='red', alpha=0.3)
        ax3.plot(range(len(drawdown)), drawdown, color='red', linewidth=1)
        ax3.set_title(f'Drawdown (MDD: {self.calculate_mdd()*100:.2f}%)')
        ax3.set_xlabel('Period')
        ax3.set_ylabel('Drawdown (%)')
        ax3.grid(True, alpha=0.3)
        
        # 4. 수익률 분포 히스토그램
        ax4 = axes[1, 1]
        ax4.hist([r * 100 for r in self.monthly_returns], bins=20, 
                alpha=0.7, color='blue', edgecolor='black')
        ax4.axvline(x=np.mean(self.monthly_returns) * 100, color='red', 
                   linestyle='--', linewidth=2, label='Mean')
        ax4.set_title('Return Distribution')
        ax4.set_xlabel('Return (%)')
        ax4.set_ylabel('Frequency')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, benchmark_returns=None):
        """성과 요약 출력"""
        print("=" * 60)
        print("PORTFOLIO PERFORMANCE SUMMARY")
        print("=" * 60)
        
        metrics = self.calculate_all_metrics()
        
        print(f"\n{'Metric':<25} {'Value':>15}")
        print("-" * 60)
        print(f"{'Sharpe Ratio':<25} {metrics['Sharpe Ratio']:>15.4f}")
        print(f"{'CAGR':<25} {metrics['CAGR']*100:>14.2f}%")
        print(f"{'Total Return':<25} {metrics['Total Return']*100:>14.2f}%")
        print(f"{'Annual Volatility':<25} {metrics['Volatility (Annual)']*100:>14.2f}%")
        print(f"{'Maximum Drawdown':<25} {metrics['MDD']*100:>14.2f}%")
        print(f"{'VaR (95%)':<25} {metrics['VaR (95%)']*100:>14.2f}%")
        print(f"{'CVaR (95%)':<25} {metrics['CVaR (95%)']*100:>14.2f}%")
        
        if benchmark_returns is not None:
            print("\n" + "=" * 60)
            print("BENCHMARK COMPARISON")
            print("=" * 60)
            comparison = self.compare_with_benchmark(benchmark_returns)
            print(f"\n{comparison.to_string()}")
        
        print("\n" + "=" * 60)


# 사용 예시
if __name__ == "__main__":
    # 예시 데이터 생성
    np.random.seed(42)
    
    # 8개월간의 포트폴리오 비중 (예시)
    weights_list = [
        [0.3, 0.3, 0.2, 0.2],  # Month 1
        [0.25, 0.35, 0.2, 0.2],  # Month 2
        [0.3, 0.3, 0.25, 0.15],  # Month 3
        [0.35, 0.25, 0.2, 0.2],  # Month 4
        [0.3, 0.3, 0.2, 0.2],  # Month 5
        [0.25, 0.35, 0.15, 0.25],  # Month 6
        [0.3, 0.25, 0.25, 0.2],  # Month 7
        [0.35, 0.3, 0.15, 0.2],  # Month 8
    ]
    
    # 각 자산의 월별 수익률 (예시)
    returns_df = pd.DataFrame({
        'Asset1': [0.02, 0.03, -0.01, 0.04, 0.01, 0.02, -0.02, 0.03],
        'Asset2': [0.01, 0.02, 0.02, -0.01, 0.03, 0.01, 0.02, 0.01],
        'Asset3': [0.03, -0.01, 0.02, 0.02, 0.01, 0.03, 0.01, 0.02],
        'Asset4': [0.01, 0.01, 0.01, 0.03, 0.02, -0.01, 0.02, 0.01],
    })
    
    # 벤치마크 수익률 (예시: 시장 지수)
    benchmark_returns = [0.015, 0.02, 0.01, 0.02, 0.015, 0.01, 0.005, 0.02]
    
    # 백테스팅 수행
    perf = PortfolioPerformance(risk_free_rate=0.03)
    results_df = perf.backtest(weights_list, returns_df, initial_capital=10000000)
    
    print("\n월별 성과:")
    print(results_df.to_string())
    
    # 성과 지표 출력
    perf.print_summary(benchmark_returns)
    
    # 시각화
    perf.plot_performance(benchmark_returns)