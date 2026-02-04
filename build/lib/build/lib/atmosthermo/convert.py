import numpy as np

def SpecificMass2SpecificContent(c, p, t, q=None):
    
    '''
    Calculates kg/m^3 of an atmospheric parameter from
    the specific mass kg/kg. e.g. useful for converting 
    from ECMWF cloud water specific mass (kg/kg) to 
    cloud water content (kg/m^3). All units in SI.

    Equations from G.W. Petty: A First Course in Atmos-
    pheric Thermodynamics, pp. 71-74

    Inputs:
        c     - specific mass (kg/kg)
        p     - pressure (Pa)
        t     - temperature (K)
        

    Outputs:
        x     - specific content (kg/m^3)
    '''
    
    R_d = 287.0 #J kg^-1 K^-1

    #Calculate total air density:
    if q is not None:
        t *= (1. + (0.61 * (q / (1.-q))))
        
    rho = p / (R_d * t)
    
    x = c * rho

    return x


#############################################################################



def SpecificHumidity2MixingRatio(q):

    '''
    Calculates mixing ratio [kg/kg] of water vapor to dry air.

    Inputs:
        q    | Specific Humidity [kg/kg], or ratio of mass of
                water vapor to mass of moist air mixture.
    Outputs:
        w    | Mixing ratio [kg/kg] of mass of water vapor to
               mass of dry air.
    
    Note: Since they occupy the same volume, this is also the
          ratio of densities.
    '''

    return q / (1. - q)


def MixingRatio2SpecificHumidity(w):
    
    '''
    Calculates specific humidity [kg/kg], or ratio of mass of water 
    vapor to mass of moist air mixture.

    Inputs:
        w    | Mixing ratio [kg/kg]
    Outputs:
        q    | Specific humidity [kg/kg]
    '''

    return w / (1. + w)

#############################################################################

def VaporDensity2MixingRatio(rho, temp, pres):
    '''
    Calculates mixing ratio (kg/kg) from vapor density (kg/m^3)

    Inputs:
        rho     | vapor density [kg/m^3]
        temp    | temperature [K]
        pres    | air pressure [Pa]

    Outputs:
        w       | mixing ratio [kg/kg]

    '''

    R_d = 287.0 #[J kg^-1 K^-1]

    rho_d = pres /(temp * R_d) #[kg/m^3]

    w = rho / rho_d   #[g/kg]

    return w


###########################################################################

def VaporDensity2SpecificHumidity(rho, temp, pres):
    
    '''
    Calculates specific humidity (q) from vapor density (rho).
    All units are SI.

    Inputs:
        rho     | vapor density [kg/m^3]
        temp    | temperature [K]
        pres    | pressure [Pa]
    Outputs:
        q       | specific humidity [kg/kg]
    '''

    R_d = 287.0 #[J kg^-1 K^-1]
    R_v = 461.5 #[J kg^-1 K^-1]
    eps = R_d/R_v

    e = rho * R_v * temp

    rho_a = (pres - e)/(R_d * temp) + (e / (R_v * temp))

    return rho / rho_a

###########################################################################

def VaporPressure2SpecificHumidity(e, p):
    '''
    Calculates specific humidity [kg/kg] from vapor pressure and
    air pressure.
    
    Inputs:
        e   | vapor pressure [Pa] (Partial pressure of water vapor)
        p   | air pressure [Pa] (pressure of moist air)
    Outputs:
        q   | specific humidity [kg/kg]
    '''

    epsilon = 0.622

    q = epsilon*e/p
    
    return q

###########################################################################

def PotentialTemperature2Temperature(theta, p):

    '''
    Converts from potential temperature (theta) to temperature
    given theta [K] and pressure [Pa].

    T = theta * (p/p_0)^(R_d/c_p)

    Assumes p_0 = 1.0e+05 Pa (1000 hPa)
    '''

    R_d   = 287.047  #J kg^-1 K^-1
    c_p   = 1005.    #J kg^-1 K^-1
    p_0   = 1e5      #hPa
    kappa = R_d / c_p

    T = theta * (p / p_0)**kappa
    
    return T
    

###########################################################################

def Temperature2PotentialTemperature(T, p):

    '''
    Converts from temperature to potential temperature (theta),
    given temperature [K] and pressure [Pa].

    theta = T * (p_0/p)^(R_d/c_p)

    Assumes p_0 = 1.0e+05 Pa (1000 hPa)
    '''

    R_d   = 287.047  #J kg^-1 K^-1
    c_p   = 1005.    #J kg^-1 K^-1
    p_0   = 1e5      #hPa
    kappa = R_d / c_p

    theta = T * (p_0 / p)**(kappa)

    return theta

###########################################################################



def Temperature2VirtualTemperature(T, q):

    '''
    Calculates virtual temperature from temperature and humidity

    Inputs:
        T | temperature [K]
        q | specific humidity [kg kg^-1]
    Outputs:
        T_v | virtual temperature
    '''

    T_v = T * (0.608*q + 1)
    
    return T_v

########################################################################
