# Socket share - compartilhar arquivos entre usuários

## Description

- O projeto de um protocolo de rede para permitir o compartilhamento de arquivos entre clientes através de um servidor.
- Desse modo, os clientes podem enviar arquivos pro servidor e solicitar arquivos dele.

## Tutorial: Como rodar a imagem do projeto a partir de um contêiner do Docker Hub

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado e configurado em seu ambiente.

### Passo 1: Pesquise a imagem desejada no Docker Hub

- Veja a imagem desse projeto no meu repositório do [Docker Hub - servidor](https://hub.docker.com/r/leandroadal/socket-server).
- Veja a imagem desse projeto no meu repositório do [Docker Hub - cliente](https://hub.docker.com/r/leandroadal/socket-client).

### Passo 2: Baixe a imagem Docker

- Abra um terminal ou prompt de comando e execute o seguinte comando com o Docker rodando em seu PC:
  
    ```
    docker pull leandroadal/socket-server:latest
    ```

    ```
    docker pull leandroadal/socket-client 
    ```

### Passo 3: Execute o container

- Após o download da imagem, execute o seguinte comando para iniciar o container:

    ```
    docker run -d --name socket-server -p 8081:8081 socket-server
    ```

    ```
    docker run --name socket-client --network host -it socket-client
    ```

- Este comando irá iniciar o programa e esperara o primeiro comando ao servidor.

### Passo 4: Acesse novamente a aplicação

- Caso queria acessar a aplicação em momento posterior siga a instrução abaixo:

- Com os container `socket-server` e `socket-client` rodando em sua máquina execute a seguinte instrução em um terminal

    ```
    docker attach socket-client
    ```

## Operações disponíveis

    • list – retorna os arquivos que estão presentes e passiveis de serem obtido do servidor;

    • upload – retorna o tamanho e o arquivo especificado pelo cliente se ele existir no servidor;

    • download – envia do cliente para o servidor um arquivo e seu tamanho;

    • remove – apaga um arquivo que foi especificado pelo cliente do servidor;

    • history – retorna uma lista com todas as requisições e respostas dadas pelo servidor;

    • list_clients – retorna uma lista com os clientes que estão conectados ao servidor;

### Exemplos de entradas

    {"operation": "list"}

    {"operation": "remove", "file_name": "name"}

    {"operation": "upload", "file_path": "testsend.txt"}

    {"operation": "download", "file_name": "test.txt"}

    {"operation": "history"}

    {"operation": "register", "name": "name"}

    {"operation": "list_clients"}

    q

### Respostas do servidor ao cliente

- See wiki in [wiki](https://www.docker.com/)
