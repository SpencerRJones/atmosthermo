from . import interpolate, convert
from .clausius_clapeyron import clausius_clapeyron
import numpy as np
from pathlib import Path

localdir = Path(__file__).resolve().parent

'''
Class of US Standard Atmosphere (1976) variables and quantities

All units are SI
'''



class us_standard_atmosphere:

    def __init__(self):
        rawdata = np.loadtxt(f'{localdir}/usstdatm_raw.txt')

        self.nlevels = rawdata.shape[0]
        self.nlayers = self.nlevels-1
        self.max_height = 75000.
        self.min_height = -5000.
        self.units = 'SI'

        self.height = rawdata[:,0]
        self.temperature = rawdata[:,1]
        self.pressure = rawdata[:,2]
        self.density = rawdata[:,3]


    def recalculate(self):

        '''
        Recalculate all variables in US Standard Atmosphere
        '''

        #Check for change in nlayers/nlevels:
        if self.nlevels != 1601:
            self.nlayers = self.nlevels - 1

        if self.nlayers != 1600:
            self.nlevels = self.nlayers + 1

        #Check for max height > 100.
        if self.max_height != 75000.:
            if self.max_height > 75000.:
                raise ValueError(f'Max height cannot be > 75 km.')

            else:
                max_idx = np.searchsorted(self.height, self.max_height)
                self.height = self.height[:max_idx + 1]
                self.pressure = self.pressure[:max_idx + 1]
                self.temperature = self.temperature[:max_idx + 1]

        #Check for min height < 0.
        if self.min_height != -5000.:
            if self.min_height < -5000.:
                raise ValueError(f'Min height cannot be < -5000.')


        #Recalculate variables
        new_height = np.linspace(self.min_height, self.max_height, self.nlevels)

        self.pressure = interpolate(self.pressure, self.height, new_height, kind='log')
        self.temperature = interpolate(self.temperature, self.height, new_height, kind='linear')

        self.height = new_height
       

    def like_ERA5(self):

        '''
        Get values at specified levels
        '''

        plevs = np.array([
                1000.,  975.,  950.,  925.,  900.,  875.,  850.,  825.,  800.,  775.,  750.,  700.,
                650.,  600.,  550.,  500.,  450.,  400.,  350.,  300.,  250.,  225.,  200.,  175.,
                150.,  125.,  100.
                ])
        plevs_r = np.flip(plevs*100.)
        pres_r = np.flip(self.pressure)
        hgt_r = np.flip(self.height)
        temp_r = np.flip(self.temperature)
        dens_r = np.flip(self.density)
        hgt = np.zeros_like(plevs)
        temp = np.zeros_like(plevs)
        dens = np.zeros_like(plevs)
        for i, lev in enumerate(plevs_r):
            idx = np.searchsorted(pres_r, lev)
            hgt[i] = hgt_r[idx]
            temp[i] = temp_r[idx]
            dens[i] = dens_r[idx]

        hgt = np.flip(hgt)
        temp = np.flip(temp)
        dens = np.flip(dens)

        self.height = hgt
        self.pressure = plevs*100.
        self.temperature = temp
        self.density = dens


    def assume_humidity(self,rh):
        
        '''
        Assume humidity throughout the profile or
        a single relative humidity value for all layers.
        Returns specific humidity [kg/kg]
        '''

        self.vapor_pressure = clausius_clapeyron(self.temperature) * rh
        self.specific_humidity = convert.VaporPressure2SpecificHumidity(
                    self.vapor_pressure, self.pressure
                )
        

          
