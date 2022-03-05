# release

## pypi

* [pypi](https://pypi.org/project/s3-pull-processor/)
* [pypitest env](https://test.pypi.org/project/s3-pull-processor/)

### pre-requisite

* testpypi and pypi TOKEN

```shell
# build
python3.9 -m build

# release to TEST https://test.pypi.org/project/s3-pull-processor/
python3.9 -m twine upload --repository testpypi dist/*

# release to PROD
python3.9 -m twine upload dist/*
```

## ghcr.io container image

### pre-requisite

* CR_PAT github TOKEN

```shell
echo $CR_PAT | docker login ghcr.io -u eduardocerqueira --password-stdin
docker tag f849ee50d8b1 ghcr.io/eduardocerqueira/s3-pull-processor:latest
docker push ghcr.io/eduardocerqueira/s3-pull-processor:lates
```
