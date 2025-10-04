import os
import pandas as pd

folder_name = 'database'
file_name = '무위험 수익률(미국채3개월).csv'
file_path = os.path.join(folder_name, file_name)

df = pd.read_csv(file_path)

df['observation_date'] = pd.to_datetime(df['observation_date'])
df.set_index('observation_date', inplace=True)

# 결측치 제거
print(df.isna().sum())
df.dropna(inplace=True)

# 일별 수익률 계산(% 단위 제거 -> 연율화된 수익률을 일별 수익률로 변환)
df['daily_return'] = (df['DTB3'] / 100) / 360

# 월별 수익률 계산(복리 계산)
monthly_returns = df.groupby(pd.Grouper(freq='M'))['daily_return'].apply(
    lambda x: (1 + x).prod() - 1
)

# csv로 변환할 준비와 변환
monthly_returns = monthly_returns.reset_index()
monthly_returns.rename(columns={'observation_date': 'date', 'daily_return': 'rf'}, inplace=True)
monthly_returns.to_csv('database/rf.csv', index=False)

print(monthly_returns)