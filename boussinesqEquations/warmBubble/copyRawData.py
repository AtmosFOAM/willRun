import os,sys

'''
Script which copies all .xyz files from test cases
into an identical directory structure within the 
"./rawData/" folder.
This makes it easier (more lightweight) to export
the data elsewhere.

Must run runAll.py (with same test cases) 
before running this script.
'''

#Folder of this script and rawData folder
baseFolder = os.path.dirname(os.path.realpath(__file__))
baseFolderRaw = os.path.join(baseFolder, "rawData")

if not os.path.exists( baseFolderRaw ):
    os.makedirs( baseFolderRaw )

#Folder to which files are exported after
exportData = False
folderExport = "/mnt/f/Desktop/"

testCases = []
testCases.append("1Fluid")
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

times = ["500", "1000"]
#times = ["0", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"]

for testCase in testCases:
    for resolution in resolutions:
        for time in times:
            if testCase == "1Fluid":
                folder = os.path.join(baseFolder, testCase)
                folder = os.path.join(folder, resolution)
                folder = os.path.join(folder, "conditionallyAveraged")
                folder = os.path.join(folder, "1col")
                folder = os.path.join(folder, str(time))
                
                folderRaw = os.path.join(baseFolderRaw, testCase)
                folderRaw = os.path.join(folderRaw, resolution)
                folderRaw = os.path.join(folderRaw, "conditionallyAveraged")
                folderRaw = os.path.join(folderRaw, "1col")
                folderRaw = os.path.join(folderRaw, str(time))
            else:
                folder = os.path.join(baseFolder, testCase)
                folder = os.path.join(folder, resolution)
                folder = os.path.join(folder, str(time))
                
                folderRaw = os.path.join(baseFolderRaw, testCase)
                folderRaw = os.path.join(folderRaw, resolution)
                folderRaw = os.path.join(folderRaw, str(time))
            
            if os.path.exists( folderRaw ):
                os.system("rm {}/*.xyz".format(folderRaw))

            print "Attempting to copy {}".format(folder)
            if os.path.exists(folder):
                if not os.path.exists( folderRaw ):
                    os.makedirs( folderRaw )
                
                os.system("cp {}/*.xyz {}/".format(folder, folderRaw))
    
    if exportData:
        os.system("cp -r {}/ {}".format(os.path.join(baseFolderRaw, testCase), folderExport))
