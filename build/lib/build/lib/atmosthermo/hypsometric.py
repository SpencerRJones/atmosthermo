import numpy as np


def hypsometric(T_v, p1, p2):

    '''
    Calculates thickness of an air layer [m] using the hypsometric equation.

    dz = (R_d*T_v)/g * ln(p1/p2)

    where p1 > p2

    Inputs:
        T_v       | Mean virtual temperature for layer
        p1        | Higher pressure boundary [Pa] or [hPa]
        p2        | Lower pressure boundary [Pa] or [hPa]

    Output:
        dz        | Depth of layer [m]
    '''

    R_d = 287.0 #[J kg^-1 K^-1]
    g   = 9.81  #[m s^-2]

    return R_d * T_v * (1./g) * np.log(p1/p2)
