# Real-time QoS and Call admission Control in SDN networks
![Python](https://img.shields.io/badge/qos-v1.0.0-orange)
![Python](https://img.shields.io/badge/cac-v1.0.0-orange)
![Python](https://img.shields.io/badge/OpenFlow-v1.3-orange)
![Python](https://img.shields.io/badge/ryuframework-4.34-blue)
![Python](https://img.shields.io/badge/python-v2.7-blue)
![Python](https://img.shields.io/badge/python-v3.6-blue)
![Python](https://img.shields.io/badge/platform-linux--64%7Cwin--64-lightgrey)

Implementation of quality of service and call admission control features within sdn networks. This implementation use Ryu Framework (https://ryu-sdn.org/) to develop controller applications based on OpenFlow v1.3. Features are integrated to an Asterisk service through ARI API via websockets. Application behaviour is exposed via a basic Front End service developed with node.js.

Applicationa architecture is shown in the figure below.

![architecture](documentation/architecture/diagrams/Real-TimeQoSandCACoverSDN-12.png)


**Table of contents**

- [Requirements](#requirements)
- [Getting Started](#gettingstarted)
- [Development](#development)
  - [Archivo de configuración](#archivo-de-configuración)
  - [Clases](#clases)
  - [Registración del servicio](#registración-del-servicio)
  - [Flask API](#flask-api)
    - [Blueprints](#blueprints)
    - [Namespaces](#namespaces)
  - [Celery workers](#celery-workers)
  - [Celery tasks](#celery-tasks)
  - [RabbitMQ](#rabbitmq)
  - [Powershell scripts](#powershell-scripts)
- [Deployment](#deployment)
  - [Building](#building)
  - [Docker deployment](#docker-container-dployment)
  - [docker-compose deployment](#docker-compose-deployment)
- [Examples](#examples)
- [references](#references)



## Ver videos (drive)
Branches: Mergear a una rama teniendo master/develop y branches por feature y comenzar a utilizar tags. Hoy en dia tenemos 2 principales y una tercera con feature experimental.

- cac-be-with-gui-topology-call-simulation-and-graphic-traffic-ovs-over-mn -- sipp simulation + cac + gui topology
- CAC_App_v1_refactor -- real time qos scripts and wireshark i/o
- cac-traffic-reporter-graph -- traffic reporter class que broadcastea con tshark/tcpdump data de simulator al backend y luego al frontend

```
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

```
# Show git branch name
force_color_prompt=yes
color_prompt=yes
parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
if [ "$color_prompt" = yes ]; then
 PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
else
```
