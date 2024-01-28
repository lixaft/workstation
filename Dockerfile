FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN : \
    && apt-get update \
    && apt-get install -y \
        python3 \
        software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

COPY hosts.yml workstation.yml run /workstation
COPY group_vars /workstation/group_vars
COPY roles /workstation/roles

WORKDIR /workstation
