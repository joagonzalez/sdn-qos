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
