FROM ubuntu:lastest

RUN apt-get install pycurl python-pip
RUN pip install git+https://github.com/dpallot/simple-websocket-server

# SETUP BACKEND
RUN mkdir /app/backend
COPY ./src/backend /app/backend

# SETUP FRONTEND
RUN mkdir /app/frontend
COPY ./src/frontend /app/frontend

# INSTALL FRONTEND DEPENDENCIES
RUN npm install --prefix /app/frontend

WORKDIR /app

CMD ["bash", "./bin/sdn-qos.sh"]
