import json
import os
import socket


def send_request(request_dict):
    try:
        # Convertendo o dicionário em uma ‘string’ JSON
        command_json = json.dumps(request_dict)
        # Enviando o comando para o servidor
        client_socket.send(command_json.encode())
    except socket.error as e:
        print('Error communicating with server:', e.strerror)


def recv_response():
    try:
        # Recebendo uma 'string' no formato JSON
        response_str_json = client_socket.recv(1024).decode()
        # Convertendo a ‘string’ JSON em um dicionário python
        response_dict = json.loads(response_str_json)
        return response_dict
    except json.decoder.JSONDecodeError as e:
        print(f'Error ao decodificar a resposta do servidor {str(e)}')
    except socket.error as e:
        print('Error communicating with server:', e.strerror)


# Chama as funções de envio de requisição e recebimento de resposta
def send_recv(request_dict):
    # Envia a solicitação ao servidor
    send_request(request_dict)
    # Recebe a resposta e a retorna
    return recv_response()


def upload_file(request_dict):
    # Caminho do arquivo a ser enviado para o servidor
    file_path = request_dict['file_path']
    del request_dict['file_path']
    try:
        # Guardando o nome do arquivo e seu tamanho
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        # # Criando um dicionário para ser convertido para JSON
        request_dict['file_name'] = file_name
        request_dict['size'] = file_size
        print(request_dict)
        # Envia a solicitação ao servidor
        send_request(request_dict)

        response_dict = recv_response()
        if response_dict['status'] != "error":
            # Lendo a arquivo através do read bytes e os enviando através do socket
            with open(file_path, 'rb') as file:
                size_sent = 0  # tamanho em ‘bytes’ enviado
                while size_sent < file_size:
                    data = file.read(1024)
                    client_socket.send(data)
                    size_sent += len(data)

            # Recebida a resposta do servidor
            response_dict = recv_response()
        print(response_dict)

    except FileNotFoundError as e:
        print(e.strerror)
    except OSError as e:
        print(e.strerror)
    except json.decoder.JSONDecodeError:
        print('Error ao decodificar a resposta do servidor')
    except Exception as e:
        print('Error occurred during file transfer:', str(e))


def download_file(request_dict):
    file_name = request_dict['file_name']
    # Enviando a requisição e recebendo o tamanho do arquivo a ser recebido
    response_dict = send_recv(request_dict)
    try:
        print(request_dict)
        # O tamanho do Arquivo é usado para verificar se o arquivo foi localizado
        file_size = int(response_dict['size'])
        if file_size == 0:
            raise FileNotFoundError

        # Recebendo e criando o arquivo no armazenamento do cliente através do write bytes
        with open(file_name, 'wb') as file:
            size_received = 0
            while size_received < file_size:  # O tamanho do Arquivo é usado para verificar até quando espera as
                data = client_socket.recv(1024)  # respostas do servidor
                file.write(data)
                size_received += len(data)
        print(recv_response())

    except FileNotFoundError:
        print(response_dict)
    except KeyError:
        print(response_dict)
    except Exception as e:
        print('Error occurred during file transfer:', str(e))


# {"operation": "list"}
# {"operation": "remove", "file_name": "name"}
# {"operation": "upload", "file_path": "testsend.txt"}
# {"operation": "download", "file_name": "test.txt"}
# {"operation": "history"}
# {"operation": "register", "name": "name"}
# {"operation": "list_clients"}
# {"operation": "q"}
def run():
    while True:
        try:
            command = input('Enter command (list, remove, upload, download, history, register, list_clients; '
                            'q to quit): ')
            # Sair
            if command == 'q':
                print('Saindo do Programa...')
                break
            # Formatando a string para o path ficar compatível com o JSON
            command = command.replace("\\", "/")
            command_dict = json.loads(command)

            if command_dict['operation'] == 'list' or command_dict['operation'] == 'remove' or \
                    command_dict['operation'] == 'history' or command_dict['operation'] == 'register' or \
                    command_dict['operation'] == 'list_clients':
                print(send_recv(command_dict))

            elif command_dict['operation'] == 'upload':
                upload_file(command_dict)

            elif command_dict['operation'] == 'download':
                download_file(command_dict)

        except json.decoder.JSONDecodeError:
            print('JSON mal formatado')

    client_socket.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8081

    # Inicia o socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    run()
