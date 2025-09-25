# 데이터 가져오기

import pandas as pd
import os

def open_file():
    folder_name = 'data'
    file_name = 'example.csv'
    file_path = os.path.join(folder_name, file_name)
    df = pd.read_csv(file_path)

    df['date'] = pd.to_datetime(df['date'])
    df['RET'] = pd.to_numeric(df['RET'], errors='coerce')
    df['MKT'] = df['PRC'] * df['SHROUT'] * 1_000_000

    print("CSV 파일을 성공적으로 불러왔습니다.")
    return df

df = open_file()
print(df.head())