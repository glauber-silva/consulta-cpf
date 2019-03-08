# Consulta CPF API

Uma simples api REST para consulta de CPF diretamente na SERPRO

Foi usado Python, Flask, Pipenv, Docker, Docker Compose e Nginx para a construção dessa API


## Instalação
1. Clone o respositório: `git clone https://glauber-silva@bitbucket.org/glauber-silva/consulta-cpf.git`.
2. `cd` no diretório `consulta-cpf`: `cd shipment-list`.
3. Execute o comando `sh install.sh`
4. Verifique a versão do Docker com o comando: `docker -v`.
```bash
Docker version 18.09.0, build 4d60db4
```
5. Verifique a versão do Docker Compose com o comando : `docker-compose -v`
```bash
docker-compose version 1.23.2, build 1110ad01
``` 

Se a instalação não funcionar contacte via email [Glauber](mailto:glauber.lucio.silva@gmail.com).

## Iniciar a aplicação
1. Ainda no mesmo diretório, execute: `sh start.sh` 
2. Depois que toda a aplicação inicializar, execute: `sudo docker ps` a saída deverá ser semelhante a esta:
```bash
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                     NAMES
c54c4142d6af        consulta-cpf_nginx      "nginx -g 'daemon of…"   26 seconds ago      Up 19 seconds       0.0.0.0:80->80/tcp        consulta-cpf_nginx_1
c2b89861492d        consulta-cpf_cpf        "/bin/sh -c 'python …"   26 seconds ago      Up 20 seconds       0.0.0.0:5001->5000/tcp    consulta-cpf_cpf_1
daa7ee69765f        consulta-cpf_users      "/usr/src/app/entryp…"   30 seconds ago      Up 26 seconds       0.0.0.0:5002->5000/tcp    consulta-cpf_users_1
f5c227f36bd8        consulta-cpf_users-db   "docker-entrypoint.s…"   32 seconds ago      Up 30 seconds       0.0.0.0:32772->5432/tcp   consulta-cpf_users-db_1
```

Para testes execute: `sh test.sh`

Depois desses passos a aplicação estará pronta pra uso. Abaixo há uma documentação básica


## API SPECS

### Authentication Header

`Authorization: Bearer jwt.token.here`

## JSON Objects:

Tenha certeza que o content-type correto é retornado `Content-Type: application/json` . 
Abaixo algumas saidas simples

### Users (Para registro)
```JSON
{
 "auth_token": "jwt.token.here",
    "message": "Registrado com sucesso.",
    "status": "success"
}
```

### Users (Para Login)
```JSON
{
 "auth_token": "jwt.token.here",
    "message": "Login realizado com sucesso.",
    "status": "success"
}
```

### CPF 
```JSON
{
    "status": "regular"
}
```


## Endpoints:


### Registro:
Campos obrigatórios: `email`, `username`, `password`

`POST /auth/register`

Examplo  body:
```JSON
{
 
    "username": "example",
    "email": "example@email.com",
    "password": "maiorqueoito"
  
}
```

### Autenticação
Campos obrigatórios: `username`, `password`

`POST /auth/login`

Examplo  body:

```JSON
{
 
    "username": "example",
    "password": "maiorqueoito"
  
}
```






### Get CPF

`GET /cpf/<cpf>`

Exemplo URL : `/cpf/40442820135`

Autenticação necessária, exemplo header:

```metadata json
Content-Type:application/json
Authorization: Bearer jwt.token.here
```

Abaixo alguns CPF para degustação:

| CPF           | SITUAÇÃO CADASTRAL              | 
|---------------|---------------------------------|
|---------------|---------------------------------|
| 40442820135   |   CPF Regular                   |
| 63017285995	|   CPF Regular                   |
| 91708635203	|   CPF Regular                   |
| 58136053391	|   CPF Regular                   |
| 40532176871	|   Suspensa                      |
| 47123586964	|   Suspensa                      |
| 07691852312	|   Pendente de Regularização     |
| 10975384600	|   Pendente de Regularização     |
| 01648527949	|   Cancelada por Multiplicidade  |
| 47893062592	|   Cancelada por Multiplicidade  |
| 98302514705	|   Nula                          |
| 18025346790	|   Nula                          |
| 64913872591	|   Cancelada de Ofício           |
| 52389071686	|   Cancelada de Ofício           |
| 05137518743	|   Titular Falecido              |
| 08849979878	|   Titular Falecido              |
---------------------------------------------------