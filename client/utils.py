import json
import os


# Enviar a resposta para o cliente
def send_response(client_socket, response_dict):
    response_json = json.dumps(response_dict)
    client_socket.send(response_json.encode('utf-8'))


# Salvando o histórico
def save_history(command_dict, response_dict, client_names, client_address, history):
    history[command_dict['requestId']] = {'operation': command_dict['operation'],
                                          'status': response_dict['status'], 'code': response_dict['code'],
                                          'client': client_names[client_address]}


# Verifica se o cliente difere de Unknown em caso afirmativo ele ja foi registrado
def check_register(client_names, client_address):
    return client_names[client_address] != 'Unknown'


# Retorna uma lista dos arquivos
def list_files():
    return '; '.join(os.listdir())
