#!/bin/sh
# 1000 replicate sweeps on the cluster (about 3 days)
for i in $(seq 1 1000); do slim -d N=1000 slim/selection.slim > results/sweep_$i.txt; done
