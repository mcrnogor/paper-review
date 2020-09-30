# code for Michael

[MC, Sep 30, 2020]
This repository contains the following files:

Notebooks:

1. Faking_from_ALP_model.ipynb: jupyter notebook demonstrating an example of simulation results from the input ALP model

2. Pre-simulation_spectra_comparison.ipynb: jupyter notebook showing the discrepancy in units between the ALP code output and the XSPEC's PHA file

Files:
- bn121225417_EMeV.npy: numpy array with the LLE energy bins
- bn121225417_SED10.npy: numpy array with the input ALP spectrum
- bn121225417SED10_norm.npy: numpy array with the normalized ALP Spectrum
- bn121225417SED10_norm_bkg.npy: numpu array with normalized ALP spectra on top of a GRB background
- bn121225417_ALP_xspec_20.pha: pha file with N[20]*ALP + bkg
- bn121225417_ALP_xspec_25.pha: pha file with N[25]*ALP + bkg
- bn121225417_LAT-LLE_bkgspectra.bak: GRB background file
- bn121225417_LAT-LLE_weightedrsp.rsp: GRB response file
- bn121225417_LAT-LLE_srcspectra.pha: GRB spectral file
