import os,sys

'''
Script which runs all specified test cases at
all specified resolutions.
'''

baseFolder = os.path.dirname(os.path.realpath(__file__))

testCases = []
testCases.append("2Fluid_DEFAULT")
# testCases.append("2Fluid_gammaZero")
# testCases.append("2Fluid_gammaZero_noTransfer")
# testCases.append("2Fluid_noTransfer")
# testCases.append("2Fluid_gaussianTransfer")
# testCases.append("2Fluid_cosineSquaredTransfer")
# testCases.append("2Fluid_wMeanTransfer")
# testCases.append("2Fluid_wMeanCellTransfer")

resolutions = ["200col", "100col", "50col", "20col", "10col", "5col", "3col", "1col"]
resolutions = ["5col", "3col", "1col"]

for testCase in testCases:
    for resolution in resolutions:
        folder = os.path.join(baseFolder, testCase)
        folder = os.path.join(folder, resolution)
        
        os.chdir(folder)
        os.system("./run.sh")

os.chdir(baseFolder)
