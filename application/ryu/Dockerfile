FROM ubuntu:16.04 

RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    python-setuptools \
    python-pip \
    python-eventlet \
    python-lxml \
    gcc python-dev libffi-dev \
    libssl-dev libxml2-dev \
    libxslt1-dev zlib1g-dev \
    wget \
    unzip && \
    # fix error: https://stackoverflow.com/questions/40184788/protocol-not-found-socket-getprotobyname
    apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall netbase -y && \
    apt-get clean && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Clone https://github.com/faucetsdn/ryu/archive/master.zip and install" && \
    wget -O /opt/ryu.zip "https://github.com/faucetsdn/ryu/archive/master.zip" --no-check-certificate && \
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
COPY response.py /usr/local/lib/python2.7/dist-packages/webob/

RUN cd /opt/ryu && python ./setup.py install

WORKDIR /opt/ryu/

# "--observe-links", # esto bindea los links en el topology
CMD [ "./bin/ryu-manager", "--observe-links", "ryu.app.rest_topology", "ryu.app.ws_topology", "ryu.app.ofctl_rest", "ryu.app.qos_simple_switch_13_CAC", "ryu.app.qos_simple_switch_rest_13_CAC", "ryu.app.rest_conf_switch", "ryu.app.rest_qos" ]

# CORS RYU webob del distpackage...