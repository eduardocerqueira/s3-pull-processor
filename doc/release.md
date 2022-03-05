# release

* [pypi](https://pypi.org/project/s3-pull-processor/)
* [pypitest env](https://test.pypi.org/project/s3-pull-processor/)

## pre-requisite

* testpypi and pypi TOKEN

```shell
# build
python3.9 -m build

# release to TEST https://test.pypi.org/project/s3-pull-processor/
python3.9 -m twine upload --repository testpypi dist/*

# release to PROD
python3.9 -m twine upload dist/*
```
