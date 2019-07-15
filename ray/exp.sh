#!/bin/bash

for i in `seq 1 1 5`
do
    python exp${i}.py 2>&1 | tee log${i}.txt
done
