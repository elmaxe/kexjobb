#!/bin/bash
# $1 Path to root directory of data. MUST NOT END WITH A SLASH.
#------------------------------------------------------------
    # The directories and files must be structured and named in the following way
    # root
    #   5000
    #       data-5000.txt
    #       queries-5000-euclid.txt
    #       queries-5000-cheb.txt
    #   10000
    #       data-10000.txt
    #       queries-10000-euclid.txt
    #       queries-10000-cheb.txt
    #   15000
    #       .
    #       .
    #       .
    #   35000
    #       ...
#------------------------------------------------------------
# $2 Path to output folder, doesn't need to exist beforehand. MUST NOT END WITH A SLASH.

densities=( 5000 10000 15000 20000 25000 30000 35000 40000 45000 50000 )

for d in "${densities[@]}"
do
    echo "Starting experiments for density of $d"
    # echo "./experiment.sh $1/$d/data-$d.txt $1/$d/queries-$d-euclid.txt euclid $2/$d/euclid"
    ./experiment.sh $1/$d/data-$d.txt $1/$d/queries-$d-euclid.txt euclid $2/$d/euclid
    # echo "./experiment.sh $1/$d/data-$d.txt $1/$d/queries-$d-cheb.txt maximum $2/$d/cheb/"
    ./experiment.sh $1/$d/data-$d.txt $1/$d/queries-$d-cheb.txt maximum $2/$d/cheb/
    echo "Finished experiments for density of $d"
done