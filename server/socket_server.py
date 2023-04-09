import socket
import threading
from controller import recv_operation

HOST = 'localhost'
PORT = 8081


class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.client_names = {}
        self.history = {}
        self.client_address = None

    def run(self):
        while True:
            print('Waiting for connection')
            client_socket, address = self.server_socket.accept()  # aceita a conexão com a porta e host especificados
            # Criando e iniciando uma nova Thread
            client_thread = threading.Thread(target=recv_operation,
                                             args=(client_socket, address, self.client_names, self.history))
            client_thread.start()


# iniciando o sevidor
server = Server(HOST, PORT)
server.run()
