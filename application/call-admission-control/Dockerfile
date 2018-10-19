FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    git \
    python-setuptools \
    python-pip \
    python-pycurl

RUN pip install git+https://github.com/dpallot/simple-websocket-server
RUN mkdir /app
RUN mkdir /app/src/
RUN mkdir /app/src/backend
RUN mkdir /app/src/frontend
RUN mkdir /app/bin/

# SETUP BACKEND
COPY src/backend /app/backend
RUN ls -lh  /app/backend
# SETUP FRONTEND
COPY src/frontend /app/frontend
RUN ls -lh /app/frontend
# SETUP EJECUTABLE
COPY bin/ /app/bin
RUN ls -lh /app/bin

# PERMISOS SCRIPT
RUN chmod 777 /app/bin/sdn-qos.sh

FROM node:8
# INSTALL FRONTEND DEPENDENCIES
RUN npm install --prefix /app/frontend


WORKDIR /app

#CMD ["sh", "/app/bin/sdn-qos.sh"]
CMD bash -C '/app/bin/sdn-qos.sh';'bash'
