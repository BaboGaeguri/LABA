import pandas as pd
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '예시데이터원본.csv')

try:
    df = pd.read_csv(file_path)
    print("CSV 파일이 성공적으로 불러와졌습니다!")
    print(df.head())

except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")

# example을 위해 9개 티커만 필터링
ticker_list = ['NVDA', 'MSFT', 'AAPL', 'GOOGL', 'AMZN', 'META', 'AVGO', 'TSLA', 'LLY']
filtered_df = df.loc[df['TICKER'].isin(ticker_list)].copy()
print(filtered_df.head())

# 각 종목에 GICS 섹터 정보 강제 병합(Financials, Real Estate는 제외)
gics_sectors = {
    'NVDA': 'Energy',
    'MSFT': 'Materials',
    'AAPL': 'Industrials',
    'GOOGL': 'Consumer Discretionary',
    'AMZN': 'Consumer Staples',
    'META': 'Communication Services',
    'AVGO': 'Information Technology',
    'TSLA': 'Utilities',
    'LLY': 'Health Care'
}
filtered_df['SECTOR'] = filtered_df['TICKER'].map(gics_sectors)

filtered_df.to_csv('data/example.csv', index=False)
