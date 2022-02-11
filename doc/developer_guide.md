# developer guide

## install

```shell
sh ops/scripts/install.sh
```

or to setup your dev environment:

```shell
pip install --editable .[dev]
```

## pre-requisite

export AWS variables

```shell
export AWS_ACCESS_KEY_ID=**************
export AWS_SECRET_ACCESS_KEY==**************
export AWS_DEFAULT_REGION==**************
export AWS_S3_SECURE_CONNECTION==**************
```

## run

follow steps from [pre-requisite](developer_guide.md#pre-requisite)

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

## running tests

follow steps from [pre-requisite](developer_guide.md#pre-requisite)

```shell
# SQS message tests
pytest -srxv test_sqs_messages.py

# S3 bucket tests
pytest -srxv test_s3_files.py

# E2E
pytest -srxv test_e2e.py
```

### Scenarios

#### HOST A send messages and HOST B consume messages from SQS

```shell
# terminal 1
watch -n 1 "pytest -srxv test_sqs_messages.py -k test_send_message"

# terminal 2
watch -n 1 "pytest -srxv test_sqs_messages.py -k test_consume_all_messages"
```

![scenario1](img/scenario_1.png)

#### HOST A upload artifact to S3 and HOST B consuming it

```shell
# terminal 1
watch -n 1 "pytest -srxv test_e2e.py -k test_host_uploader"

# terminal 2
watch -n 1 "pytest -srxv test_e2e.py -k test_host_consumer"
```

![scenario2](img/scenario_2.png)

## contributing

before commit any code, run lint, it is required to have [dev](../setup.cfg) packages installed

```shell
pre-commit run --all
```
