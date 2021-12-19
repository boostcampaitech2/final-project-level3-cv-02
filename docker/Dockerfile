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


RUN pip install pip==21.2.4 && \
	git clone -b develop git@github.com:boostcampaitech2/final-project-level3-cv-02.git /root/main && \
	pip install -r /root/main/docker/requirements.txt && \
	cd /root/main && \
	git checkout -b master

# 2nd Stage
FROM python:3.8.7-slim-buster
LABEL maintainer="sejongjeong <wjdtpwhd@gmail.com>"

# copy all the settings and packages from 1st stage (builder) to avoid leak ssh key
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /root/main /main
WORKDIR /main
ENV PYTHONPATH=/main
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python", "./back-end/main.py"]