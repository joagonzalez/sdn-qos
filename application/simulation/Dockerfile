FROM ubuntu:latest

USER root
WORKDIR /root

COPY ./wait-for-it.sh /root
COPY simulation-setup.sh /root

RUN apt-get update && apt-get install -y --no-install-recommends \
    sip-tester \
    tcpdump \
    netcat \
 && chmod +x /root/simulation-setup.sh \
 && chmod +x /root/wait-for-it.sh

# ENTRYPOINT ["bash"]
CMD ["/root/simulation-setup.sh"]
