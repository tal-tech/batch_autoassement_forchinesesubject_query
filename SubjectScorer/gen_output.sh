#!/bin/bash
python TestPerformance.py data/$1
mv subject_scorer.log log$1
cat log$1 | grep "####" > ll$1

