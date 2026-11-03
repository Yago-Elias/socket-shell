import socket
import utils

# obtêm o ip atual do computador
IP = socket.gethostbyname(socket.gethostname())
PORT = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP, PORT))
utils.log(F'Servidor iniciado em {IP}:{PORT}')

while True:
    try:
        message, client_address = server.recvfrom(2048)
        utils.log(f'Recebendo dados de {client_address[0]}')

        message = message.decode().upper()

        server.sendto(message.encode(), client_address)
    except KeyboardInterrupt:
        utils.log('Servidor interrompido (^C)', utils.ERROR)
        server.sendto(utils.COL_ERROR.encode(), (IP, PORT))
        server.close()
        break
