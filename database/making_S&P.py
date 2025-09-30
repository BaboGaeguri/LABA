import os
import pandas as pd

folder_name = 'database'
file_name = 'S&P 500 Historical Components & Changes.csv'
file_path = os.path.join(folder_name, file_name)

df_sp500 = pd.read_csv(file_path)
print(df_sp500)

folder_name = 'database'
file_name = '예시데이터원본.csv'
file_path = os.path.join(folder_name, file_name)

df = pd.read_csv(file_path)
print(df)

# df['date'] = pd.to_datetime(df['date'])
# df['RET'] = pd.to_numeric(df['RET'], errors='coerce')
