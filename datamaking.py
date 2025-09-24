import pandas as pd
import numpy as np
import os

# N: 자산 개수
# K: 견해 개수
# tau: 시장 불확실성 스칼라 (1*1)
# sigma: 초과수익률 공분산 행렬 (N*N)
# P: 자산 식별 견해 행렬 (K*N)
# omega: 견해 불확실성 공분산 행렬 (K*K)
# pi: 내재 시장 균형 초과수익률 벡터 (N*1)
# Q: 투자자 견해 초과수익률 벡텨 (K*1)
def open_file():
    folder_name = 'data'
    file_name = 'example.csv'
    file_path = os.path.join(folder_name, file_name)
    df = pd.read_csv(file_path)

    df['date'] = pd.to_datetime(df['date'])
    df['RET'] = pd.to_numeric(df['RET'], errors='coerce')

    print("CSV 파일을 성공적으로 불러왔습니다.")
    return df

df = open_file()

start_date = '2021-05-01'
end_date = '2024-04-30'
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()

pivot_df = filtered_df.pivot_table(index='date', columns='TICKER', values='RET')

sigma = pivot_df.cov()

# print(filtered_df)
# print(pivot_df)
print(sigma)