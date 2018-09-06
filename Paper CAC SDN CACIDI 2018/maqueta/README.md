# Maqueta 
## Arquitectura

Al no poder tener capa 2 directa en gcloud para emular clientes y el uso del OVS se crea una maquina con Ryu/OVS/clientes virtualizando dentro de esta con vbox en un debian que vive en el promox del laboratorio de redes en UNSAM.
```
                                         XXXXXXX
          XXXX        XXXXXXXXX  X   XXXXX    X X
     XX XX   XXXXXXXXXX          XXXX         X X
    XX      +-----------------------------+   X
  XX        |                             |   X
  X         |     asterisk                |  XX
 X          |                             |  X
 X          |                             |  X
 X          +--------------+--------------+  XXXXXXX
 XX                        |                        XX
    XXXX                   |                         X     IP publica de UNSAM
   XX                      |                         X
  X         +--------------v--------------+          X       +-------------------------------------------------------------+
 XX         |                             |         X        |                                                             |
XX          |     API                     +---------------->                                                               |
X           |                             |      XX          |                  +----------------------------+             |
X           |                             |      XXXXX       |                  |                            |             |
X           |                             |          X       |                  |      RYU/OVS               |             |
XX          +-----------------------------+         XX       |                  |                            |             |
   XXXXXX                                          XX        |                  |                            |             |
     X         Google Cloud                     XXX          |                  |                            |             |
     X                                      XXXX             |                  |                            |             |
     X                                XX                     |                  |                            |             |
     X             XX                 X                      |                  |                            |             |
     XX            X  X              XX                      |               +--+---------------------------++             |
       XX         XX   X            X                        |               |                              |              |
          XX X XXXX     XX       XX                          |               |                              |              |
                         XXX X X                             |               |                              |              |
                                                             |               |                              |              |
                                                             |     +---------+------+           +-----------+---+          |
                                                             |     |                |           |               |          |
                                                             |     |                |           |               |          |
                                                             |     |                |           |               |          |
                                                             |     |   Cliente 1    |           |   Cliente 2   |          |
                                                             |     |                |           |               |          |
                                                             |     |                |           |               |          |
                                                             |     |                |           |               |          |
                                                             |     |                |           |               |          |
                                                             |     |                |           |               |          |
                                                             |     +----------------+           +---------------+          |
                                                             |                                                             |
                                                             +-------------------------------------------------------------+

```
La API va a vivir en google cloud y va a llamar al API REST de Ryu por la publica que nos habilite UNSAM.


## Links Utiles

- [acceso a la consola web](https://console.cloud.google.com/home/dashboard?project=cac-sdn)

- [como installar google sdk (opcional)](https://cloud.google.com/sdk/install)

## Status

| NAME       | ZONE       | MACHINE_TYPE              | INTERNAL_IP | EXTERNAL_IP   | STATUS  | USER     |
| ---------- | ---------- | ------------------------- | ----------- | ------------- | ------- | -------- |
| asterisk   | us-east1-b | custom (1 vCPU, 2.00 GiB) | 10.142.0.2  | 35.211.219.55 | RUNNING | asterisk |
| client1    | us-east1-b | f1-micro                  | 10.142.0.4  | 35.196.43.158 | RUNNING | ubuntu   |
| controller | us-east1-b | custom (2 vCPU, 2.00 GiB) | 10.142.0.3  | 35.196.178.40 | RUNNING | ubuntu   |
| OVS        | unsam(prom)| custom (1 vCPU, 1.00 GiB) |             |               | RUNNING | ovs      |

password momentanea ovs: sdn2018

## Comandos utiles

- acceder por ssh a los clientes linphone usando el Xserver del server en google.

```bash
ssh -X ubuntu@35.196.43.158 linphone
```

- Configurar google sdk

```
gcloud config set project cac-sdn
gcloud config set compute/zone us-east1-b
```

- Conectarse por ssh con google sdk

```
gcloud compute ssh ubuntu@client1
```

- listar las maquinas

```
gcloud compute instances list
```
