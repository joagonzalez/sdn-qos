Sección I - Introducción: CAC y SDN

El presente trabajo trata acerca del uso de aplicaciones no estandarizadas denominadas Call Admission Control (CAC). Estas aplicaciones implementan mecanismos de control y prevención de congestión en redes del tipo VOIP.

Mecanismos típicos de CAC son, por ejemplo, denegar el establecimiento de una llamada cuando no existen recursos de procesamiento en los equipos de la red, ó cuando el tráfico ó cantidad de llamadas excede un límite máximo preestablecido. Debido a que no existe un único mecanismo, y ninguno de ellos se encuentra estandarizado, no existe un criterio uniforme a la hora de lograr una interacción entre dominios de proveedores de servicio diferentes.

El estado del arte en la práctica sobre redes VOIP, indica que los mecanismos CAC son implementados mayormente en la IP PBX, utilizando criterios e interfaces propietarias de quien desarrolla la solución. Esto no favorece para nada la idea de lograr tener un mecanismo CAC uniforme entre dominios con IP PBX’s pertenecientes a distintos fabricantes.

Este paper aborda la problemática mencionada usando la tecnología de Software-Defined Networking, proponiendo la arquitectura y desarrollo de un mecanismo CAC con interfaces abiertas que permita satisfacer las demandas asociadas a IP PBX’s de diferentes desarrolladores de soluciones VOIP.

La arquitectura SDN (Figura 1) plantea un modelo donde se separa el plano de control (Controlador SDN) del plano de conmutación de la red, especificando interfaces abiertas y programables (API’s) para el plano de control tanto en el sentido Northbound como Southbound. Esto permite el desarrollo de aplicaciones que pueden interactuar con el plano de control manejando los elementos de conmutación mediante una capa de abstracción que favorece la programabilidad de la red.

[Acá va la figura 1]

Si bien en la actualidad no hay un estándar definido para las API, en la práctica suele optarse por el protocolo OpenFlow para la interfaz Southbound e implementaciones de interfaces API REST para la comunicación Northbound.

Lo que resta del paper está organizado de la siguiente manera. En la sección II, describimos los requisitos de funcionamiento asociados al mecanismo CAC y definimos las especificaciones de las interfaces Northbound y Southbound que deberá tener la aplicación. En la sección III abordamos el diseño y desarrollo de la aplicación que implementa las funcionalidades especificadas. En la sección IV, se describe el desarrollo de un prototipo funcional el cual se utiliza para realizar las pruebas y obtener los resultados experimentales descriptos en la sección V. Finalmente, en la sección VI se finaliza con las conclusiones y observaciones referentes a la modelización de CAC en entornos SDN.

Sección II - Especificación de la aplicación CAC

Típicamente, una implementación de CAC se puede separar en dos funciones básicas, una que permita, o no, el inicio de una llamada en base a una política preestablecida, y otra que garantice la calidad de las llamadas que ya se encuentran en curso. 

La figura 2 muestra la estructura de una implementación CAC desde el punto de vista de una arquitectura cliente-servidor. La figura muestra un proceso servidor que atenderá los intentos de inicio de sesión de los diferentes clientes, y ante el cual el proceso servidor deberá permitir o denegar las mismas, comparando el número de sesiones activas con el máximo preestablecido en las políticas del dominio. Posteriormente, en caso de que se permita el inicio de sesión, el proceso servidor deberá realizar un cambio de estado en los elementos de red que permita establecer el tráfico de datos entre los clientes origen y destino, garantizando la calidad de servicio (QoS). En caso de que no se permita el inicio de sesión, el proceso servidor deberá realizar el aviso correspondiente hacia los clientes.
 
[Acá poner figura 2 Cliente-Servidor]

El diseño del flujo de trabajo para el proceso servidor, debe contemplar la respuesta hacia los clientes en tiempo real, por lo que el intercambio de mensajes entre ellos debe ser tratado en los elementos de red de manera prioritaria.  

Implementar este tipo de comunicación en redes convencionales, y garantizar el grado de QoS necesario para las llamadas, puede convertirse en un desafío para los desarrolladores que no posean conocimientos en networking, debido a la falta de abstracción que suele haber en las interfaces que poseen los elementos de red. El uso de SDN  debe permitir al desarrollador abstraerse del conocimiento detallado de los elementos de red, permitiéndole programar de manera sencilla su comportamiento para obtener los resultados que se buscan.

Como resultado de estas consideraciones, se listan las principales funcionalidades que debe cumplir la aplicación CAC a desarrollar:
1 -  Debe ser capaz de comunicarse a través de una interfaz abierta y bien definida que permita el intercambio de mensajes y eventos con la PBX. 
2 - Debe ser capaz de recibir y manejar los mensajes asociados a los siguientes eventos que ocurran en la PBX:
>> Establecimiento de una llamada
>> Cambios en los parámetros asociados a una llamada ya establecida
>> Finalización de una llamada
3 - Debe denegar o permitir el establecimiento de una llamada en base a un máximo predefinido por el administrador del dominio
4 - Debe interpretar los requerimientos de QoS necesarios para las llamadas que puedan iniciarse y traducirlos a mensajes que actúen sobre los elementos de red a través del controlador SDN
5 - Debe poseer una interfaz que permita la interacción con el administrador del dominio (Falta poner detalle de qué datos deben mostrarse y/o poder configurarse)

Sección III - Diseño de la aplicación CAC 

En la figura 3 se muestra el diseño de la arquitectura básica para la implementación de la funcionalidad CAC en el entorno SDN, la cual incluye los siguientes componentes:

[Acá agregar figura 3 Arquitectura Básica]

Proceso Servidor CAC: aplicación servidor que implementa la lógica especificada, capturando los eventos que envía la PBX a través de la Northbound API y enviando la información necesaria hacia el controlador SDN a través de la Southbound API, para que se realicen las acciones necesarias sobre los elementos de red.

Server: Un server físico o máquina virtual con capacidad para correr un proceso servidor CAC. El proceso servidor CAC podría estar distribuído en múltiples servers para mitigar problemas de escalabilidad. 

Clientes SIP: una aplicación cliente que utiliza señalización SIP contra la PBX para el establecimiento de llamadas VOIP.

Elementos de red: switches SDN programables a través de un controlador SDN mediante OpenFlow.

Controlador SDN: recibe las directivas, a través de la interfaz southbound de la API CAC,  para que se establezcan los flujos de datos con la QoS requerida entre los clientes SIP y la PBX; y programa los elementos de red utilizando OpenFlow.

Módulo SDN: Integrado dentro del proceso servidor CAC, recibe la información relacionada al establecimiento de sesiones y envía las directivas hacia el controlador SDN a través de la interfaz southbound API.

Módulo Policy Manager: Integrado dentro del proceso servidor CAC, implementa la interfaz con el administrador del dominio, mediante la cual se definen las políticas de control para el proceso CAC. Además, provee monitoreo y estadísticas relacionadas al consumo de recursos.  

Módulo CAC: Integrado dentro del proceso servidor CAC, implementa la comunicación con la PBX a través de la interfaz Northbound API. Realiza el monitoreo de los eventos que genera la PBX,  realiza el control de establecimiento de las sesiones y envía los requerimientos de QoS hacia el módulo SDN.

IP PBX: Es la que establece la comunicación con los clientes SIP y maneja las sesiones. Además, envía los eventos e información necesaria hacia el módulo CAC para que se realice el control correspondiente.

Sección IV - Implementación del prototipo

Para poder evaluar la implementación de CAC en el entorno SDN, se optó por quitar complejidad desde el punto de vista de networking y hacer foco en la interacción del proceso servidor CAC desarrollado con la PBX y el controlador SDN. Desde el punto de vista del desarrollo de la aplicación, optamos por implementar una arquitectura del tipo model-view-controller (MVC), desacoplando los servicios de visualización y proceso en front-end y back-end respectivamente.
El desarrollo se basó pricipalmente en herramientas de software de código open source, de uso modular y portable, y favoreciendo la escalabilidad de la solución.
 Para el desarrollo del front-end, se optó por implementar una interfaz WEB GUI basada en Node.js, mediante la cual el usuario operador puede interactuar con la aplicación. A través de la interfaz de usuario, se realiza el ingreso de los parámetros necesarios para el funcionamiento del mecanismo CAC, los cuales son: máximo número de sesiones simultáneas y .....
 Otra de las funciones de la interfaz de usuario, son la visualización de estadísticas correspondientes al consumo de recursos de red (tráfico en interfaces, ancho de banda consumido, delay y latencia).
El back-end se resolvió mediante la interacción de una IP PBX Asterisk, el controlador SDN Ryu y elementos de red OpenVSwitch. 
Asterisk posee a partir de la release XX.XX la interfaz ARI (Api Rest Interface), la cual permite a través de un web socket el monitoreo de sus eventos y la ejecución de aplicaciones externas asociadas a los mismos. Esto se aprovechó para implementar la interfaz Northbound API del proceso servidor CAC. En la fase de establecimiento de una llamada, Asterisk transfiere el control hacia la aplicación CAC desarrollada,la cual monitorea los eventos que señaliza Asterisk a través del web socket. Los eventos que se monitorean son los de inicio de llamada, cambios en una llamada existente ó finalización de llamada.
Ante un evento de inicio de llamada, se compara la cantidad máxima de llamadas establecida por el usuario con la cantidad de llamadas en curso. Si se supera el máximo permitido, la aplicación finaliza la llamada y envía a través de Asterisk el aviso correspondiente a los clientes SIP.
En caso de que no se supere el máximo definido por el usuario, se acepta la llamada, y se obtienen a través de Asterisk los parámetros de sesión SIP que luego serán utilizados por el módulo SDN.  
En el módulo SDN se realizan tres operaciones en base a la información que se extrae de la sesión SIP. El primer paso consiste en determinar la ubicación dentro de la red de los clientes SIP entre los que se debe establecer la sesión; para ello se formatea y envía una consulta al controlador SDN a través de la interfaz REST que nos devuelve la información de direccionamiento necesarias para armar las reglas de flujo basadas en OpenFlow 1.3. El segundo paso consiste en armar las reglas de flujo OpenFlow, las cuales contienen como matching la información obtenida por el descubrimiento de red y dos acciones asociadas. Las acciones consisten en marcar el tráfico del flujo RTP como prioritario (mediante el campo DSCP=XX), y posteriormente enviarlo a la cola de alta prioridad del puerto de salida que corresponda.
El tercer paso consiste en formatear el mensaje para enviarlo a través de la interfaz REST hacia el controlador SDN.
Como controlador SDN se utilizó Ryu, el cual posee módulos que implementan interfaces REST con métodos que permiten realizar consultas, establecer flujos y colas de servicio sobre los elementos de red sin necesidad de tener que conocer el protocolo OpenFlow, lo que nos brinda una excelente capa de abstracción desde el punto de vista del desarrollador. Se aprovechó el framework existente de Ryu y se lo modificó agregando los métodos REST necesarios para interactuar con la interfaz Southbound API del módulo SDN.
Como switch SDN utilizamos OpenVSwitch, el cual soporta OpenFlow 1.3 como protocolo de comunicación con el controlador SDN y permite trabajar en su implementación del Kernel-Space con colas de servicio asociadas a sus puertos.
Los clientes SIP que se utilizaron están basados en Linphone.

En la figura 4, se muestra la maqueta del prototipo desarrollado:

[Acá iría la maqueta especificada con el tipo de PBX, controlador, switch openflow, etc]


Sección V - Pruebas, evaluación y resultados obtenidos

Las pruebas realizadas consistieron en fijar un umbral de 4 sesiones mediante la interfaz de usuario, luego generar una cantidad de 4 llamadas desde los clientes SIP, con lo que se iguala el umbral preestablecido. En este punto, se pudo comprobar que todas las llamadas se establecieron con éxito, pero al intentar el inicio de una quinta llamada, el sistema actúa correctamente dando aviso a los clientes SIP acerca de la imposibilidad de establecer una nueva llamada.
Para comprobar  que las 4 llamadas que se encuentran en curso tienen garantizado el QoS, se genera un escenario de congestión inyectando tráfico best-effort. En la gráfica [X] se puede visualizar cómo el tráfico de voz resulta de mayor prioridad y no hay pérdida de paquetes, mientras que para el tráfico best-effort sucede lo contrario. 

[Acá irían las gráficas que se obtengan de la parte práctica]


Sección VI - Conclusiones

El motivo del presente trabajo era encontrar una modelización de macanismo CAC que trabaje sobre entornos de red SDN, facilitando la interoperabilidad y la programabilidad de la red frente a requerimientos de calidad de servicio que ejercen las llamadas basadas en tecnologías VOIP.

Nuestra contribución es la especificación de un modelo para el desarrollo de aplicaciones CAC en entornos SDN,  basada en el uso de interfaces API y herramientas de código abierto. 
Cabe destacar, que si bien aún no existe un marco formal de estandarización para la interacción de mecanismos CAC con IP PBXs de diferentes fabricantes, el modelo presentado brinda una posible solución a este problema, la cual puede lograrse con herramientas de uso accesible y libre, como las utilizadas en el prototipo desarrollado.

El uso de entornos SDN ofrece múltiples ventajas desde el punto de vista de la red, por ejemplo la posibilidad de que el mecanismo CAC opere con IP PBXs desarrolladas por diferentes fabricantes; así como también, la programabilidad de los elementos de red para reaccionar en forma dinámica a los requerimientos de QoS de las llamadas que se establezcan. 

En nuestra primer evaluación, hemos encontrado resultados favorables que nos alientan a pensar, adicionalmente, en el uso del modelo presentado para el desarrollo de nuevas aplicaciones sobre entornos SDN, ya sea para expandir las funcionalidades del prototipo ensayado ó para trabajar sobre nuevos escenarios.



-----------------------------------------------------------

## TODOS

- Armar gráfico/explicacion arquitectura nivel sofware de aplicacion CAC
- Hablar de pruebas simple_switch OpenFlow1.5 para utilizar nuevas metricas y features agregadas en estas versiones
- Hablar de objetivo final respecto de graficos que se esperan realizar y resultados que se esperan obtener con este modelo de trabajo










    

