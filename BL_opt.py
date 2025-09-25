from view_불완전 import BlackLittermanMatrixGenerator
from BL_equation import BL_Parameters

import numpy as np

def BL_optimization(tau):
    bl_generator = BlackLittermanMatrixGenerator()
    my_matrices = bl_generator.generate_all_matrices(k_views=5)
    bl_generator.display_matrices(my_matrices)
    P = my_matrices['P']
    Q = my_matrices['Q']
    omega = my_matrices['Omega']

    BL_parameters = BL_Parameters()
    pi = BL_parameters.making_pi()
    sigma = BL_parameters.making_sigma()
    tau=tau
    tausigma_inv = np.linalg.inv(tau * sigma)
    omega_inv = np.linalg.inv(omega)

    BL_returns = np.linalg.inv(tausigma_inv + P.T @ omega_inv @ P) @ (tausigma_inv @ pi + P.T @ omega_inv @ Q)
    return BL_returns