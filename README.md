
# atmosthermo
A Python Module for commonly used atmospheric thermodynamics conversions and functions.

### Getting Started
It is recommended that this module be installed using PIP. atmosthermo uses very few outside dependencies and is made to be as intuitive to use as possible. For this reason, many of the utilities are simply Python functions and most mathematical operations are performed using numpy. To install,

```bash
pip install atmosthermo
```

Test the import and make a simple example calculation:

```console
$ python
>>> import atmosthermo as at
>>> T = 288.1
>>> e_s = at.clausius_clapeyron(T)
>>> print(f'Saturation vapor pressure at {T}K: {e_s:.3f}')
Saturation vapor pressure at 288.1K: 1728.676
```

### Examples
#### 1. Conversions:
Several useful functions for converting between atmospheric variables are in the `convert` section of the module. All conversions are called using the name of the variable to convert from, the name of the variable to convert to, and separating them by a "2". All variable names are in Camel Case for easier readibility. For instance, if you want to convert from vapor pressure [Pa] to specific humidity [kg/kg], you would call:
```console
$ python
>>> import atmosthermo as at
>>> e = 6.18
>>> p = 101325.
>>> q = at.convert.VaporPressure2SpecificHumidity(e, p)
>>> print(f'Specific humidity = {q} [kg/kg]')
Specific humidity = 3.793693560325684e-05 [kg/kg]
```
These functions are also vectorized so they can do as many conversions at once:
```console
$ python
>>> import numpy as np
>>> import atmosthermo as at
>>> theta = np.array([320., 300., 290])
>>> p = np.array([101325., 100000., 95000.])
>>> at.convert.PotentialTemperature2Temperature(theta, p)
array([321.20533567, 300.        , 285.78237322])
```
Python `help()` also can be useful if you are not sure how to use a particular function.
```console
$ python
>>> import atmosthermo as at
>>> help(at.convert.SpecificMass2SpecificContent)
Help on function SpecificMass2SpecificContent in module atmosthermo.convert:

SpecificMass2SpecificContent(c, p, t, q=None)
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
```

#### 2. Using the US Standard Atmosphere

The US Standard Atmosphere (1976) is preloaded into the atmosthermo module as a Python class. The default resolution is 50 meters per layer, but this can be changed to any resolution quite simply using a single call that recalculates all variables:
```
>>> import atmosthermo as at
>>> #Initialize the atmosphere
>>> atm = at.us_standard_atmosphere()
>>> atm.height
array([-5000., -4950., -4900., ..., 74900., 74950., 75000.], shape=(1601,))
>>> atm.temperature
array([320.65 , 320.325, 320.   , ..., 206.85 , 206.75 , 206.65 ],
      shape=(1601,))
>>> #Let's look at the number of height levels:
>>> atm.nlayers
1600
>>> #Let's change the number of layers:
>>> atm.nlayers = 100
>>> #Calling recalculate checks to see if the number of layers has
>>> # changed and recalculates variables accordingly
>>> atm.recalculate()
>>> atm.height
array([-5000., -4200., -3400., -2600., -1800., -1000.,  -200.,   600.,
        1400.,  2200.,  3000.,  3800.,  4600.,  5400.,  6200.,  7000.,
        7800.,  8600.,  9400., 10200., 11000., 11800., 12600., 13400.,
       14200., 15000., 15800., 16600., 17400., 18200., 19000., 19800.,
       20600., 21400., 22200., 23000., 23800., 24600., 25400., 26200.,
       27000., 27800., 28600., 29400., 30200., 31000., 31800., 32600.,
       33400., 34200., 35000., 35800., 36600., 37400., 38200., 39000.,
       39800., 40600., 41400., 42200., 43000., 43800., 44600., 45400.,
       46200., 47000., 47800., 48600., 49400., 50200., 51000., 51800.,
       52600., 53400., 54200., 55000., 55800., 56600., 57400., 58200.,
       59000., 59800., 60600., 61400., 62200., 63000., 63800., 64600.,
       65400., 66200., 67000., 67800., 68600., 69400., 70200., 71000.,
       71800., 72600., 73400., 74200., 75000.])
```
It is also possible to change where the atmosphere begins and ends. Let's say we want to go from the surface to 50 km and we want 50 layers:
```console
$ python
>>> import atmosthermo as at
>>> atm = at.us_standard_atmosphere()
>>> atm.min_height = 0.
>>> atm.max_height = 50000.
>>> atm.nlayers = 50
>>> atm.recalculate()
>>> atm.height
array([    0.,  1000.,  2000.,  3000.,  4000.,  5000.,  6000.,  7000.,
        8000.,  9000., 10000., 11000., 12000., 13000., 14000., 15000.,
       16000., 17000., 18000., 19000., 20000., 21000., 22000., 23000.,
       24000., 25000., 26000., 27000., 28000., 29000., 30000., 31000.,
       32000., 33000., 34000., 35000., 36000., 37000., 38000., 39000.,
       40000., 41000., 42000., 43000., 44000., 45000., 46000., 47000.,
       48000., 49000., 50000.])
>>> atm.temperature
array([288.15, 281.65, 275.15, 268.65, 262.15, 255.65, 249.15, 242.65,
       236.15, 229.65, 223.15, 216.65, 216.65, 216.65, 216.65, 216.65,
       216.65, 216.65, 216.65, 216.65, 216.65, 217.65, 218.65, 219.65,
       220.65, 221.65, 222.65, 223.65, 224.65, 225.65, 226.65, 227.65,
       228.65, 231.45, 234.25, 237.05, 239.85, 242.65, 245.45, 248.25,
       251.05, 253.85, 256.65, 259.45, 262.25, 265.05, 267.85, 270.65,
       270.65, 270.65, 270.65])
```

