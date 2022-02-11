# developer guide

## install

```shell
sh ops/scripts/install.sh
```

## run

```shell
# generate some artifacts
sh ops/scripts/artifact_generator.sh

# upload artifact
s3-pull-processor upload --path /home/ecerquei/git/s3-pull-processor/artifacts/artifact-1.tar.gz

# pull artifacts
s3-pull-processor pull --interval 10

# pull artifacts and run action
s3-pull-processor pull --interval 10 --action ibutsu
```

## developer guide

```shell
pip install --editable .[dev]
pre-commit run --all
```
