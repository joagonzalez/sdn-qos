FROM ubuntu:latest

USER root
WORKDIR /root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iproute2 \
    iputils-ping \
    nmap \
    sip-tester \
    wireshark \
    tcpdump \
    linphone-nogtk \
    linphone 

ENTRYPOINT ["/bin/bash"]
