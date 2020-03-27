#!/bin/bash
# $1 Path to data
# $2 Path to query points
# $3 Distance function: "maximum" or "euclid"
if [ "$3" == "maximum" ]; then
    dist="minkowski.MaximumDistanceFunction"
else
    dist="minkowski.EuclideanDistanceFunction"
fi

strategyIndices=( nobulk str astr onedim binsplit hilbert peano zcurve)

strategies[nobulk]=" "
strategies[str]="-spatial.bulkstrategy SortTileRecursiveBulkSplit"
strategies[astr]="-spatial.bulkstrategy AdaptiveSortTileRecursiveBulkSplit"
strategies[onedim]="-spatial.bulkstrategy OneDimSortBulkSplit"
strategies[binsplit]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort BinarySplitSpatialSorter"
strategies[hilbert]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort HilbertSpatialSorter"
strategies[peano]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort PeanoSpatialSorter"
strategies[zcurve]="-spatial.bulkstrategy SpatialSortBulkSplit -rtree.bulk.spatial-sort ZCurveSpatialSorter"

for strategy in "${strategyIndices[@]}"
do
    echo "Start $strategy"
    echo "./elkinogui.sh -dbc.in $1 -db.index tree.spatial.rstarvariants.rstar.RStarTreeFactory -pagefile.pagesize 4096 ${strategies[$strategy]} -time -algorithm benchmark.RangeQueryBenchmarkAlgorithm -algorithm.distancefunction $dist -rangebench.query FileBasedDatabaseConnection -dbc.in $2 -evaluator NoAutomaticEvaluation -resulthandler ResultWriter | grep --invert-match '#'"
    ./elkinogui.sh -dbc.in $1 -db.index tree.spatial.rstarvariants.rstar.RStarTreeFactory -pagefile.pagesize 4096 ${strategies[$strategy]} -time -algorithm benchmark.RangeQueryBenchmarkAlgorithm -algorithm.distancefunction $dist -rangebench.query FileBasedDatabaseConnection -dbc.in $2 -evaluator NoAutomaticEvaluation -resulthandler ResultWriter | grep --invert-match '#' > $strategy.txt
    echo "Finshed $strategy"
    echo ""
done