FROM python:3.9-slim-buster AS dev

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
        # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
        && apt-get update \
        && apt-get install -y sudo \
        && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
        && chmod 0440 /etc/sudoers.d/$USERNAME

RUN apt-get -qq update && apt-get install -qq -y git curl wget bash zip make

ENV DOCKER_VERSION=20.10.9
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz \
        && tar xzvf docker-${DOCKER_VERSION}.tgz --strip 1 \
        -C /usr/local/bin docker/docker \
        && rm docker-${DOCKER_VERSION}.tgz

# AWS SAM requirements
RUN pip3 install \
        pylint \
        black \
        rope \
        debugpy \
        aws-sam-cli \
        cfn-lint \
        pytest

# AWS CLI
RUN curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip \
        && unzip awscliv2.zip \
        && ./aws/install \
        && rm awscliv2.zip

# DynamoDB Local
RUN curl https://s3.ap-southeast-1.amazonaws.com/dynamodb-local-singapore/dynamodb_local_latest.zip -o dynamodb_local_latest.zip \
        && unzip dynamodb_local_latest.zip -d /opt/dynamodb_local \
        && rm dynamodb_local_latest.zip

# Dev Requirements (https://pypi.org/project/htmlwebshot/)
RUN apt-get update \
        && apt-get install -y wkhtmltopdf
RUN pip3 install htmlwebshot

# Swap to user space
USER $USERNAME
