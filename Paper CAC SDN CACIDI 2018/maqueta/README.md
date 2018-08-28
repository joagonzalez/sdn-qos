# Maqueta en GCloud

## Links Utiles

- [acceso a la consola web](https://console.cloud.google.com/home/dashboard?project=cac-sdn)

- [como installar google sdk (opcional)](https://cloud.google.com/sdk/install)

## Status

| NAME       | ZONE       | MACHINE_TYPE              | INTERNAL_IP | EXTERNAL_IP   | STATUS  | USER     |
| ---------- | ---------- | ------------------------- | ----------- | ------------- | ------- | -------- |
| asterisk   | us-east1-b | custom (1 vCPU, 2.00 GiB) | 10.142.0.2  | 35.211.219.55 | RUNNING | asterisk |
| client1    | us-east1-b | f1-micro                  | 10.142.0.4  | 35.196.43.158 | RUNNING | ubuntu   |
| controller | us-east1-b | custom (2 vCPU, 2.00 GiB) | 10.142.0.3  | 35.196.178.40 | RUNNING | ubuntu   |

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
