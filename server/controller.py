from operations import ServerOperations
from exceptions.exceptions import Unauthorized, UserRegister, OperationUnavailable
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
