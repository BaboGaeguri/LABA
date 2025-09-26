import numpy as np
import pandas as pd
from IPython.display import display

np.set_printoptions(precision=6, suppress=True)

# 자산 3개, 뷰 2개
n, k = 3, 2

# 자산간의 공분산 행렬
Sigma = np.array([
    [0.0400, 0.0120, 0.0060],
    [0.0120, 0.0225, 0.0090],
    [0.0060, 0.0090, 0.0160]
])

# 시가총액 비중으로 가중한 벡터
w_mkt = np.array([[0.55],
                  [0.30],
                  [0.15]])

# 델타는 위험을 얼마나 회피하는가, 타우는 시장을 얼마나 못믿는가 --> 크면 뷰가 크게 반영
delta = 2.8
# 위험회피계수 λ는 시장 위험프리미엄 ÷ 시장 초과수익률 분산으로 구함
tau   = 0.05

# 피킹행렬
P = np.array([
    [ 1, -1,  0],
    [ 0,  0,  1]
])

# 각 뷰의 수익률
Q = np.array([[0.02],
              [0.03]])

Omega_base = P @ (tau * Sigma) @ P.T
Omega = np.diag(np.diag(Omega_base)) * 1.0

# 얘가 파이(시장암묵 기대수익)
pi = delta * Sigma @ w_mkt  # n x 1 행렬


# @ = 행렬곱, np.linalg.inv = 역행렬, 오메가는 뷰의 공분산(불확실성)
tauSigma_inv = np.linalg.inv(tau * Sigma)
Omega_inv = np.linalg.inv(Omega)

M = tauSigma_inv + P.T @ Omega_inv @ P
M_inv = np.linalg.inv(M)

mu_BL = M_inv @ (tauSigma_inv @ pi + P.T @ Omega_inv @ Q)  # (n x 1)

Sigma_mu_BL = M_inv

# ---------- 3) Portfolio weights from μ_BL (illustrative) ----------
Sigma_inv = np.linalg.inv(Sigma)
w_dir = Sigma_inv @ mu_BL
w_tan = w_dir / np.sum(w_dir)

w_delta = (1.0 / delta) * w_dir
w_delta_norm = w_delta / np.sum(w_delta)

# ---------- 4) Package results as tables ----------
assets = [f"Asset {i}" for i in range(1, n+1)]
views  = [f"View {i}"  for i in range(1, k+1)]

df_inputs = pd.DataFrame({
    "w_mkt": w_mkt.flatten(),
}, index=assets)

df_Sigma = pd.DataFrame(Sigma, index=assets, columns=assets)

df_params = pd.DataFrame({
    "delta":[delta],
    "tau":[tau]
})

df_views = pd.DataFrame(P, index=views, columns=assets)
df_Q     = pd.DataFrame(Q, index=views, columns=["Q"])
df_Omega = pd.DataFrame(Omega, index=views, columns=views)

df_pi    = pd.DataFrame(pi, index=assets, columns=["pi (implied ER)"])
df_muBL  = pd.DataFrame(mu_BL, index=assets, columns=["mu_BL (posterior ER)"])
df_SmuBL = pd.DataFrame(Sigma_mu_BL, index=assets, columns=assets)

df_weights = pd.DataFrame({
    "Market w": w_mkt.flatten(),
    "BL (tan, sum=1)": w_tan.flatten(),
    "BL (1/δΣ⁻¹μ, sum=1)": w_delta_norm.flatten()
}, index=assets)

# ---------- 5) Display ----------
print("00_Inputs_w_mkt")
display(df_inputs.round(6))
print("01_Sigma")
display(df_Sigma.round(6))
print("02_Params")
display(df_params.round(6))
print("03_P (Picking Matrix)")
display(df_views.round(6))
print("04_Q (Views)")
display(df_Q.round(6))
print("05_Omega (View Uncertainty)")
display(df_Omega.round(6))
print("06_pi (Implied Equilibrium ER)")
display(df_pi.round(6))
print("07_mu_BL (Posterior ER)")
display(df_muBL.round(6))
print("08_Sigma_mu_BL (Posterior Cov of μ)")
display(df_SmuBL.round(6))
print("09_Weights_Comparison")
display(df_weights.round(6))

Sigma, w_mkt, delta, tau, P, Q, Omega, pi, mu_BL, Sigma_mu_BL, w_tan, w_delta_norm