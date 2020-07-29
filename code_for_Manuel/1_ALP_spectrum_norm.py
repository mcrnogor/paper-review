#!/usr/bin/env python                                                          #
#                                                                              #
# Autor: Milena C.                                                             #
# Date: 7/22/2019                                                              #
# Use: Producing ALP text files to be passed to HEASOFT to produce XSPEC       #
#      ALP spectra with a given input normalization and energy range.          #
#------------------------------------------------------------------------------#

import os
import sys
import argparse
import numpy as np
# import astropy & ALPs after xspec, conflicting libraries

import xspec as xs
xs.Xset.allowPrompting = False #keeps pyxspec from hanging, waiting a response to a prompt
xs.Xset.allowNewAttributes = True

# Normalization values:
N=np.logspace(np.log10(8.4e-8), np.log10(8.4e2), 30) # cm^-2

# Defining the strings for spectral files
spectrum = 'bn121225417_LAT-LLE_bkgspectra.bak{1}'
# background = 'bn121225417_LAT-LLE_bkgspectra.bak{1}'
bkg_unqual = 'bn121225417_LAT-LLE_bkgspectra.bak'
response = 'bn121225417_LAT-LLE_weightedrsp.rsp'

# Opening spectra in XSPEC
xs.AllData.clear()
s = xs.Spectrum(spectrum)
s.response = (response)
#s.background= (background)

# plotting and extracting values
xs.Plot.device="/xs"
xs.Plot.xAxis="MeV"
xs.Plot.add=True
xs.Plot.background=True
xs.Plot.xLog=True
xs.Plot.yLog=True
xs.Plot.show()
xs.Plot("data")

# background data and errors
xerr = np.asarray(xs.Plot.xErr()) # in MeV
yerr = np.asarray(xs.Plot.yErr()) # in ph/s/MeV/cm^2
bkg = xs.Plot.y()
splitted = spectrum.split("_")[0]

# Defining the energy range, as determined by the LLE background
from astropy.io import fits
hdu = fits.open(bkg_unqual)
energy = hdu[2].data # reported in keV
E_MeV = (energy['E_MIN'] + energy['E_MAX'])/2000. # average bin energy in MeV


# Calculating the ALP stuff
sys.path.append('/Users/milena/Desktop/2nd_yr_project/ALPs/ALPs_analysis/') # path to calc_alp_signal script
from scipy import integrate
from calc_alp_signal import ALPSNSignal

alp_sn10 = ALPSNSignal(Mprog = 10.)
ts = np.linspace(0.,25.,len(E_MeV))
dndedt_alp10 = alp_sn10(E_MeV, ts, g10=0.1)
SED10 = integrate.simps(dndedt_alp10, ts)/ts.max()
SED10_norm = np.empty((len(N), len(SED10)))
SED10_norm_bkg = np.empty((len(N), len(SED10)))
lc10 = integrate.simps(dndedt_alp10, E_MeV)


for i in range(len(N)):
    SED10_norm[i,:] = N[i]*SED10 # normalized spectrum
    SED10_norm_bkg[i,:] = N[i]*SED10+bkg # normalized spectrum on top of the bkg

np.save(splitted+'_SED10.npy', SED10)
np.save(splitted+'SED10_norm.npy', SED10_norm)
np.save(splitted+'SED10_norm_bkg.npy', SED10_norm_bkg)
np.save(splitted+'_EMeV.npy', E_MeV) # saving mean energy bin values
np.save(splitted+'_lc10.npy', lc10)

# producing a file for XSPEC:
# https://heasarc.gsfc.nasa.gov/lheasoft/ftools/headas/ftflx2xsp.html

column1 = np.empty((len(N), len(SED10)))
column2 = np.empty((len(N), len(SED10)))
column3 = np.empty((len(N), len(SED10)))
column4 = np.empty((len(N), len(SED10)))

for i in range(len(N)):
    column1[i,:] = energy['E_MIN'] / 1000. # in MeV
    column2[i,:] = energy['E_MAX'] / 1000. # in MeV
    column3[i,:] = SED10_norm_bkg[i,:] # in ph/cm^2/s/MeV
    column4[i,:] = yerr*N[i]*1e-52 # random uncertainty

    #column4[i,:] = np.random.normal(0, 1e-52, len(SED10)) # random uncertainty
    data = np.array([column1[i, :], column2[i, :], column3[i, :], column4[i, :]]).T
    np.savetxt(splitted+'_ALP_xspec_%i.txt' %i, data)
