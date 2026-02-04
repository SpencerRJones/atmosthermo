import numpy as np

def clausius_clapeyron(T, species='water'):

    '''
    Calculates saturation vapor pressure using Clausius Clapeyron with
    normal assumptions.

    Inputs:
        T | temperature [K]
        species | "water" or "ice": species for which e_s is calculated
    Outputs:
        e_s | saturation vapor pressure
    '''

    e_s0 = 611. #[Pa]
    L_v = 2.5e6 #[J kg^-1]
    R_v = 461.5 #[J kg^-1 K^-1]
    T_0 = 273.  #[K]

    e_s = e_s0 * np.exp((L_v/R_v)*(1./T_0 - 1./T))

    return e_s

