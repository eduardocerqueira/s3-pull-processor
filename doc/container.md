# container

```shell
# build container
sh ops/scripts/container_image_build.sh

# run container with no arguments
docker run --name poc-s3 s3-pull-processor
```

## example

Simulating HOST-A uploading artifact data to S3, and HOST-B pulling data from S3 and SQS and processing it.

```shell
# HOST-A
docker run --name host-a s3-pull-processor s3-pull-processor upload -p /tmp/test123.tar -f

# HOST-B
docker run --name host-b s3-pull-processor s3-pull-processor pull
```
