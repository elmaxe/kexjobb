#!/bin/bash
# $1 Path to data.
# $2 Path to query points.
# $3 Distance function: "maximum" or "euclid".
# $4 Folder to save output files to.
if [ "$3" == "maximum" ]; then
    dist="minkowski.MaximumDistanceFunction"
else
    dist="minkowski.EuclideanDistanceFunction"
fi

strategyIndices=( str astr onedim binsplit hilbert peano zcurve nobulk)

strategies[0]="-spatial.bulkstrategy SortTileRecursiveBulkSplit"
strategies[1]="-spatial.bulkstrategy AdaptiveSortTileRecursiveBulkSplit"
strategies[2]="-spatial.bulkstrategy OneDimSortBulkSplit"
strategies[3]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort BinarySplitSpatialSorter"
strategies[4]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort HilbertSpatialSorter"
strategies[5]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort PeanoSpatialSorter"
strategies[6]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort ZCurveSpatialSorter"
strategies[7]=" "

mkdir -p $4

# for strategy in "${strategyIndices[@]}"
# do
#     echo "Start $strategy"
#     echo "./elkinogui.sh -dbc.in $1 -db.index tree.spatial.rstarvariants.rstar.RStarTreeFactory -pagefile.pagesize 4096 ${strategies[$strategy]} -time -algorithm benchmark.RangeQueryBenchmarkAlgorithm -algorithm.distancefunction $dist -rangebench.query FileBasedDatabaseConnection -dbc.in $2 -evaluator NoAutomaticEvaluation -resulthandler ResultWriter | grep --invert-match '#'"
#     time ./elkinogui.sh -dbc.in $1 -db.index tree.spatial.rstarvariants.rstar.RStarTreeFactory -pagefile.pagesize 4096 ${strategies[$strategy]} -time -algorithm benchmark.RangeQueryBenchmarkAlgorithm -algorithm.distancefunction $dist -rangebench.query FileBasedDatabaseConnection -dbc.in $2 -evaluator NoAutomaticEvaluation -resulthandler ResultWriter | grep --invert-match '#' > $4/$strategy.txt
#     echo "Finshed $strategy"
#     echo ""
# done

for ((i = 0; i < ${#strategies[@]}; i++))
do
    echo "Start ${strategyIndices[$i]}"
    echo "./elkinogui.sh -dbc.in $1 -db.index tree.spatial.rstarvariants.rstar.RStarTreeFactory -pagefile.pagesize 4096 ${strategies[$i]} -time -algorithm benchmark.RangeQueryBenchmarkAlgorithm -algorithm.distancefunction $dist -rangebench.query FileBasedDatabaseConnection -dbc.in $2 -evaluator NoAutomaticEvaluation -resulthandler ResultWriter | grep --invert-match '#'"
    time ./elkinogui.sh -dbc.in $1 -db.index tree.spatial.rstarvariants.rstar.RStarTreeFactory -pagefile.pagesize 4096 ${strategies[$i]} -time -algorithm benchmark.RangeQueryBenchmarkAlgorithm -algorithm.distancefunction $dist -rangebench.query FileBasedDatabaseConnection -dbc.in $2 -evaluator NoAutomaticEvaluation -resulthandler ResultWriter | grep --invert-match '#' > $4/${strategyIndices[$i]}.txt
    echo "Finshed ${strategyIndices[$i]}"
    echo ""
done