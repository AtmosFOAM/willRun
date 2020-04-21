#!/bin/bash -e

# Horizontal average and conditional average based on the sign of w 

if [ "$#" -ne 2 ]
then
   echo usage: ./conditionalAverage.sh caseName time
   exit
fi

case=$1
time=$2
newCase=3col

# Calculate sigma based on w on the resolved mesh
writeuvw -case $case -time $time u
conditionalAverage -case $case -time $time uz 0 stable buoyant

# Multiply fields by sigma (zero or one)
for part in stable buoyant; do
    for var in b uz P; do
        multiplyFields -case $case $time sigma$var.$part $time $var \
             $time sigma.$part
    done
done

# Horizontal averages

for newCase in 1col; do

    # Map onto coarse mesh
    mapFields -case $case/conditionallyAveraged/$newCase -mapMethod \
        cellVolumeWeight $case -consistent -noFunctionObjects -sourceTime $time
    rm -rf $case/conditionallyAveraged/$newCase/$time
    mv $case/conditionallyAveraged/$newCase/0.1 \
        $case/conditionallyAveraged/$newCase/$time

    # Divide conditional average fields by sigma
    for part in stable buoyant; do
        for var in b uz P; do
            multiplyFields -case $case/conditionallyAveraged/$newCase $time \
                $var.$part $time sigma$var.$part $time sigma.$part -pow1 -1
        done
    done

    # Write out ascii data and sort by z
    for part in '' .stable .buoyant; do
        for var in b uz P sigma sigmab sigmaP sigmauz; do
            if [ -a $case/conditionallyAveraged/$newCase/$time/$var$part ]; then
                writeCellDataxyz -case $case/conditionallyAveraged/$newCase -time $time $var$part
                sort -g -k 3 \
                    $case/conditionallyAveraged/$newCase/$time/$var$part.xyz \
                    | sponge \
                    $case/conditionallyAveraged/$newCase/$time/$var$part.xyz
            fi
        done
    done

    # Calculate pressure difference from the mean
    for part in stable buoyant; do
        paste $case/conditionallyAveraged/$newCase/$time/P.$part.xyz \
            $case/conditionallyAveraged/$newCase/$time/P.xyz | \
            awk '{print $1, $2, $3, $4-$8}' > \
            $case/conditionallyAveraged/$newCase/$time/Pi.$part.xyz
    done
done

