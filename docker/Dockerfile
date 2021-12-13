# 1st Stage
FROM python:3.8.7-slim-buster AS builder
LABEL maintainer="sejongjeong <wjdtpwhd@gmail.com>"

# install required packages
RUN apt-get update \
	&& apt-get install -y --no-install-recommends git \
	&& apt-get install -y --no-install-recommends ssh \
	&& apt-get install -y gcc \
	&& rm -rf /var/lib/apt/lists/

# make github as a known host
RUN mkdir -p -m 0600 /root/.ssh \
	&& ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts

## ADD SSH Key into Docker container
ADD id_rsa /root/.ssh/id_rsa

COPY . /main
WORKDIR /main
ENV PYTHONPATH=/main
ENV PYTHONUNBUFFERED=1

RUN pip install pip==21.2.4 && \
	pip install -r requirements.txt && \
	git clone 