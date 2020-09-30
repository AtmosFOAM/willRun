# willRun
Test cases for the AtmosFOAM-multiFluid Boussinesq model.

## Prerequisites
* Install [OpenFOAM dev](https://github.com/OpenFOAM/OpenFOAM-dev).
* Install [AtmosFOAM-tools](https://github.com/AtmosFOAM/AtmosFOAM-tools/).
* Install [AtmosFOAM](https://github.com/AtmosFOAM/AtmosFOAM/).
* Install [AtmosFOAM-multiFluid](https://github.com/AtmosFOAM/AtmosFOAM-multiFluid/).
* If you need to run 2-fluid Boussinesq simulations, you must firstly run the 200 column single-fluid test case at [boussinesqEquations/warmBubble/1Fluid/200col/](boussinesqEquations/warmBubble/1Fluid/200col/). This will conditionally average the data for each resolution for each timestep (which usually takes at least 10 hours). 

## Running and analysing 2-fluid test cases
* Test cases are located in [boussinesqEquations/warmBubble/](boussinesqEquations/warmBubble/).
* Run all your chosen testcases at all chosen resolutions in [runAll.py](boussinesqEquations/warmBubble/runAll.py).
* Extract all .xyz files using [copyRawData.py](boussinesqEquations/warmBubble/copyRawData.py).
* Plot the data using [plotProfiles.py](boussinesqEquations/warmBubble/rawData/plotProfiles.py).

## Transfer analysis of 2-fluid system
* Transfer analysis of the 2-fluid model can be conducted from [boussinesqEquations/warmBubble/2Fluid_transferAnalysis/](boussinesqEquations/warmBubble/2Fluid_transferAnalysis/) using [runAll_TransferAnalysis.py](boussinesqEquations/warmBubble/2Fluid_transferAnalysis/runAll_TransferAnalysis.py).
* This will run the 2-fluid model for 1 timestep starting from all timesteps saved by the 1-Fluid simulation.
