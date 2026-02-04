import numpy as np


'''
These functions calculate variables using the ideal gas law.

p = rho*R_d*T

or p = rho*R_d*T_v if moisture is considered.
'''


def calculate_air_density(temp, pres, q=None):
    '''
    Calculates air density from temperature, pressure, and humidity
    using ideal gas law. If humidity is not provided, function
    returns dry air density. All input and output units are SI.

    Inputs:
        temp     | temperature [K]
        pres     | pressure [Pa]
        q        | specific humidity [kg/kg]

    Outputs:
        rho      | air density [kg m^-3]
    '''
    t = temp
    if q is not None:
        t *= 1. + 0.608*q

    R_d = 287.0 #J kg^-1 K^-1

    return pres / (R_d * t)
