FROM ubuntu:latest

USER root
WORKDIR /root

COPY ./wait-for-it.sh /root
COPY simulation-setup.sh /

RUN apt-get update && apt-get install -y --no-install-recommends \
    sip-tester \
    tcpdump \
    netcat \
 && chmod +x /simulation-setup.sh

# ENTRYPOINT ["bash"]
CMD ["/simulation-setup.sh"]
