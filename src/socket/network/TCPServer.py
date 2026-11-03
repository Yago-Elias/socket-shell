import socket, protocol
from socket.shell import parse_line, parser
from socket.shell import execute_line

# IP = socket.gethostbyname(socket.gethostname())
IP = '127.0.0.1'
PORT = 10000

skt_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

skt_server.bind((IP, PORT))
skt_server.listen()

while True:
    skt_client, _ = skt_server.accept()

    try:
        while True:
            message = protocol.receive(skt_client)
            if message is None:
                print(f'Cliente fechou a conexão.')
                break

            message = message.decode(errors='replace').strip()
            if message == 'exit':
                protocol.send(skt_client, 'Sessão encerrada!'.encode())
                break

            try:
                message = parse_line(parser(message))
                output = execute_line(*message)
            except Exception as e:
                protocol.send(skt_client, e.__str__().encode())
            else:
                protocol.send(skt_client, output.stdout + output.stderr)
    except (ConnectionResetError, BrokenPipeError):
        skt_client.close()
        break

skt_server.close()
