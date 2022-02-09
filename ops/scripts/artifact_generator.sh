#!/bin/bash

# artifact generator for testing
# arg: number of artifacts to be created
# how to run: sh ops/scripts/artifact_generator.sh 1

if [ $# -eq 0 ]; then
    echo "ERROR: provide a number of artifacts to be created as paramter, example: artifact_generator.sh 1"
    exit 1
fi

counter=$1
for ((i = 1 ; i <= $counter ; i++)); do
  artifact_name=artifact-$i.tar.gz
  tar -cvzf artifacts/$artifact_name --files-from /dev/null
  echo "artifacts/$artifact_name"
done
