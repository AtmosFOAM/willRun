#!/bin/bash -e

case=.

# clear out old stuff
rm -rf $case/[0-9]* $case/constant/polyMesh $case/core $case/log

# create mesh
blockMesh -case $case

# Initial conditions from ../resolved_singleFluid with modifications
#cp -r ../../1Fluid/200col/conditionallyAveraged/1col/2 ./0
#cp 0/u 0/u.stable
#cp 0/u 0/u.buoyant
#sed -i 's/buoyancyf/bf.sum/g' 0/P
cp -r init/ ./0

setFields

# Solve multi-fluid Boussinesq equations
#multiFluidBoussinesqFoam >& log & sleep 0.01; tail -f log
multiFluidBoussinesqFoamDwDtTransfer

# Plots
mv 0/P.buoyant 0/Pi.buoyant
mv 0/P.stable 0/Pi.stable
#writeCellDataxyz sigma.stable
#writeCellDataxyz sigma.buoyant
#writeCellDataxyz b.stable
#writeCellDataxyz b.buoyant
#writeCellDataxyz u.stable
#writeCellDataxyz u.buoyant
#writeCellDataxyz uz.stable
#writeCellDataxyz uz.buoyant
#writeCellDataxyz P.stable
#writeCellDataxyz P.buoyant
for time in [0-9]*; do
    ../../plots/plotProfiles.sh $case $time
done

