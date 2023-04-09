# Socket share - compartilhar arquivos entre usuários
 
# Description:
- O projeto de um protocolo de rede para permitir o compartilhamento de arquivos entre clientes através de um servidor.
- Desse modo, os clientes podem enviar arquivos pro servidor e solicitar arquivos dele.
# Tutorial: Como rodar a imagem do projeto a partir de um contêiner do Docker Hub

## Pré-requisitos:
- [Docker](https://www.docker.com/) instalado e configurado em seu ambiente.

## Passo 1: Pesquise a imagem desejada no Docker Hub
- Veja a imagem desse projeto no meu repositório do .

## Passo 2: Baixe a imagem Docker
- Abra um terminal ou prompt de comando e execute o seguinte comando com o Docker rodando em seu PC:
  
    ```
    docker pull   
    ```

## Passo 3: Execute o container
- Após o download da imagem, execute o seguinte comando para iniciar o container:
    ```
    docker run -p 
    ```

- Este comando irá iniciar o container e redirecionar as solicitações HTTP para a porta 8080 do host.

## Passo 4: Acesse a aplicação
- Abra um navegador web e acesse `http://localhost:8081/` para acessar a aplicação.


## Operações disponíveis:

    • list – retorna os arquivos que estão presentes e passiveis de serem obtido do servidor;

    • upload – retorna o tamanho e o arquivo especificado pelo cliente se ele existir no servidor;

    • download – envia do cliente para o servidor um arquivo e seu tamanho;

    • remove – apaga um arquivo que foi especificado pelo cliente do servidor;

    • history – retorna uma lista com todas as requisições e respostas dadas pelo servidor;

    • list_clients – retorna uma lista com os clientes que estão conectados ao servidor;


### Exemplos de entradas:

    {"operation": "list"}

    {"operation": "remove", "file_name": "name"} {"operation": "upload", "file_path": "/test.txt"}

    {"operation": "upload", "file_path": "D:\Programação\Projetos\Python\socketshare\client\testsend.txt"}

    {"operation": "download", "file_name": "test.text"}

    {"operation": "history"}

    {"operation": "register", "name": "name"}

    {"operation": "list_clients"}

    {"operation": "q"} {"operation": "download", "file_name": "pycharm-community-2023.1.exe"}