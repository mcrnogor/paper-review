#!/bin/bash

for i in {0..29}

do

flx2xsp bn121225417_ALP_xspec_$i.txt bn121225417_ALP_xspec_$i.pha bn121225417_ALP_xspec_$i.rsp xunit=MeV yunit=ph/cm^2/s/MeV

done
