import socket, protocol

# IP = socket.gethostbyname(socket.gethostname())
IP = '127.0.0.1'
PORT = 10000

skt_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    skt_client.connect((IP, PORT))
except ConnectionRefusedError:
    print(f'Não foi possível conectar ao servidor {IP}:{PORT}')
else:
    while True:
        try:
            input_shell = input(f'{IP}:{PORT} $ ')
        except (EOFError, KeyboardInterrupt):
            break
        else:
            if input_shell == 'exit': break

        protocol.send(skt_client, input_shell.encode())
        message = protocol.receive(skt_client)

        if message is None:
            print('Servidor caiu.')
            break

        print(message.decode(), end='')

skt_client.close()
