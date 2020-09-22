import os,sys

baseFolder = sys.path[0]
baseFolderRaw = os.path.join(baseFolder, "rawData")

if not os.path.exists( baseFolderRaw ):
    os.makedirs( baseFolderRaw )



testCases = ["1Fluid", "2Fluid", "2Fluid_temp", "2Fluid_wTransfer"]
testCases = ["2Fluid_temp"]
testCases = ["2Fluid_cosineSquaredTransfer"]
testCases = ["2Fluid_cosineSquaredTransfer_divTransfer"]
testCases = ["2Fluid_stabilityAnalysis"]
testCases = ["2Fluid_oneD"]
#testCases = ["2Fluid"]

resolutions = ["200col", "100col", "50col", "20col", "10col", "5col", "3col", "1col"]
resolutions = ["5col", "3col", "1col"]
resolutions = ["1col"]
#resolutions = ["200col"]

times = ["500", "1000"]
times = ["0", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"]
times = range(0,5100,100)

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
            
            if os.path.exists(folder):
                if not os.path.exists( folderRaw ):
                    os.makedirs( folderRaw )
                
                os.system("cp {}/*.xyz {}/".format(folder, folderRaw))
    
    #os.system("cp -r {}/ $DROPBOX/".format( os.path.join(baseFolderRaw, testCase) ))
    os.system("cp -r {}/ /mnt/f/Desktop/".format( os.path.join(baseFolderRaw, testCase) ))
