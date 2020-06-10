import os,sys

baseFolder = sys.path[0]
baseFolderRaw = os.path.join(baseFolder, "rawData")

if not os.path.exists( baseFolderRaw ):
    os.makedirs( baseFolderRaw )



resolutions = ["5col", "3col", "1col"]
#resolutions = ["5col", "3col"]
times = range(2,504,2)

for resolution in resolutions:
    
    for time in times:
        folderRaw = os.path.join(baseFolderRaw, resolution)
        folderRaw = os.path.join(folderRaw, str(time+2))
        os.system("mv {}/massTransferreddwdtTransfer.stable.xyz {}/massTransferredNewdwdtTransfer.stable.xyz".format(folderRaw, folderRaw))
        os.system("mv {}/massTransferreddwdtTransfer.buoyant.xyz {}/massTransferredNewdwdtTransfer.buoyant.xyz".format(folderRaw, folderRaw))
    
# os.system("cp -r {}/ $DROPBOX/".format( os.path.join(baseFolderRaw, testCase) ))
