import os,sys

baseFolder = sys.path[0]

testCases = ["2Fluid", "2Fluid_wTransfer"]
testCases = ["2Fluid_cosineSquaredTransfer"]
testCases = ["2Fluid_cosineSquaredTransfer_divTransfer"]
testCases = ["2Fluid_stabilityAnalysis"]
#testCases = ["2Fluid"]

resolutions = ["200col", "100col", "50col", "20col", "10col", "5col", "3col", "1col"]
#resolutions = ["20col", "10col", "5col", "3col", "1col"]
resolutions = ["5col", "3col", "1col"]

for testCase in testCases:
    for resolution in resolutions:
        folder = os.path.join(baseFolder, testCase)
        folder = os.path.join(folder, resolution)
        
        os.chdir(folder)
        os.system("./run.sh")

os.chdir(baseFolder)
