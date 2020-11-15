FROM ubuntu:18.04

USER root
WORKDIR /root

COPY ./wait-for-it.sh /

COPY ./topologies /

COPY ./mininet-setup.sh /
COPY ./api.py /
COPY ./loggerService.py /
COPY ./MyTopo.py /
COPY ./simulation-topology.py /
COPY ./SimulationApp.py /
COPY ./__init__.py /


RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iproute2 \
    iputils-ping \
    mininet \
    net-tools \
    libcurl4-openssl-dev \ 
    libssl-dev \
    openvswitch-switch \
    openvswitch-testcontroller \
    python-setuptools \
    libffi-dev \
    python-dev \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python-pip \
 && rm -rf /var/lib/apt/lists/* \
 && chmod +x /mininet-setup.sh

RUN pip install wheel
RUN pip install mininet 
RUN pip install pycurl

ENTRYPOINT ["/mininet-setup.sh"]
