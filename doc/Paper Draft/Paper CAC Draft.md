## Using Software-Defined Networking for Call Admission Control and VoIP applications

### Sección I - Introducción: CAC y SDN

Call Admission Control (CAC) es un mecanismo que permite establecer un límite en la cantidad de sesiones concurrentes que se establecen en una red VoIP [1]. Esta funcionalidad brinda un mecanismo de control y prevención de congestión indispensable en redes que soportan tráfico real-time, en donde la calidad de las comunicaciones debe estar garantizada.

Mecanismos típicos de CAC son, por ejemplo, denegar el establecimiento de una llamada cuando no existen recursos de procesamiento en los dispositivos de la red, o cuando el tráfico o cantidad de llamadas exceden un límite máximo preestablecido. Debido a que no existe un único mecanismo, y ninguno de ellos se encuentra estandarizado con excepción de un framework de referencia [12], no existe un criterio uniforme a la hora de lograr una interacción entre dominios de proveedores de servicio diferentes.

El estado del arte en la práctica sobre redes VOIP, indica que los mecanismos CAC son implementaciones que residen mayormente en la IP PBX, utilizando criterios e interfaces propietarias de quienes desarrollan la solución. Esto no favorece el objetivo de estandarizar un mecanismo que trabaje entre dominios con IP PBX’s pertenecientes a distintos fabricantes.

En este paper se propone abordar la problemática mencionada aprovechando las ventajas que brinda la tecnología de Software-Defined Networking, proponiendo un modelo de arquitectura con interfaces abiertas y programables (API's) para el desarrollo de un mecanismo CAC que actúe de manera uniforme con IP PBX’s pertenecientes a distintos fabricantes. 

La arquitectura SDN de la Figura 1 plantea un modelo donde se separa el plano de control (Controlador SDN) del plano de conmutación de la red [2], especificando interfaces abiertas y programables (API’s) para el plano de control tanto en el sentido Northbound como Southbound. Esto permite el desarrollo de aplicaciones que pueden interactuar con el plano de control manejando los elementos de conmutación mediante una capa de abstracción que favorece la programabilidad de la red. 

[Acá va la figura 1 de Arquitectura SDN]

Si bien en la actualidad no hay un estándar definido para las interfaces API, en la práctica suele optarse por el protocolo OpenFlow para la interfaz Southbound e implementaciones de interfaces API REST para la comunicación Northbound.

Lo que resta del paper está organizado de la siguiente manera. En la sección II, describimos los requisitos de funcionamiento asociados al mecanismo CAC y definimos las especificaciones de las interfaces Northbound y Southbound que deberá tener la aplicación a desarrollar. En la sección III abordamos el diseño y desarrollo de una aplicación que implementa las funcionalidades especificadas. En la sección IV, se describe el desarrollo de un prototipo funcional el cual se utiliza para realizar las pruebas y obtener los resultados experimentales descriptos en la sección V. Finalmente, en la sección VI se finaliza con las conclusiones y observaciones referentes a la modelización de CAC en entornos SDN.

### Sección II - Especificación de la aplicación CAC

Típicamente, una implementación de CAC se puede separar en dos funciones básicas, una que permita, o no, el inicio de una llamada en base a una política preestablecida, y otra que garantice la calidad de las llamadas que ya se encuentran en curso. 

La figura 2 muestra la estructura de una implementación CAC desde el punto de vista de una arquitectura cliente-servidor. La figura muestra un proceso servidor que atenderá los intentos de inicio de sesión de los diferentes clientes, y ante el cual el proceso servidor deberá permitir o denegar las mismas, comparando el número de sesiones activas con el máximo preestablecido en las políticas del dominio. Posteriormente, en caso de que se permita el inicio de sesión, el proceso servidor deberá realizar un cambio de estado en los elementos de red que permita establecer el tráfico de datos entre los clientes origen y destino, garantizando la calidad de servicio (QoS). En caso de que no se permita el inicio de sesión, el proceso servidor deberá realizar el aviso correspondiente hacia los clientes.
 
 ### NOTA:  Desarrollar diferencias entre esquema CAC tradicional (usado con colas QoS) con CAC SDN en donde se implementa la calidad del servicio (colas) en forma dinámica/tiempo real - Ver si va aca o en Seccion I

[Acá poner figura 2 Cliente-Servidor]

El diseño del flujo de trabajo para el proceso servidor, debe contemplar la respuesta hacia los clientes en tiempo real, por lo que el intercambio de mensajes entre ellos debe ser tratado en los elementos de red de manera prioritaria.  

Implementar este tipo de comunicación en redes convencionales, y garantizar el grado de QoS necesario para las llamadas, puede convertirse en un desafío para los desarrolladores que no posean conocimientos en networking, debido a la falta de abstracción que suele haber en las interfaces que poseen los elementos de red. El uso de SDN  debe permitir al desarrollador abstraerse del conocimiento detallado de los elementos de red, permitiéndole programar de manera sencilla su comportamiento para obtener los resultados que se buscan.

Como resultado de estas consideraciones, se listan las principales funcionalidades que debe cumplir la aplicación CAC a desarrollar:

1 -  Debe ser capaz de comunicarse a través de una interfaz abierta y bien definida que permita el intercambio de mensajes y eventos con la IP PBX. 
2 - Debe ser capaz de recibir y manejar los mensajes asociados a los siguientes eventos que ocurran en la IP PBX:
 - Establecimiento de una llamada
 - Cambios en los parámetros asociados a una llamada ya establecida
 - Finalización de una llamada
3 - Debe denegar o permitir el establecimiento de una llamada en base a un máximo predefinido por el administrador del dominio
4 - Debe interpretar los requerimientos de QoS necesarios para las llamadas que puedan iniciarse y traducirlos a mensajes que actúen sobre los elementos de red a través del controlador SDN
5 - Debe poseer una interfaz que permita la interacción con el administrador del dominio

### Sección III - Diseño de la aplicación CAC 

En la figura 3 se muestra el diseño de la arquitectura básica para la implementación de la funcionalidad CAC en  entornos SDN, la cual incluye los siguientes componentes:

[Acá agregar figura 3 Arquitectura Básica]

Proceso Servidor CAC: aplicación servidor que implementa la lógica especificada, capturando los eventos que envía la IP PBX a través de la Northbound API y enviando la información necesaria hacia el controlador SDN a través de la Southbound API, para que se realicen las acciones necesarias sobre los elementos de red.

Server: Un server físico o máquina virtual con capacidad para correr un proceso servidor CAC. El proceso servidor CAC podría estar distribuído en múltiples servers para mitigar problemas de escalabilidad. 

Clientes SIP: una aplicación cliente que utiliza señalización SIP contra la IP PBX para el establecimiento de llamadas VOIP.

Elementos de red: switches SDN programables a través de un controlador SDN mediante OpenFlow.

Controlador SDN: recibe las directivas, a través de la interfaz southbound API, para que se establezcan los flujos de datos con la QoS requerida entre los clientes SIP y la PBX; y programa los elementos de red utilizando OpenFlow.

Módulo SDN: Integrado dentro del proceso servidor CAC, recibe la información relacionada al establecimiento de sesiones y envía las directivas hacia el controlador SDN a través de la interfaz southbound API.

Módulo Policy Manager: Integrado dentro del proceso servidor CAC, implementa la interfaz con el administrador del dominio, mediante la cual se definen las políticas de control para el proceso CAC. Además, provee monitoreo y estadísticas relacionadas al consumo de recursos.  

Módulo CAC: Integrado dentro del proceso servidor CAC, implementa la comunicación con la PBX a través de la interfaz Northbound API. Realiza el monitoreo de los eventos que genera la PBX,  realiza el control de establecimiento de las sesiones y envía los requerimientos de QoS hacia el módulo SDN.

IP PBX: Es la que establece la comunicación con los clientes SIP y maneja las sesiones. Además, envía los eventos e información necesaria hacia el módulo CAC para que se realice el control correspondiente.

### Sección IV - Implementación del prototipo

Para poder evaluar la implementación de CAC en el entorno SDN, se desarrolló un prototipo montado sobre un escenario completamente virtual basado en Mininet[3]. Dado que el objetivo primordial era comprobar el funcionamiento del modelo sin hacer foco en métricas referidas a performance, el escenario virtual montado sobre Mininet brinda un marco ideal para evaluaciones rápidas y de bajo costo.
El desarrollo del prototipo se basó pricipalmente en el uso de herramientas de software de código abierto, de uso modular y portable, y con características que favorecen la escalabilidad.
Además, se optó como criterio quitar complejidad desde el punto de vista de networking y hacer foco en la interacción de la aplicación CAC desarrollada con la PBX y el controlador SDN. 
Para el desarrollo de la aplicación, optamos por implementar una arquitectura del tipo model-view-controller (MVC)[4], desacoplando los servicios de visualización y procesamiento en front-end y back-end respectivamente.

 Para el desarrollo del front-end, se optó por implementar una interfaz WEB GUI basada en Node.js[5], mediante la cual los usuarios puede interactuar con la aplicación. A través de la interfaz de usuario, se realiza el ingreso de los parámetros necesarios para el funcionamiento del mecanismo CAC, que para el prototipo resulta ser la máxima cantidad de llamadas simultáneas permitidas.
 Otra de las funciones de la interfaz de usuario, son la visualización de estadísticas correspondientes al consumo de recursos de red (tráfico en interfaces, ancho de banda consumido, delay y latencia).
El back-end se resolvió mediante la interacción de una IP PBX basada en Asterisk[6], un controlador SDN basado en Ryu[7] y elementos de red basados en OpenVSwitch[8]. 
Asterisk posee la interfaz ARI (Api Rest Interface)[9], la cual permite a través de un web socket el monitoreo de sus eventos y la ejecución de aplicaciones externas asociadas a los mismos. Esto se aprovechó para implementar la interfaz Northbound API de la aplicación CAC. En la fase de establecimiento de una llamada, Asterisk transfiere el control hacia la aplicación CAC, la cual monitorea los eventos que señaliza Asterisk a través del web socket. Los eventos que se monitorean son los de inicio de llamada, cambios en una llamada existente ó finalización de llamada.
Ante un evento de inicio de llamada, se compara la cantidad máxima de llamadas establecidas por el usuario con la cantidad de llamadas en curso. Si se supera el máximo permitido, la aplicación finaliza la llamada y envía a través de Asterisk el aviso correspondiente a los clientes SIP.
En caso de que no se supere el máximo definido por el usuario, se acepta la llamada, y se obtienen a través de Asterisk el SDP con los parámetros de sesión SIP que luego serán utilizados por el módulo SDN.  
En el módulo SDN se realizan tres operaciones en base a la información del SDP que se recibe de cada sesión SIP. El primer paso consiste en extraer del SDP las direcciones IP, los puertos y parámetros de media que utilizarán los clientes SIP para establecer la llamada. Con estos datos el módulo SDN deberá determinar la ubicación dentro de la red de los clientes SIP, lo que se obtiene enviando una consulta con el formato adecuado al controlador SDN a través de la interfaz REST. El segundo paso consiste en armar las reglas de flujo OpenFlow para establecer en el switch el path de la media RTP entre los clientes SIP. Las reglas de flujo contienen como campo de matching la información obtenida a partir del descubrimiento de red y dos acciones asociadas, las cuales consisten en marcar el tráfico del flujo RTP como prioritario (mediante el marcado del campo DSCP=XX), y posteriormente enviarlo a la cola de alta prioridad del puerto de salida que corresponda.
El tercer paso consiste en formatear el mensaje para enviarlo a través de la interfaz REST hacia el controlador SDN. 
En la figura 4 se puede visualizar un diagrama de flujo que explica la lógica de funcionamiento de la aplicación CAC desarrollada.
Con la finalidad de otorgarle mayor flexiblidad al tratamiento de los flujos y mejorar la eficiencia en el intercambio de mensajes entre controlador SDN y elementos de red, se optó por usar OpenFlow 1.3, el cual nos permite armar un pipeline [10] de tratamiento de flujos mediante el uso de multi-tablas.
Como controlador SDN se utilizó Ryu, el cual implementa OpenFlow 1.3 y posee módulos que implementan métodos de consultas, establecimiento de flujos y colas de servicio sobre los elementos de red a través de una interfaz REST, lo que nos brinda una excelente capa de abstracción desde el punto de vista del desarrollador. Se aprovechó el framework existente de Ryu y se lo modificó agregando los métodos REST necesarios para interactuar con la interfaz Southbound API del módulo SDN en la aplicación CAC.
Como switch SDN utilizamos OpenVSwitch, el cual soporta OpenFlow 1.3 como protocolo de comunicación con el controlador SDN y permite trabajar en su implementación de Kernel-Space con colas de servicio asociadas a sus puertos.
Los clientes SIP que se utilizaron están basados en Linphone[11].

En la figura 5, se muestra el prototipo desarrollado:

[Acá iría la figura 4 con el diagrama de flujo que explica la lógica de la aplicación]

[Acá iría figura 5 con la maqueta especificada con el tipo de PBX, controlador, switch openflow, etc]


### Sección V - Pruebas, evaluación y resultados obtenidos

Las pruebas realizadas consistieron en ingresar mediante la interfaz de usuario el número máximo de llamadas simultánes en 3. Luego se generaron 3 llamadas, usando los clientes SIP basados en Linphone, desde el Host 1 al Host 2. En este punto, se pudo comprobar que todas las llamadas se establecieron con éxito, pero al intentar el inicio de una cuarta llamada, el mecanismo de CAC la rechaza dando aviso a los clientes SIP acerca de la imposibilidad de establecerla.
Para comprobar  que las 3 llamadas que se encuentran en curso tienen garantizado el QoS, se genera un escenario de congestión inyectando adicionalmente tráfico best-effort mediante Iperf desde el Host 1 al Host 2. En la figura 6 se puede visualizar cómo el tráfico de voz resulta de mayor prioridad y no existe prácticamente pérdida de paquetes, mientras que para el tráfico best-effort sucede lo contrario, demostrando que las reglas de flujo actúan correctamente enviando el tráfico RTP de media a las colas de alta prioridad asociadas a los puertos de salida, logrando de esta manera el traffic shaping deseado.  

[Acá iría la figura 6 con gráfica de resultados]


### Sección VI - Conclusiones

El motivo del presente trabajo era encontrar una modelización de macanismo CAC que trabaje sobre entornos de red SDN, facilitando la interoperabilidad con la IP PBX y la programabilidad de la red frente a requerimientos de calidad de servicio que ejercen las llamadas basadas en tecnologías VOIP.

Nuestra contribución es la especificación de un modelo para el desarrollo de aplicaciones CAC en entornos SDN,  basada en el uso de interfaces API y herramientas de código abierto. 
Cabe destacar, que si bien aún no existe un marco formal de estandarización para la interacción de mecanismos CAC con IP PBXs de diferentes fabricantes, el modelo presentado brinda una posible solución a este problema, la cual puede lograrse con herramientas de uso accesible y libre, como las utilizadas en el prototipo desarrollado.

El uso de entornos SDN ofrece múltiples ventajas desde el punto de vista de la red, por ejemplo la posibilidad de que el mecanismo CAC opere con IP PBXs desarrolladas por diferentes fabricantes; así como también, la programabilidad de los elementos de red para reaccionar en forma dinámica a los requerimientos de QoS de las llamadas que se establezcan. 

En nuestra primer evaluación, hemos encontrado resultados favorables que nos alientan a pensar, adicionalmente, en el uso del modelo presentado para el desarrollo de nuevas aplicaciones sobre entornos SDN, ya sea para expandir las funcionalidades del prototipo ensayado ó para trabajar sobre otros escenarios.

References:
[1] "VoIP Call Admission Control. https://www.cisco.com/c/en/us/td/docs/ios/solutions_docs/voip_solutions/CAC.html," 2001.

[2] Open Networking Foundation, “SDN architecture 1.0 - ONF TR-502,” 2014.

[3] "Mininet. http://mininet.org/," 2018.

[4] Glenn E. Krasner, Stephen T. Pope “A Cookbook for Using View-Controller User the Model-Interface Paradigm in Smalltalk-80,” Journal of Object-Oriented Programming, 1988.

[5] "Node.js. https://nodejs.org/en/," 2018.

[6] "Asterisk. https://www.asterisk.org/," 2018.

[7] "Ryu SDN Controller. https://osrg.github.io/ryu/," 2018.

[8] "OpenVSwitch. https://www.openvswitch.org/," 2018.

[9] "Asterisk Rest Interface (ARI). https://wiki.asterisk.org/wiki/pages/viewpage.action?pageId=29395573," 2017.

[10] Open Networking Foundation, "OpenFlow Switch Specification Version 1.3.0 - ONF TS-006," 2012.

[11] "Linphone. http://www.linphone.org/," 2018.

[12] https://www.ietf.org/rfc/rfc2753.txt



-----------------------------------------------------------

## TODOS

- Armar gráfico/explicacion arquitectura nivel sofware de aplicacion CAC
- Hablar de pruebas simple_switch OpenFlow1.5 para utilizar nuevas metricas y features agregadas en estas versiones
- Hablar de objetivo final respecto de graficos que se esperan realizar y resultados que se esperan obtener con este modelo de trabajo










    

