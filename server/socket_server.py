import json
import socket
import threading
import uuid

from server.controller import control_operations


class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.client_names = {}
        self.history = {}
        self.client_address = None

    def recv_operation(self, client_socket, address):
        print(f'Connection from {address} established.')
        self.client_address = f'{address[0]}:{address[1]}'
        self.client_names[self.client_address] = 'Unknown'
        with client_socket:  # quando para de receber requisições fecha o socket
            while True:
                try:
                    recv_command = client_socket.recv(1024).decode()
                    if not recv_command:  # Quando o client desconecta
                        raise ConnectionResetError
                    request_dict = json.loads(recv_command)

                    request_id = str(uuid.uuid4())  # Gerando um ID aleatório
                    request_dict['requestId'] = request_id

                    # Envia os comandos para a função que gerencia as funções que representam as operações do servidor
                    control_operations(client_socket, request_dict, self.client_names,
                                       self.client_address, self.history)

                except ConnectionResetError:
                    print(f"Connection with {address} lost")
                    del self.client_names[self.client_address]
                    break
                except json.decoder.JSONDecodeError as e:
                    print('Badly formatted JSON')
                    print(f"Connection with {address} lost. {e}")
                    del self.client_names[self.client_address]  # para continuar na lista de clientes
                    break
                except OSError as e:
                    print('Socket error')
                    print(f"Connection with {address} lost. {e}")
                    del self.client_names[self.client_address]
                    break

    def run(self):
        while True:
            print('Waiting for connection')
            client_socket, address = self.server_socket.accept()

            # Criando e iniciando uma nova Thread
            client_thread = threading.Thread(target=self.recv_operation,
                                             args=(client_socket, address))
            client_thread.start()


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8081
    # iniciando o servidor
    server = Server(HOST, PORT)
    server.run()
