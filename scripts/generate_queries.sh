#!/bin/bash
# Prints queries to stdout
# $1 File containing the model
# $2 Query range
# $3 Number of queries

shuf $1 > temp.txt
head -$3 temp.txt > temp2.txt
rm temp.txt
awk -v var="$2" '$4=var' temp2.txt
rm temp2.txt