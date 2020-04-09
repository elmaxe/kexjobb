#!/bin/bash
# Prints queries to stdout
#
# $1 Path to root directory of data. MUST NOT END WITH A SLASH.
#------------------------------------------------------------
    # The directories and files must be structured and named in the following way
    # root
    #   5000
    #       data-5000.txt
    #   10000
    #       data-10000.txt
    #   15000
    #       .
    #       .
    #       .
    #   35000
    #       ...
#------------------------------------------------------------
# $2 Query range, euclid
# $3 Query range, chebyshev
# $4 Number of queries

densities=( 5000 10000 15000 20000 25000 30000 35000 40000 45000 50000 )

for d in "${densities[@]}"
do
    shuf $1/$d/data-$d.txt > temp.txt
    head -$4 temp.txt > temp2.txt
    rm temp.txt
    awk -v var="$2" '$4=var' temp2.txt > $1/$d/queries-$d-euclid.txt
    rm temp2.txt
done

for d in "${densities[@]}"
do
    shuf $1/$d/data-$d.txt > temp.txt
    head -$4 temp.txt > temp2.txt
    rm temp.txt
    awk -v var="$3" '$4=var' temp2.txt > $1/$d/queries-$d-cheb.txt
    rm temp2.txt
done
