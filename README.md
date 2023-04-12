# Socket share - compartilhar arquivos entre usuários
 
# Description:
- O projeto de um protocolo de rede para permitir o compartilhamento de arquivos entre clientes através de um servidor.
- Desse modo, os clientes podem enviar arquivos pro servidor e solicitar arquivos dele.

## Operações disponíveis:

    • list – retorna os arquivos que estão presentes e passiveis de serem obtido do servidor;

    • upload – retorna o tamanho e o arquivo especificado pelo cliente se ele existir no servidor;

    • download – envia do cliente para o servidor um arquivo e seu tamanho;

    • remove – apaga um arquivo que foi especificado pelo cliente do servidor;

    • history – retorna uma lista com todas as requisições e respostas dadas pelo servidor;

    • list_clients – retorna uma lista com os clientes que estão conectados ao servidor;


### Exemplos de entradas:

    {"operation": "list"}

    {"operation": "remove", "file_name": "name"}

    {"operation": "upload", "file_path": "D:\caminho-do-arquivo"}

    {"operation": "download", "file_name": "test.text"}

    {"operation": "history"}

    {"operation": "register", "name": "name"}

    {"operation": "list_clients"}

    {"operation": "q"}