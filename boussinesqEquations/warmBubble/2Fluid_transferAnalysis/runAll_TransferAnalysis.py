import os,sys

baseFolder = sys.path[0]
baseFolderRaw = os.path.join(baseFolder, "rawData")

if not os.path.exists( baseFolderRaw ):
    os.makedirs( baseFolderRaw )



resolutions = ["5col", "3col", "1col"]
#resolutions = ["5col", "3col"]
resolutions = ["1col"]
times = range(2,504,2)
times = range(350,504,2)

for resolution in resolutions:
    
    for time in times:
        print 10*"{}, t={}s\n".format(resolution, time)
        
        folder = os.path.join(baseFolder, resolution)
        
        os.chdir(folder)
        os.system("./run.sh {}".format(time))
        
        folder = os.path.join(folder, "2")
        
        folderRaw = os.path.join(baseFolderRaw, resolution)
        folderRaw = os.path.join(folderRaw, str(time+2))
        
        if os.path.exists( folderRaw ):
            os.system("rm {}/*.xyz".format(folderRaw))
        
        if os.path.exists(folder):
            if not os.path.exists( folderRaw ):
                os.makedirs( folderRaw )
            
            os.system("cp {}/*.xyz {}/".format(folder, folderRaw))
    
# os.system("cp -r {}/ $DROPBOX/".format( os.path.join(baseFolderRaw, testCase) ))
