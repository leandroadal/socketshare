import json
import uuid

from exceptions.exceptions import Unauthorized, OperationUnavailable, UserRegister
from operations import ServerOperations
from utils import send_response, save_history, check_register


# Gerencia para qual função as operações devem seguir
def control_operations(client_socket, request_dict, client_names, client_address, history):
    operations = ServerOperations(client_socket, request_dict, client_names, client_address, history)
    try:
        command_type = request_dict['operation']
        if command_type == 'list':
            if check_register(client_names, client_address):
                operations.list_operation()
            else:
                raise Unauthorized

        elif command_type == 'remove':
            if check_register(client_names, client_address):
                operations.remove_operation()
            else:
                raise Unauthorized

        elif command_type == 'upload':
            if check_register(client_names, client_address):
                operations.upload_operation()
            else:
                raise Unauthorized

        elif command_type == 'download':
            if check_register(client_names, client_address):
                operations.download_operation()
            else:
                raise Unauthorized

        elif command_type == 'register':
            if not check_register(client_names, client_address):
                operations.register_operation()
            else:
                raise UserRegister

        elif command_type == 'history':
            if check_register(client_names, client_address):
                operations.history_operation()
            else:
                raise Unauthorized

        elif command_type == 'list_clients':
            if check_register(client_names, client_address):
                operations.list_clients_operation()
            else:
                raise Unauthorized
        else:
            raise OperationUnavailable

    except FileNotFoundError:
        response_dict = {'status': 'error', 'code': '404', 'message': 'File not found.', 'size': '0'}
        save_history(request_dict, response_dict, client_names, client_address, history)
        send_response(client_socket, response_dict)

    except OSError as e:
        response_dict = {'status': 'error', 'code': '403', 'message': f'Error accessing/transfer files: {e}'}
        save_history(request_dict, response_dict, client_names, client_address, history)
        send_response(client_socket, response_dict)

    except Unauthorized as e:
        response_dict = {'status': 'error', 'code': '401', 'message': f'{e}',
                         'requestId': request_dict['requestId']}
        save_history(request_dict, response_dict, client_names, client_address, history)
        send_response(client_socket, response_dict)

    except OperationUnavailable as e:
        response_dict = {'status': 'error', 'code': '405', 'message': f'{e}',
                         'requestId': request_dict['requestId']}
        save_history(request_dict, response_dict, client_names, client_address, history)
        send_response(client_socket, response_dict)

    except UserRegister as e:
        response_dict = {'status': 'error', 'code': '406', 'message': f'{e}',
                         'requestId': request_dict['requestId']}
        save_history(request_dict, response_dict, client_names, client_address, history)
        send_response(client_socket, response_dict)

    except Exception as e:
        response_dict = {'status': 'error', 'code': '500', 'message': f'Unexpected error occurred: {str(e)}'}
        save_history(request_dict, response_dict, client_names, client_address, history)
        send_response(client_socket, response_dict)


# Trata do recebimento dos comandos dos clientes e o tratamento de erros que os desconecta do servidor
def recv_operation(client_socket, address, client_names, history):
    print(f'Connection from {address} established.')
    client_address = f'{address[0]}:{address[1]}'
    client_names[client_address] = 'Unknown'
    while True:
        try:
            recv_command = client_socket.recv(1024).decode()
            if not recv_command:  # Quando o client desconecta
                raise ConnectionResetError
            request_dict = json.loads(recv_command)

            request_id = str(uuid.uuid4())  # Gerando um ID aleatório
            request_dict['requestId'] = request_id

            # Envia os comandos para a função que gerencia as funções que representam as operações do servidor
            control_operations(client_socket, request_dict, client_names, client_address, history)

        except ConnectionResetError:
            print(f"Connection with {address} lost")
            del client_names[client_address]
            client_socket.close()
            break
        except json.decoder.JSONDecodeError as e:
            print('Badly formatted JSON')
            print(f"Connection with {address} lost. {e}")
            del client_names[client_address]  # para continuar na lista de clientes
            client_socket.close()
            break
