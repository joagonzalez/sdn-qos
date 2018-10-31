FROM ubuntu:latest

USER root
WORKDIR /root

COPY ./wait-for-it.sh /
COPY ./topologies /
COPY mininet-setup.sh /

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iproute2 \
    iputils-ping \
    mininet \
    net-tools \
    openvswitch-switch \
    openvswitch-testcontroller \
    tcpdump \
    linphone-nogtk \
 && rm -rf /var/lib/apt/lists/* \
 && chmod +x /mininet-setup.sh

ENTRYPOINT ["/mininet-setup.sh"]
