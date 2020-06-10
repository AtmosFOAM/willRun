#!/bin/bash -e

case=.
time=$1

# clear out old stuff
rm -rf $case/[0-9]* $case/constant/polyMesh $case/core $case/log

# create mesh
blockMesh -case $case

# Initial conditions from ../resolved_singleFluid with modifications
cp -r ../../1Fluid/200col/conditionallyAveraged/1col/$time ./0
sed -i 's/buoyancyf/bf.sum/g' 0/P

# Solve multi-fluid Boussinesq equations
#multiFluidBoussinesqFoam >& log & sleep 0.01; tail -f log
multiFluidBoussinesqFoamWTransfer

# Plots
mv 0/P.buoyant 0/Pi.buoyant
mv 0/P.stable 0/Pi.stable
for time in 0 2; do
    ./plotProfiles.sh $case $time
done

