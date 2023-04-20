import json
import os

from utils import list_files, send_response, save_history


# lida com a efetuação das operações do servidor
class ServerOperations:
    def __init__(self, client_socket, request_dict, client_names, client_address, history):
        self.client_socket = client_socket
        self.request_dict = request_dict
        self.client_address = client_address
        self.client_names = client_names
        self.history = history

    # Cria uma lista com os arquivos disponíveis no servidor
    def list_operation(self):
        file_list = list_files()
        response_dict = {'status': 'ok', 'code': '200', 'message': file_list,
                         'requestId': self.request_dict['requestId']}

        save_history(self.request_dict, response_dict, self.client_names, self.client_address, self.history)
        send_response(self.client_socket, response_dict)

    # Remove um arquivo especificado pelo cliente do servidor
    def remove_operation(self):
        file_name = self.request_dict['file_name']
        if (file_name == '__init__.py' or file_name == 'controller.py' or file_name == 'operations.py' or
                file_name == 'socket_server.py' or file_name == 'utils.py'):
            response_dict = {'status': 'error', 'code': '402', 'message': 'Cannot delete this file.',
                             'requestId': self.request_dict['requestId']}
        else:
            os.remove(file_name)
            response_dict = {'status': 'ok', 'code': '202', 'message': 'File removed successfully!',
                             'requestId': self.request_dict['requestId']}

        save_history(self.request_dict, response_dict, self.client_names, self.client_address, self.history)
        send_response(self.client_socket, response_dict)

    # Recebe e guarda um arquivo do cliente no servidor
    def upload_operation(self):
        file_name = self.request_dict['file_name']
        file_size = int(self.request_dict['size'])
        # confirmação para que o cliente saiba que pode enviar o arquivo
        response_dict = {'status': 'ok', 'code': '203', 'size': file_size,
                         'requestId': self.request_dict['requestId']}
        send_response(self.client_socket, response_dict)

        with open(file_name, 'wb') as file:
            size_received = 0
            while size_received < file_size:
                data = self.client_socket.recv(1024)
                file.write(data)
                size_received += len(data)
        response_dict = {'status': 'ok', 'code': '204', 'message': f'File {file_name} received successfully!',
                         'requestId': self.request_dict['requestId']}

        save_history(self.request_dict, response_dict, self.client_names, self.client_address, self.history)
        send_response(self.client_socket, response_dict)

    # Envia um arquivo do servidor para o cliente
    def download_operation(self):
        file_name = self.request_dict['file_name']
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f'File not found: {file_name}')
        file_size = os.path.getsize(file_name)
        response_dict = {'status': 'ok', 'code': '205', 'size': file_size,
                         'requestId': self.request_dict['requestId']}
        send_response(self.client_socket, response_dict)
        with open(file_name, 'rb') as file:
            size_sent = 0
            while size_sent < file_size:
                data = file.read(1024)
                self.client_socket.send(data)
                size_sent += len(data)
        response_dict = {'status': 'ok', 'code': '201', 'message': f'File "{file_name}" sent successfully!',
                         'size': file_size, 'requestId': self.request_dict['requestId']}

        save_history(self.request_dict, response_dict, self.client_names, self.client_address, self.history)
        send_response(self.client_socket, response_dict)

    # Recupera o histórico de requisições dos clientes para o servidor
    def history_operation(self):
        history_operations = json.dumps(self.history)
        response_dict = {'status': 'ok', 'code': '206', 'history': history_operations}
        send_response(self.client_socket, response_dict)

    # Registra o nome de um cliente no servidor
    def register_operation(self):
        client_name = self.request_dict['name']
        self.client_names[self.client_address] = client_name  # sobrescreve o nome
        response_dict = {'status': 'ok', 'code': '207', 'message': 'Client registered successfully!',
                         'requestId': self.request_dict['requestId']}
        save_history(self.request_dict, response_dict, self.client_names, self.client_address, self.history)
        send_response(self.client_socket, response_dict)

    # Mostra a lista de Clients conectadas no servidor
    def list_clients_operation(self):
        # Criando lista de clientes a partir da key, value de client_names e juntando com o método join
        clients = '; '.join(f"[{name}] {address}" for address, name in self.client_names.items())
        response_dict = {'status': 'ok', 'code': '208', 'clients': f"Connected clients: {clients}",
                         'requestId': self.request_dict['requestId']}

        save_history(self.request_dict, response_dict, self.client_names, self.client_address, self.history)
        send_response(self.client_socket, response_dict)
