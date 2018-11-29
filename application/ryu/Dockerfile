FROM ubuntu:latest 

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python-setuptools \
    python-pip \
    python-eventlet \
    python-lxml \
    wget \
    unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Download https://github.com/osrg/ryu/archive/master.zip and install" && \
    wget -O /opt/ryu.zip "http://github.com/osrg/ryu/archive/master.zip" --no-check-certificate && \
    unzip -q /opt/ryu.zip -d /opt && \
    mv /opt/ryu-master /opt/ryu && \
    rm /opt/ryu.zip && \
    cd /opt/ryu && \
    pip install -r tools/pip-requires && \
    python ./setup.py install

RUN pip install -r /opt/ryu/tools/pip-requires --upgrade 

# ADD applications/qos_simple_switch_13_CAC.py opt/ryu/ryu/app/qos_simple_switch_13_CAC.py
COPY applications/qos_simple_switch_13_CAC.py opt/ryu/ryu/app/qos_simple_switch_13_CAC.py
COPY applications/qos_simple_switch_rest_13_CAC.py opt/ryu/ryu/app/qos_simple_switch_rest_13_CAC.py
COPY applications/simple_switch_13_CAC.py opt/ryu/ryu/app/simple_switch_13_CAC.py

RUN cd /opt/ryu && python ./setup.py install

WORKDIR /opt/ryu/

# "--observe-links", # esto bindea los links en el topology
CMD [
  "./bin/ryu-manager", 
  "--observe-links",
  "ryu.app.rest_topology",
  "ryu.app.ws_topology",
  "ryu.app.ofctl_rest",
  "ryu.app.qos_simple_switch_13_CAC",
  "ryu.app.qos_simple_switch_rest_13_CAC",
  "ryu.app.rest_conf_switch",
  "ryu.app.rest_qos"
]
