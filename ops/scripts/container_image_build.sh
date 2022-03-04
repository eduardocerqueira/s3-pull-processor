#!/bin/bash

# build docker container image.
# how to run: sh ops/scripts/container_image_build.sh

source $(dirname "$0")/lib.sh

# build custom images
print_header "build s3-pull-processor image"
docker build -t s3-pull-processor -f Dockerfile . --network=host

print_header "list s3-pull-processor images"
docker image ls | grep -e 's3-pull-processor'
echo
