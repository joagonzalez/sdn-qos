## Abstract

### Tema
Call Admission Control (CAC) es un mecanismo que permite establecer un límite en la cantidad de sesiones concurrentes que se establecen en una aplicación VoIP basada en SIP. Dicho mecanismo no se encuentra estandarizado y su implementación tiene dificultades en ambientes con múltiples vendors.
El modelo propuesto por Software Defined Networking (SDN) desacopla el plano de control del plano de datos de la red, definiendo interfaces abiertas que hacen a la red programable y adaptable a los cambios requeridos por las aplicaciones. Este modelo brinda un escenario ideal para la implementación de aplicaciones de red como CAC.

### Objetivos
El objetivo de este trabajo es describir las especificaciones, diseño e implementación de una aplicación de CAC que permite sacar provecho de las ventajas del modelo propuesto por SDN. Asimismo, simular el funcionamiento del prototipo y evaluar su performance a partir de métricas pre-establecidas.

### Metodología
Para ello, se describe el modelo de arquitectura de la aplicación desarrollada y se realizan simulaciones utilizando Mininet para la conformación de la topología de red, Faucet como controlador SDN y Asterisk como aplicación VoIP basada en SIP junto con su REST API. 

### Discusión
Este trabajo se propone discutir, a través del desarrollo e implementación de funcionalidades de red, las ventajas del marco de trabajo propuesto por las redes definidas por software. Se espera contribuir con un modelo de CAC vendor agnóstico gracias a la utilización de interfaces abiertas brindadas por controladores y aplicaciones como Asterisk utilizadas en conjunto con el protocolo OpenFlow.

