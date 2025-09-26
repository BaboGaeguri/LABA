from utils.open_file import open_file
from utils.preprocessing import preprocessing

import pandas as pd
import numpy as np
import os

# N: 자산 개수
# K: 견해 개수
# sigma: 초과수익률 공분산 행렬 (N*N)
# pi: 내재 시장 균형 초과수익률 벡터 (N*1)

class Market_Params:
    def __init__(self):
        self.df = preprocessing(open_file())
        self.start_date = '2021-05-01'
        self.end_date = '2024-04-30'

    # Sigma: 초과수익률 공분산 행렬 (N*N)
    @classmethod
    def making_sigma(self):
        filtered_df = self.df[(self.df['date'] >= self.start_date) & (self.df['date'] <= self.end_date)].copy()
        pivot_filtered_df = filtered_df.pivot_table(index='date', columns='SECTOR', values='RET_SEC')
        sigma = pivot_filtered_df.cov()
        return sigma

    # Pi: 내재 시장 균형 초과수익률 벡터 (N*1)
    def making_w_mkt(self):
        mkt_cap = self.df[self.df['date'] == self.end_date]['MKT_SEC'].values.reshape(-1, 1)
        total_mkt_cap = np.sum(mkt_cap)
        w_mkt = mkt_cap / total_mkt_cap
        return w_mkt
    
    def making_delta(self):
        filtered_df = self.df[(self.df['date'] >= self.start_date) & (self.df['date'] <= self.end_date)].copy()
        ret_mean = filtered_df['RET_SEC'].mean()
        ret_variance = filtered_df['RET_SEC'].var()
        delta = ret_mean / ret_variance
        return delta
    
    @classmethod
    def making_pi(self):
        w_mkt = self.making_w_mkt()
        delta = self.making_delta()
        sigma = self.making_sigma()
        pi = delta * sigma @ w_mkt
        return pi