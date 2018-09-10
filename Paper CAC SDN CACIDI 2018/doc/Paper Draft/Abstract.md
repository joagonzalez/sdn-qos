# Using Software-Defined Networking for Call Admission Control and VoIP applications

## Abstract

### Tema
Call Admission Control (CAC) es un mecanismo que permite establecer un límite en la cantidad de sesiones concurrentes que se establecen en una red VoIP basada en SIP. Dicho mecanismo no se encuentra estandarizado y su implementación genera dificultades en entornos de redes tradicionales donde interactúan elementos de red fabricados por diferentes vendors.
El modelo propuesto por Software Defined Networking (SDN) plantea una separación entre el plano de control y el plano de de datos de las redes, definiendo interfaces abiertas y programables que permiten desarrollar aplicaciones que interactúen con los elementos de red de diferentes vendors de manera flexible y uniforme, lo que brinda un entorno ideal para resolver la interoperabilidad de CAC.

### Objetivos
El objetivo de este trabajo es describir las especificaciones, diseño e implementación de un mecanismo CAC que permite sacar provecho de las ventajas del modelo propuesto por SDN. Asimismo, desarrollar un prototipo simulado en entorno virtual que nos permita comprobar el funcionamiento y obtener conclusiones respecto del comportamiento buscado.

### Metodología
Para ello, se describe el modelo de arquitectura de la aplicación desarrollada y se realizan simulaciones utilizando Mininet para la conformación de la topología de red, Ryu como controlador SDN y Asterisk como aplicación PBX basada en SIP.

### Discusión
Este trabajo se propone discutir, a través del desarrollo e implementación de funcionalidades de red, las ventajas del marco de trabajo propuesto por las redes definidas por software. Se espera contribuir con un modelo para el desarrollo de un mecanismo CAC que sea vendor agnostic, gracias a la utilización de interfaces abiertas y programables brindadas por controladores y aplicaciones como Asterisk.

## Abstract (English)

Call Admission Control (CAC) is a mechanism that allows to fix the amount of concurrent sessions established within a VoIP application based on SIP protocol. Such mechanism is not standardized and its deployment brings difficulties in traditional network environments where different networking devices from multiple vendors interact with each other. Software Defined Networking (SDN) is a model that decouples the control and forwarding logic from the network infrastructure making it programmable and providing open interfaces. This scenario makes an ideal environment in order to solve CAC interoperability.

The aim of this paper is to describe specifications, design and deployment of a novel CAC application that allows to take advantage of SDN model. In addition, we developed a first version of this application and report experimental testing and evaluation results for this prototype. 

For this purpose, we describe an architectural model of the developed application and we run simulations using Mininet for network topology, Ryu as SDN controller and Asterisk as IP PBX software application based on SIP protocol. Finally, taking advantage of SDN model, this application implement real-time QoS during simulations for building a more realistic scenario regarding how prioritization and CAC mechanism work together in order to guarantee the quality of service.

This paper presents the advantages of the SDN framework through the development and implementation of network applications. We conclude with a discussion on how these applications provide a vendor agnostic and standardized solution for network mechanisms such as CAC. 

https://www.ietf.org/rfc/rfc2753.txt
https://tools.ietf.org/html/rfc4804
