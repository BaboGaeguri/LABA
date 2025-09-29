from .portfolio_opt.utils.open_file import open_file
from .portfolio_opt.utils.preprocessing import preprocessing

from AIportfolio.backtest.evaluating import PortfolioPerformance
from AIportfolio.backtest.visualization import visualization

def test(results):
    results = results

    # 'w_tan' 비중만 추출하여 리스트로 만들기
    weights_tan = [item['w_tan'].flatten() for item in results]
    print("최종 생성된 weights_list (w_tan):")
    for w in weights_tan:
        print(w)

    # 'w_delta_norm' 비중만 추출하여 리스트로 만들기
    weights_delta_norm = [item['w_delta_norm'].flatten() for item in results]
    print("\n최종 생성된 weights_list (w_delta_norm):")
    for w in weights_delta_norm:
        print(w)

    returns_df = preprocessing(open_file())

    # 백테스트 실행
    pp = PortfolioPerformance(risk_free_rate=0.00)
    backtest_results = pp.backtest(weights_list=weights_tan, returns_df=returns_df)

    print("\n백테스트 결과 (DataFrame):")
    print(backtest_results)

    print("\n포트폴리오 성과 지표:")
    metrics = pp.calculate_all_metrics()
    for key, value in metrics.items():
        print(f"{key:<20}: {value:.4f}")