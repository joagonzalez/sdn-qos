FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    git \
    python-setuptools \
    python-pip \
    python-pycurl

RUN pip install git+https://github.com/dpallot/simple-websocket-server

WORKDIR /app

# SETUP BACKEND
COPY ./src/backend /app/backend

# SETUP FRONTEND
COPY ./src/frontend /app/frontend

FROM node:8
# INSTALL FRONTEND DEPENDENCIES
RUN npm install --prefix /app/frontend

CMD ["bash", "./bin/sdn-qos.sh"]
