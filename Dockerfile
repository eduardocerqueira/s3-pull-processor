FROM fedora:35

LABEL name="poc-s3-pull-processor"
LABEL author="eduardomcerqueira@gmail.com"
LABEL maintainer="eduardomcerqueira@gmail.com"
LABEL description="POC producer and consumer artifact from/to centralized object storage"

# AWS environment variables
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV AWS_S3_SECURE_CONNECTION=${AWS_S3_SECURE_CONNECTION}

ENV VIRTUAL_ENV=/opt/src/s3-pull-processor/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opt/src/s3-pull-processor

# packages required in OS
RUN dnf install git -y

# install from repo
# RUN git clone https://github.com/eduardocerqueira/s3-pull-processor.git .

# install from local source code, files in .dockerignore will be excluded
COPY . .

RUN env

RUN sh ops/scripts/install.sh
CMD s3-pull-processor
