FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive
RUN : \
    && apt-get update \
    && apt-get install --assume-yes \
        python3 \
        software-properties-common

WORKDIR /workstation
COPY . .
RUN ["python3", "run"]
