import numpy as np
import math


########################################################################

def marshall_palmer(D_min = 0.01, D_max = 10, npoints=100, scale = 'log',
                    D = None, lamb = None, R = None, rwc = None):

    '''
    Returns an array of n(D), the number of drops n at each diameter D using
    a Marshall-Palmer distribution: n(D) = 8000 * exp(-lambda*D)

    Inputs:
        D_min          | Minimum size of droplets [mm] (Default 10 um)
        D_max          | Maximum size of droplets [mm] (Default 10 mm)
        npoints        | Number of droplet diameters to calculate n for 
                         (Default 100)
        scale          | Whether D space is set up in log space or
                         linear space.
        D              | (Optional) User provides their own array of D
                          sizes in mm.
        lamb           | Slope parameter. If left to None, is calculated
                         from R or rwc.
        R              | Rain rate. If left to None, is not used.
        rwc            | Rain water content [g/m^3]. Used to constrain
                         lamb.

    Outputs:
        n              | Array of size D that gives the number concentration,
                         or number of drops per volume [m^-3 mm^-1]
    '''

    n0 = 8.0e06 #[m^-4]
    rho_l = 1000. #density of liquid water [kg m^-3]

    #Set up D array:
    if scale == 'log':
        diam = 10.**(np.linspace(np.log10(D_min), np.log10(D_max), npoints))
    elif scale == 'linear':
        diam = np.linspace(D_min, D_max, npoints)

    if D is not None:
        diam = D


    #Check for how to calculate lamb:
    if lamb is None:
        if rwc is not None:
            lamb = ((n0*np.pi*rho_l)/(rwc*0.001))**0.25 * 0.001 #[m^-4]*[kg m^-3]/[kg m^-3] --> #[mm^-1]
        elif R is not None:
            lamb = 4.1 * R**-0.21
        else:
            raise ValueError(f'Either lamb, R, or rwc has to be specified.')
        

    n = n0 * np.exp(-lamb * diam) * 0.001 #[mm^-1 m^-3]
    
    return n, diam

########################################################################


def inverse_exponential(n0, rho, D_min = 0.01, D_max = 10, npoints=100, scale = 'log',
                        D = None, lamb = None, q = None):

    '''
    Returns an array of n(D), the number of particles n at each diameter D using
    a general inverse exponential distribution: n(D) = n0 * exp(-lambda*D)

    Inputs:
        n0             | Inverse exponential intercept parameter [mm^-1 m^-3]
        rho            | Species density [kg m^-3] (Liquid water = 1000 kg m^-3)
        D_min          | Minimum size of particles [mm] (Default 10 um)
        D_max          | Maximum size of particles [mm] (Default 10 mm)
        npoints        | Number of particle diameters to calculate n for
                         (Default 100)
        scale          | Whether D space is set up in log space or
                         linear space.
        D              | (Optional) User provides their own array of D
                          sizes in mm.
        lamb           | Slope parameter. If left to None, is calculated
                         from q.
        q              | Specific water content [g/m^3]. Used to constrain
                         lamb.

    Outputs:
        n              | Array of size D that gives the number concentration,
                         or number of particles per volume [m^-3 mm^-1]
    '''

    n0 = n0 * 1000. #[mm^-1 m^-3] --> [m^-4]

    #Set up D array:
    if scale == 'log':
        diam = 10.**(np.linspace(np.log10(D_min), np.log10(D_max), npoints))
    elif scale == 'linear':
        diam = np.linspace(D_min, D_max, npoints)

    if D is not None:
        diam = D


    #Check for how to calculate lamb:
    if lamb is None:
        if q is not None:
            lamb = ((n0*np.pi*rho)/(q*0.001))**0.25 * 0.001 #[m^-4]*[kg m^-3]/[kg m^-3] --> #[mm^-1]
        else:
            raise ValueError(f'Either lamb or q has to be specified.')


    n = n0 * np.exp(-lamb * diam) * 0.001 #[mm^-1 m^-3]

    return n, diam

########################################################################


def gamma_distribution(n0, mu, D_min=0.01, D_max=10, npoints=100, scale='log',
                       D=None, lamb=None, lwc=None):

    '''
    Returns an array of n(D), the number of drops n at each diameter D using
    a gamma distribution: n(D) = n0 * D^mu * exp(-lambda*D)

    Inputs:
        n0             | Intercept parameter [mm^-(mu+1) m^-3]
        mu             | Shape parameter []
        D_min          | Minimum size of droplets [mm] (Default 10 um)
        D_max          | Maximum size of droplets [mm] (Default 10 mm)
        npoints        | Number of droplet diameters to calculate n for
                         (Default 100)
        scale          | Whether D space is set up in log space or
                         linear space.
        D              | (Optional) User provides their own array of D
                          sizes in mm.
        lamb           | Slope parameter. If left to None, is calculated
                         from rwc.
        lwc            | Liquid water content [g/m^3]. Used to constrain
                         lamb if not specified.

    Outputs:
        n              | Array of size D that gives the number concentration,
                         or number of drops per volume [m^-3 mm^-1]
    '''

    n0 = n0 * 1000.  #[mm^-(mu+1) m^-3] --> #[m^-(mu+4)]
    rho_l = 1000.    #Density of liquid water [kg/m^3]

    #Set up D array:
    if scale == 'log':
        diam = 10.**(np.linspace(np.log10(D_min), np.log10(D_max), npoints))
    elif scale == 'linear':
        diam = np.linspace(D_min, D_max, npoints)
    if D is not None:
        diam = D

    #Calculate lamb if not specified:
    if lamb is None:
        if lwc is not None:
            lamb = ((n0*rho_l*np.pi*math.gamma(mu+4))/(6.*lwc*0.001))**(1./(mu+4)) * 0.001
            #units: ([m^-(mu+4)]*[kg m^-3]*[]*[]/([]*[kg m^-3]))^(1/(mu+4))
            #       = [m^-(mu+4)]^(1/mu+4) = m^(-(mu+4)/(mu+4)) = [m^-1]
            #       m^-1 * 10^-3 = mm^-1
        else:
            raise ValueError(f'Either lamb or rwc has to be specified.')

    n = n0 * (diam*0.001)**mu * np.exp(-lamb * diam) * 0.001
    #units: [m^-(mu+4)]*[m^mu]*[] = [m^(-mu-4+mu)] = [m^-4] * 10^-3 = [mm^-1 m^-3]

    return n, diam


########################################################################




def normalized_gamma(mu, n_0=None, n_w=None, D_m=None, lamb=None, lwc=None, D=None,
                     D_min=0.01, D_max=10, npoints=100, scale='log'):

    '''
    Returns an array of n(D), the number of drops n at each diameter D using a
    normalized gamma distribution: n(D) = N_w * f(mu) * (D/D_m) * exp(-(4+mu)(D/D_m))
    where f(mu) = (6*(4+mu)^(4+mu))/(256*gamma(4+mu)).

    Inputs:
        mu           | Shape parameter []
        n_0          | Standard Gamma intercept parameter [mm^-(1+mu) m^-3]
        n_w          | Normalized Gamma intercept parameter [mm^-1 m^-3]
        D_m          | Median Diameter [mm]
        lamb         | Slope parameter [mm^-1]
        lwc          | Liquid water content [g m^-3]
        D            | (Optional) User provides their own array of D
                          sizes in mm.
        D_min        | Minimum size of droplets [mm] (Default 10 um)
        D_max        | Maximum size of droplets [mm] (Default 10 mm)
        npoints      | Number of droplet diameters to calculate n for
                         (Default 100)
        scale        | Whether D space is set up in log space or
                         linear space.
    Outputs:
        n            | Array of size D that gives the number concentration,
                         or number of drops per volume [m^-3 mm^-1]

    Notes:
        These parameters can be specified in a number of different combinations
        and used to derive the others. For derivations of the relationships
        used below, please refer to Testud et al. 2001.
    '''

    rho_l = 1000.     #Density of liquid water [kg/m^3]

    #Set up D array:
    if scale == 'log':
        diam = 10.**(np.linspace(np.log10(D_min), np.log10(D_max), npoints))
    elif scale == 'linear':
        diam = np.linspace(D_min, D_max, npoints)
    if D is not None:
        diam = D


    #First error check: conflicts
    if D_m is not None and lamb is not None:
        raise ValueError(f'Both D_m and lamb cannot be specified.')


    #Second error check: make sure we have enough constraints
    given = {
        'n_0': n_0 is not None,
        'n_w': n_w is not None,
        'D_m': D_m is not None,
        'lamb': lamb is not None,
        'lwc': lwc is not None
    }

    valid_combos = [
        {'D_m', 'n_w'},
        {'D_m', 'n_0'},
        {'D_m', 'lwc'},
        {'lamb', 'n_w'},
        {'lamb', 'n_0'},
        {'lwc', 'n_w'},
    ]

    provided = {k for k, v in given.items() if v}

    # Check if any valid combo is a subset of provided
    if not any(combo <= provided for combo in valid_combos):
        raise ValueError(
            f"Invalid parameter set: {provided}. "
            f"You must provide one of: {valid_combos}"
        )

    #Fill in missing parameters:
    if 'D_m' not in provided:
        if 'lamb' in provided:
            D_m = (4.+mu) / lamb  #[mm]
        else:
            lamb = ((4.+mu)**4 * ((np.pi*rho_l*n_w*1000.)/(256.*lwc*0.001)))**0.25 * 0.001   #[mm^-1]
            D_m = (4.+mu) / lamb  #[mm]

    if 'n_w' not in provided:
        if 'n_0' in provided:
            n_w = n_0 * D_m**mu * (math.gamma(4.+mu)/6.) * (256./((4.+mu)**(4.+mu))) #[mm^-1 m^-3]
        elif 'lwc' in provided:
            n_w = (256./(np.pi*rho_l)) * ((lwc*0.001)/((D_m*0.001)**4)) * 0.001 #[mm^-1 m^-3]
        elif 'lamb' in provided and 'n_0' in provided:
            D_m = (4.+mu) / lamb #[mm]
            n_w = n_0 * D_m**mu * (math.gamma(4.+mu)/6.) * (256./((4.+mu)**(4.+mu))) #[mm^-1 m^-3]


    #Final check:
    assert D_m is not None
    assert n_w is not None

    x = diam / D_m

    f_mu = (6. * (4.+mu)**(4.+mu)) / (256. * math.gamma(4.+mu))

    f_x = f_mu * x**mu * np.exp(-(4.+mu)*x)

    n = n_w * f_x #Final units: [mm^-1 m^-3]

    return n, diam

########################################################################
