from open_file import open_file

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

df = open_file()

start_date = '2021-05-01'
end_date = '2024-04-30'

# Sigma: 초과수익률 공분산 행렬 (N*N)
def making_sigma():
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    pivot_filtered_df = filtered_df.pivot_table(index='date', columns='TICKER', values='RET')
    sigma = pivot_filtered_df.cov()
    return sigma

# Pi: 내재 시장 균형 초과수익률 벡터 (N*1)
def making_w_mkt():
    mkt_cap = df[df['date'] == end_date]['MKT'].values.reshape(-1, 1)
    total_mkt_cap = np.sum(mkt_cap)
    w_mkt = mkt_cap / total_mkt_cap
    return w_mkt

def making_delta():
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    ret_mean = filtered_df['RET'].mean()
    ret_variance = filtered_df['RET'].var()
    delta = ret_mean / ret_variance
    return delta

def making_Pi():
    w_mkt = making_w_mkt()
    delta = making_delta()
    sigma = making_sigma()
    pi = delta * sigma @ w_mkt
    return pi
Pi = making_Pi()
print(Pi)


# mu_BL = M_inv @ (tauSigma_inv @ pi + P.T @ Omega_inv @ Q)
# BL_returns = np.linalg.inv(TauSigma_inv + P.T @ Omega_inv @ P) @ (TauSigma_inv @ Pi + P.T @ Omega_inv @ Q)

'''
Tau = 0.025
Sigma = making_sigma()

P
Omega
Q

Pi = delta * Sigma @ w_mkt

TauSigma_inv = np.linalg.inv(Tau*Sigma)
'''