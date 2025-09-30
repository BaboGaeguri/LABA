import matplotlib.pyplot as plt
import seaborn as sns

class visualization:
    def __init__(self, portfolio_values, monthly_returns):
        self.portfolio_values = portfolio_values
        self.monthly_returns = monthly_returns

    def plot_performance(self, benchmark_returns=None, figsize=(15, 10)):

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