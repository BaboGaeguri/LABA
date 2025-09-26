from view_params import BlackLittermanMatrixGenerator
from market_params import Market_Params

import pandas as pd
import numpy as np

def BL_optimization(tau):
    # view_params
    bl_generator = BlackLittermanMatrixGenerator()
    my_matrices = bl_generator.generate_all_matrices(k_views=5)
    bl_generator.display_matrices(my_matrices)
    P = my_matrices['P']
    Q = my_matrices['Q']
    omega = my_matrices['Omega']

    # market_params
    BL_parameters = Market_Params()
    pi = BL_parameters.making_pi()
    sigma = BL_parameters.making_sigma()
    tau=tau

    # Black-Litterman 공식 적용
    tausigma_inv = np.linalg.inv(tau * sigma)
    omega_inv = np.linalg.inv(omega)

    BL_returns = np.linalg.inv(tausigma_inv + P.T @ omega_inv @ P) @ (tausigma_inv @ pi + P.T @ omega_inv @ Q)

    SECTOR = sigma.columns
    BL_returns_series = pd.Series(BL_returns.values.flatten(), index=SECTOR)

    return BL_returns_series